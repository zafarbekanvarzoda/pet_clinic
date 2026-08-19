from fastapi import FastAPI, HTTPException, Depends
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from models import Pet, Owner

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Pet clinic API is working"}


@app.post("/pets")
def create_pet(name: str, species: str, age: int, owner_id: int, db: Session = Depends(get_db)):

    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=400, detail="Owner with this id does not exist")

    pet = Pet(name=name, species=species, age=age, owner_id = owner_id)
    db.add(pet)
    db.commit()
    return {"id": pet.id, "name": pet.name, "species": pet.species, "age": pet.age, "owner_id": owner_id}


@app.get("/pets")
def list_pets(db: Session = Depends(get_db)):
    pets = db.query(Pet).all()
    return [{"id": p.id, "name": p.name, "species": p.species, "age": p.age, "owner_id": p.owner_id} for p in pets]


@app.get("/pets/{pet_id}")
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return {"id": pet.id, "name": pet.name, "species": pet.species, "age": pet.age, "owner_id": pet.owner_id}

@app.put("/pets/{pet_id}")
def update_pet(pet_id: int, name: str, species: str, age: int, owner_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail=f"Pet with {pet_id} id is not found")

    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=400, detail="Owner with this id does not exist")

    pet.name = name
    pet.species = species
    pet.age = age
    pet.owner_id = owner_id
    db.commit()

    return {"id": pet.id, "name": pet.name, "species": pet.species, "age": pet.age, "owner_id": pet.owner_id}


@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail=f"Pet with {pet_id} id is not found")

    db.delete(pet)
    db.commit()
    return "Pet Deleted"

@app.post("/owner")
def create_owner(name: str, phone: str, db: Session = Depends(get_db)):
    owner = Owner(name=name, phone=phone)
    db.add(owner)
    db.commit()
    return {"id": owner.id, "name": owner.name, "phone": owner.phone}

@app.get("/owner/{owner_id}")
def show_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=404, detail="Error, id is not found")
    return {"id": owner.id, "name": owner.name, "phone": owner.phone}

