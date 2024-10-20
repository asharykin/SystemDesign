from typing import Optional

from passlib.context import CryptContext

from entities import User, Delivery, Parcel


class UserService:
    def __init__(self):
        self.users = {}
        self.user_id_counter = 0
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.create_admin()

    def create_admin(self):
        admin = User(username="admin", password="secret", first_name="Admin",
                     last_name="Adminov", email="admin@gmail.com",
                     address="10 Arbat Street Moscow")
        self.save(admin)

    def find_all(self):
        return list(self.users.values())

    def save(self, user: User):
        self.user_id_counter += 1
        user.id = self.user_id_counter
        user.password = self.pwd_context.hash(user.password)
        self.users[user.username] = user
        return user

    def find_by_username(self, username: str):
        return self.users.get(username)

    def find_by_first_name_and_last_name(self, first_name: str, last_name: str):
        return [
            user for user in self.find_all()
            if first_name in user.first_name and last_name in user.last_name
        ]

    def validate_credentials(self, username: str, password: str):
        user = self.users.get(username)
        if user and self.pwd_context.verify(password, user.password):
            return True
        return False


class ParcelService:
    def __init__(self):
        self.parcels = {}
        self.parcel_id_counter = 0

    def save(self, parcel: Parcel):
        self.parcel_id_counter += 1
        parcel.id = self.parcel_id_counter
        self.parcels[parcel.id] = parcel
        return parcel

    def find_by_user_id(self, user_id: int):
        return [parcel for parcel in self.parcels.values() if user_id is None or parcel.user_id == user_id]


class DeliveryService:
    def __init__(self):
        self.deliveries = {}
        self.delivery_id_counter = 0

    def save(self, delivery: Delivery):
        self.delivery_id_counter += 1
        delivery.id = self.delivery_id_counter
        self.deliveries[delivery.id] = delivery
        return delivery

    def find_by_sender_or_receiver_id(self, sender_id: Optional[int] = None, receiver_id: Optional[int] = None):
        return [
            delivery for delivery in self.deliveries.values()
            if (sender_id is None or delivery.sender_id == sender_id) and
               (receiver_id is None or delivery.receiver_id == receiver_id)
        ]
