from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.trains import CreateTrains,UpdateTrains,TrainsResponse
from models import Train


router = APIRouter(prefix="/trains",tags=["Trains"])


@router.post("/",response_model=TrainsResponse)
def createtrain(train : CreateTrains,db : Session = Depends(get_db)):
    create_train = Train(**train.model_dump())
    db.add(create_train)
    db.commit()
    db.refresh(create_train)
    return create_train

@router.get("/", response_model=list[TrainsResponse])
def getAlltrains(db : Session = Depends(get_db)):
    return db.query(Train).all()

@router.get("/{id}",response_model=TrainsResponse)
def gettrain(id : int , db : Session = Depends(get_db)):
    get_train = db.query(Train).filter(Train.id == id).first()
    if get_train:
        return get_train
    else:
     raise   HTTPException(status_code=404,detail="Train Not Found")

@router.put("/{id}",response_model=TrainsResponse)
def updatetrain(id : int ,train : UpdateTrains, db : Session = Depends(get_db)):
    update_train = db.query(Train).filter(Train.id == id).first()
    if update_train:
        for key,value in train.model_dump(exclude_unset=True).items():
            setattr(update_train, key, value)
        db.commit()
        db.refresh(update_train)
        return update_train
    else:
      raise  HTTPException(status_code=404,detail="Train not Found")
    
@router.delete("/{id}")
def deletetrain(id : int , db : Session = Depends(get_db)):
   del_train = db.query(Train).filter(Train.id == id).first()
   if del_train:
      db.delete(del_train)
      db.commit()
      return(f"id : {id}   : Deleted Succesfully")
   else:
      raise HTTPException(status_code=404,detail="Train Not Found")




