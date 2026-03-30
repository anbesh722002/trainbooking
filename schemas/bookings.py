from pydantic import BaseModel
from typing import Optional

class CreateBooking(BaseModel):
    train_no : int
    name : str
    coach : str
    seat_no : Optional[int] = None

class UpdateBooking(BaseModel):
    train_no : int
    name : str
    coach : str
    seat_no : Optional[int] = None
    status : str

class BookingResponse(BaseModel):
    booking_id : int
    train_no : int
    name : str
    coach : str
    seat_no : Optional[int] = None
    status : str
    waiting_no : Optional[int] = None

    class Config:
        from_attributes = True