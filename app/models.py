from pydantic import BaseModel


class User(BaseModel):
    id: int = None
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    address: str

    class Config:
        orm_mode = True


class Parcel(BaseModel):
    id: int = None
    description: str
    weight: float
    user_id: int
    delivery_id: int

    class Config:
        orm_mode = True


class Delivery(BaseModel):
    id: int = None
    sender_id: int
    receiver_id: int

    class Config:
        orm_mode = True
