from fastapi import FastAPI, Depends
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from service import (
    insert_pet, get_all_pets, get_pet_by_id, modify_pet, remove_pet,
    add_owner, get_owner, add_user, get_user,
)
from schemas import (
    PetCreateDTO, PetResponseDTO, PetUpdateDTO,
    OwnerCreateDTO, OwnerResponseDTO, UserCreateDTO, UserResponseDTO,
)

from auth import verify_create_api_key, verify_read_api_key, verify_update_api_key, verify_delete_api_key

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


@app.post("/users", response_model=UserResponseDTO, dependencies=[Depends(verify_create_api_key)])
def create_user(user_data: UserCreateDTO, db: Session = Depends(get_db)):
    return add_user(user_data, db)


@app.get("/users/{user_id}", response_model=UserResponseDTO, dependencies=[Depends(verify_read_api_key)])
def show_user(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)


@app.post("/owner", response_model=OwnerResponseDTO, dependencies=[Depends(verify_create_api_key)])
def create_owner(owner_data: OwnerCreateDTO, db: Session = Depends(get_db)):
    return add_owner(owner_data, db)


@app.get("/owner/{owner_id}", response_model=OwnerResponseDTO, dependencies=[Depends(verify_read_api_key)])
def show_owner(owner_id: int, db: Session = Depends(get_db)):
    return get_owner(db, owner_id)


@app.post("/pets", response_model=PetResponseDTO, dependencies=[Depends(verify_create_api_key)])
def create_pet(pet_data: PetCreateDTO, db: Session = Depends(get_db)):
    return insert_pet(pet_data, db)


@app.get("/pets", response_model=list[PetResponseDTO], dependencies=[Depends(verify_read_api_key)])
def list_pets(db: Session = Depends(get_db)):
    return get_all_pets(db)


@app.get("/pets/{pet_id}", response_model=PetResponseDTO, dependencies=[Depends(verify_read_api_key)])
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    return get_pet_by_id(db, pet_id)


@app.put("/pets/{pet_id}", response_model=PetResponseDTO, dependencies=[Depends(verify_update_api_key)])
def update_pet(pet_id: int, pet_data: PetUpdateDTO, db: Session = Depends(get_db)):
    return modify_pet(pet_id, pet_data, db)


@app.delete("/pets/{pet_id}", dependencies=[Depends(verify_delete_api_key)])
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    remove_pet(db, pet_id)
    return "Pet Deleted"


