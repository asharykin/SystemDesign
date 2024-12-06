import json
from typing import Optional

import redis

from entities import Delivery
from services import SessionLocal

REDIS_URL = "redis://redis:6379/deliveries"
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


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
