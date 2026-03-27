from pydantic import BaseModel

class CreateBooking(BaseModel):
    train_no : int
    name : str
    coach : str
    seat_no : int
    status : str

class UpdateBooking(BaseModel):
    train_no : int
    name : str
    coach : str
    seat_no : int
    status : str

class BookingResponse(BaseModel):
    booking_id : int
    train_no : int
    name : str
    coach : str
    seat_no : int
    status : str

    class Config:
        from_attributes = True