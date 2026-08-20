from fastapi import FastAPI, Depends
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from service import insert_pet, get_all_pets, get_pet_by_id, modify_pet, remove_pet, add_owner, get_owner

from schemas import PetCreateDTO, PetResponseDTO, PetUpdateDTO
from schemas import OwnerCreateDTO, OwnerResponseDTO

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
def create_pet(pet_data: PetCreateDTO, db: Session = Depends(get_db)):
    pet = insert_pet(pet_data.age, db, pet_data.name, pet_data.owner_id, pet_data.species)
    return {"id": pet.id}


@app.get("/pets", response_model=list[PetResponseDTO])
def list_pets(db: Session = Depends(get_db)):
    pets = get_all_pets(db)
    return pets


@app.get("/pets/{pet_id}", response_model=PetResponseDTO)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = get_pet_by_id(db, pet_id)
    return pet


@app.put("/pets/{pet_id}", response_model=PetResponseDTO)
def update_pet(pet_data: PetUpdateDTO, db: Session = Depends(get_db)):
    pet = modify_pet(pet_data.age, db, pet_data.name, pet_data.owner_id, pet_data.pet_id, pet_data.species)
    return pet


@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    remove_pet(db, pet_id)
    return "Pet Deleted"


@app.post("/owner", response_model=OwnerResponseDTO)
def create_owner(owner_data: OwnerCreateDTO, db: Session = Depends(get_db)):
    owner = add_owner(db, owner_data.name, owner_data.phone)
    return owner


@app.get("/owner/{owner_id}", response_model=OwnerResponseDTO)
def show_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = get_owner(db, owner_id)
    return owner


