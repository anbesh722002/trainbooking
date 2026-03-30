from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.bookings import CreateBooking,UpdateBooking,BookingResponse
from models import Booking
from sqlalchemy import desc,func


router = APIRouter(prefix="/bookings",tags=["Bookings"])

@router.post("/",response_model=BookingResponse)
def createbooking(book : CreateBooking ,db : Session = Depends(get_db)):
    seat_exists = db.query(Booking).filter(
        Booking.train_no == book.train_no,
        Booking.coach == book.coach,
        Booking.seat_no == book.seat_no,
        Booking.status.in_(["BOOKED", "CONFIRMED"])).first()
    if seat_exists:
        raise HTTPException(status_code=400,detail="Seat already booked")
    else:
        seatCount = db.query(Booking).filter(
        Booking.train_no == book.train_no,
        Booking.coach == book.coach,
        Booking.status.in_(["BOOKED", "CONFIRMED"])).count()
        if seatCount < 2 :
            create_booking = Booking(**book.model_dump(),status="BOOKED")
            db.add(create_booking)
            db.commit()
            db.refresh(create_booking)
            return create_booking
        else :
            waiting_db = db.query(func.max(Booking.waiting_no)).filter(
            Booking.train_no == book.train_no,
            Booking.coach == book.coach,
            Booking.status == "WAITING").scalar()
            max_waiting = waiting_db if waiting_db else 0
            createWaiting = Booking(**book.model_dump(exclude={"seat_no"}),seat_no=None,status="WAITING",waiting_no = max_waiting + 1)
            db.add(createWaiting)
            db.commit()
            db.refresh(createWaiting)
            return createWaiting

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
    
@router.put("/{booking_id}")
def cancelbooking(booking_id : int ,db : Session = Depends(get_db)):
    cancel_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if cancel_booking:
        cancel_booking.status = "CANCELLED"
        seatno = cancel_booking.seat_no
        traino = cancel_booking.train_no
        coach = cancel_booking.coach
        waiting_db = db.query(Booking).filter(
            Booking.train_no == traino,
            Booking.coach == coach,
            Booking.status == "WAITING").order_by(Booking.waiting_no).first()
        if waiting_db:
            waiting_db.seat_no = seatno
            waiting_db.status = "CONFIRMED"
            waiting_db.waiting_no = None
        db.commit()
        db.refresh(cancel_booking)
        return f"{booking_id} is Cancelled Successfully"
    else:
        return "Booking Not Found"


    
@router.delete("/{booking_id}")
def deletebookings(booking_id : int , db : Session = Depends(get_db)):
    delete_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if delete_booking:
        db.delete(delete_booking)
        db.commit()
        return f"{booking_id} is Deleted Successfully"
    else:
        raise HTTPException(status_code=404,detail="incorrect Booking Id")

