import json
from typing import Optional

import redis
from passlib.context import CryptContext
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entities import User, Delivery
from models import Parcel

DB_URL = "postgresql://postgres:123456@db:5432/postgres"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

MONGO_URL = "mongodb://mongo:27017/"
mongo_client = MongoClient(MONGO_URL)

REDIS_URL = "redis://redis:6379/deliveries"
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


class UserService:
    def __init__(self):
        self.session = SessionLocal
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def save(self, user: User):
        with self.session() as session:
            user.password = self.pwd_context.hash(user.password)
            user = User(**user.__dict__)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def find_all(self):
        with self.session() as session:
            return session.query(User).all()

    def find_by_username(self, username: str):
        with self.session() as session:
            return session.query(User).filter(User.username == username).first()

    def find_by_first_name_and_last_name(self, first_name: str, last_name: str):
        with self.session() as session:
            query = session.query(User)
            if first_name:
                query = query.filter(User.first_name.like(f"%{first_name}%"))
            if last_name:
                query = query.filter(User.last_name.like(f"%{last_name}%"))
            return query.all()

    def validate_credentials(self, username: str, password: str):
        user = self.find_by_username(username)
        if user and self.pwd_context.verify(password, user.password):
            return True
        return False


class ParcelService:
    def __init__(self):
        self.collection = mongo_client["mongo"]["parcels"]
        self.collection.create_index([("user_id", 1)])
        self.save(Parcel(description="Clothes", weight=2.575, user_id=1, delivery_id=1))
        self.save(Parcel(description="Stationery", weight=0.425, user_id=2, delivery_id=2))

    def save(self, parcel: Parcel):
        result = self.collection.insert_one(parcel.__dict__)
        parcel.id = str(result.inserted_id)
        return parcel

    def find_by_user_id(self, user_id: Optional[int] = None):
        if user_id:
            query = {"user_id": user_id}
        else:
            query = {}
        parcels = self.collection.find(query)
        return [Parcel(**parcel) for parcel in parcels]


class DeliveryService:
    def __init__(self):
        self.session = SessionLocal
        self.redis_client = redis_client

    def save(self, delivery: Delivery):
        with self.session() as session:
            delivery = Delivery(**delivery.__dict__)
            session.add(delivery)
            session.commit()
            session.refresh(delivery)
            return delivery

    def find_by_sender_or_receiver_id(self, sender_id: Optional[int] = None, receiver_id: Optional[int] = None):
        deliveries = []

        if sender_id:
            keys = self.redis_client.keys(f"sender:{sender_id}:delivery:*")
            for key in keys:
                delivery_str = self.redis_client.get(key)
                delivery_dict = json.loads(delivery_str)
                deliveries.append(Delivery(**delivery_dict))

        elif receiver_id:
            keys = self.redis_client.keys(f"receiver:{receiver_id}:delivery:*")
            for key in keys:
                delivery_str = self.redis_client.get(key)
                delivery_dict = json.loads(delivery_str)
                deliveries.append(Delivery(**delivery_dict))

        if not deliveries:
            with self.session() as session:
                query = session.query(Delivery)
                if sender_id:
                    query = query.filter(Delivery.sender_id == sender_id)
                elif receiver_id:
                    query = query.filter(Delivery.receiver_id == receiver_id)
                deliveries = query.all()

                for delivery in deliveries:
                    delivery_dict = delivery.__dict__
                    delivery_dict.pop("_sa_instance_state")
                    self.redis_client.set(f"sender:{delivery.sender_id}:delivery:{delivery.id}", json.dumps(delivery_dict))
                    self.redis_client.set(f"receiver:{delivery.receiver_id}:delivery:{delivery.id}", json.dumps(delivery_dict))

        return deliveries
