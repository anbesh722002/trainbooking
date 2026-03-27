from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.bookings import CreateBooking,UpdateBooking,BookingResponse
from models import Booking



router = APIRouter(prefix="/bookings",tags=["Bookings"])

@router.post("/",response_model=BookingResponse)
def createbooking(book : CreateBooking ,db : Session = Depends(get_db)):
    create_booking = Booking(**book.model_dump())
    db.add(create_booking)
    db.commit()
    db.refresh(create_booking)
    return create_booking

@router.get("/",response_model=list[BookingResponse])
def getAllBookings(db : Session = Depends(get_db)):
    return db.query(Booking).all()

@router.get("/{booking_id}",response_model=BookingResponse)
def getBookings(booking_id : int,db : Session = Depends(get_db)):
    get_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if get_booking:
        return get_booking
    else:
        raise HTTPException(status_code=404,detail="In correct Booking Id")
    
@router.put("/{booking_id}",response_model=BookingResponse)
def updatebookings(booking_id : int,booking : UpdateBooking , db : Session = Depends(get_db)):
    update_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if update_booking:
        for key,Value in booking.model_dump(exclude_unset=True).items():
            setattr(update_booking,key,Value)
        db.commit()
        db.refresh(update_booking)
        return update_booking
    else:
        raise HTTPException(status_code=404,detail="Incorrect Booking Id")
    
@router.delete("/{booking_id}")
def deletebookings(booking_id : int , db : Session = Depends(get_db)):
    delete_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if delete_booking:
        db.delete(delete_booking)
        db.commit()
        return f"{id} is Deleted Successfully"
    else:
        raise HTTPException(status_code=404,detail="incorrect Booking Id")
