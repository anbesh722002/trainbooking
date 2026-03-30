from sqlalchemy import Column,String,Integer,ForeignKey
from database import Base


class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer,primary_key=True)
    train_no = Column(Integer)


class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer,primary_key=True)
    train_no = Column(Integer,ForeignKey("trains.train_no"))
    name = Column(String)
    coach = Column(String)
    seat_no = Column(Integer,nullable=True)
    status = Column(String)
    waiting_no = Column(Integer, nullable=True)
