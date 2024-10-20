from typing import List, Optional

from fastapi import APIRouter, Depends

from entities import Delivery
from routers.auth import get_current_user
from services import DeliveryService

router = APIRouter()
delivery_service = DeliveryService()


@router.post("/deliveries", response_model=Delivery)
def create_delivery(delivery: Delivery, current_user: str = Depends(get_current_user)):
    return delivery_service.save(delivery)


@router.get("/deliveries", response_model=List[Delivery])
def get_deliveries_by_sender_or_receiver(sender_id: Optional[int] = None, receiver_id: Optional[int] = None, current_user: str = Depends(get_current_user)):
    return delivery_service.find_by_sender_or_receiver_id(sender_id, receiver_id)
