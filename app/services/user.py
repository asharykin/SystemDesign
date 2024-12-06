import json
import threading
import time

from confluent_kafka import Producer, Consumer
from passlib.context import CryptContext

from entities import User
from services import SessionLocal

kafka_bootstrap_servers = "kafka1:9092,kafka2:9092"
kafka_topic = "user_topic"
kafka_consumer_group = "user_group"


class UserService:
    def __init__(self):
        self.session = SessionLocal
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.kafka_producer = Producer({"bootstrap.servers": kafka_bootstrap_servers})

    def save(self, user: User):
        user.password = self.pwd_context.hash(user.password)
        user_dict = user.__dict__
        print(user_dict)
        self.kafka_producer.produce(kafka_topic, json.dumps(user_dict).encode("utf-8"))
        self.kafka_producer.flush()
        return "Message sent"

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


class UserConsumer:
    def __init__(self):
        self.session = SessionLocal
        self.kafka_consumer = Consumer({
            "bootstrap.servers": kafka_bootstrap_servers,
            "group.id": kafka_consumer_group,
            "auto.offset.reset": "earliest"
        })
        self.kafka_consumer.subscribe([kafka_topic])

    def consume(self):
        while True:
            time.sleep(5)
            msg = self.kafka_consumer.poll()

            if msg is None:
                continue
            if msg.error():
                continue

            user_data = json.loads(msg.value().decode("utf-8"))
            user = User(**user_data)
            with self.session() as session:
                session.add(user)
                session.commit()

    def run(self):
        threading.Thread(target=self.consume, daemon=True).start()
