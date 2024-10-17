from typing import List, Optional

from fastapi import APIRouter, Depends

from entities import Parcel
from routers.auth import get_current_user
from services import ParcelService

router = APIRouter()
parcel_service = ParcelService()


@router.post("/parcels", response_model=Parcel)
def create_parcel(parcel: Parcel, current_user: str = Depends(get_current_user)):
    return parcel_service.save(parcel)


@router.get("/parcels", response_model=List[Parcel])
def get_parcels_by_user_id(user_id: Optional[int] = None, current_user: str = Depends(get_current_user)):
    return parcel_service.find_all_or_by_user_id(user_id)
