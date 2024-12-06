from typing import Optional

from pymongo import MongoClient

from models import Parcel

MONGO_URL = "mongodb://mongo:27017/"
mongo_client = MongoClient(MONGO_URL)
collection = mongo_client["mongo"]["parcels"]


class ParcelService:
    def __init__(self):
        self.collection = collection
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
