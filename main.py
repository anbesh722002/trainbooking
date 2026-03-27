from fastapi import FastAPI
from database import Base,engine
import models
from routers import trains_router,bookings_router


app = FastAPI()
app.include_router(trains_router.router)
app.include_router(bookings_router.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def show():
    return {"message" : "Helo FastApi"}

