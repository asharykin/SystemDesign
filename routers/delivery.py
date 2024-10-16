from fastapi import APIRouter
from entities import Delivery
from services import DeliveryService
from typing import List, Optional

router = APIRouter()
delivery_service = DeliveryService()


@router.post("/deliveries", response_model=Delivery)
def create_delivery(delivery: Delivery):
    return delivery_service.save(delivery)


@router.get("/deliveries", response_model=List[Delivery])
def get_deliveries_by_sender_or_receiver(sender_id: Optional[int] = None, receiver_id: Optional[int] = None):
    return delivery_service.find_all_or_by_sender_or_receiver_id(sender_id, receiver_id)
