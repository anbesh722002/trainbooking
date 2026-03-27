from pydantic import BaseModel

class CreateTrains(BaseModel):
    train_no : int

class UpdateTrains(BaseModel):
    train_no : int

class TrainsResponse(BaseModel):
    id : int
    train_no : int

    class Config:
        from_attributes = True

        

