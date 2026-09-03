from fastapi import FastAPI, Depends
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from service import (
    insert_pet, get_all_pets, get_pet_by_id, modify_pet, remove_pet,
    add_owner, get_owner, add_user, get_user, add_vet, get_vet,
    get_all_vets, modify_vet, remove_vet, get_all_users, modify_user, remove_user,
    modify_owner, remove_owner, get_all_owners
)

from schemas import (
    PetCreateDTO, PetResponseDTO, PetUpdateDTO,
    OwnerCreateDTO, OwnerResponseDTO, UserCreateDTO, UserResponseDTO,
    VetCreateDTO, VetResponseDTO, VetUpdateDTO, UserUpdateDTO, OwnerUpdateDTO
)
from auth import verify_api_key

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

#======================================USER=========================================
@app.post("/users", status_code= 201 , response_model = UserResponseDTO, dependencies = [Depends(verify_api_key)])
def create_user(user_data: UserCreateDTO, db: Session = Depends(get_db)):
    return add_user(user_data, db)


@app.get("/users/{user_id}", response_model=UserResponseDTO, dependencies=[Depends(verify_api_key)])
def show_user(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

@app.get("/users", response_model=list[UserResponseDTO], dependencies=[Depends(verify_api_key)])
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@app.put("/users/{user_id}", response_model=UserResponseDTO, dependencies=[Depends(verify_api_key)])
def update_user(user_id: int, user_data: UserUpdateDTO, db: Session = Depends(get_db)):
    return modify_user(user_id, user_data, db)


@app.delete("/users/{user_id}", status_code = 204, dependencies=[Depends(verify_api_key)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    remove_user(db, user_id)
    return "User Deleted"


#======================================USER END=========================================

#======================================OWNER=========================================
@app.post("/owner", status_code = 201 , response_model=OwnerResponseDTO, dependencies=[Depends(verify_api_key)])
def create_owner(owner_data: OwnerCreateDTO, db: Session = Depends(get_db)):
    return add_owner(owner_data, db)


@app.get("/owner/{owner_id}", response_model=OwnerResponseDTO, dependencies=[Depends(verify_api_key)])
def show_owner(owner_id: int, db: Session = Depends(get_db)):
    return get_owner(db, owner_id)

@app.get("/owners", response_model=list[OwnerResponseDTO], dependencies=[Depends(verify_api_key)])
def list_owners(db: Session = Depends(get_db)):
    return get_all_owners(db)


@app.put("/owner/{owner_id}", response_model=OwnerResponseDTO, dependencies=[Depends(verify_api_key)])
def update_owner(owner_id: int, owner_data: OwnerUpdateDTO, db: Session = Depends(get_db)):
    return modify_owner(owner_id, owner_data, db)


@app.delete("/owner/{owner_id}", status_code = 204 ,dependencies=[Depends(verify_api_key)])
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    remove_owner(db, owner_id)
    return "Owner Deleted"


#======================================OWNER END=========================================


#======================================PET==============================================

@app.post("/pets", status_code = 201, response_model=PetResponseDTO, dependencies=[Depends(verify_api_key)])
def create_pet(pet_data: PetCreateDTO, db: Session = Depends(get_db)):
    return insert_pet(pet_data, db)


@app.get("/pets", response_model=list[PetResponseDTO], dependencies=[Depends(verify_api_key)])
def list_pets(db: Session = Depends(get_db)):
    return get_all_pets(db)


@app.get("/pets/{pet_id}", response_model=PetResponseDTO, dependencies=[Depends(verify_api_key)])
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    return get_pet_by_id(db, pet_id)


@app.put("/pets/{pet_id}", response_model=PetResponseDTO, dependencies=[Depends(verify_api_key)])
def update_pet(pet_id: int, pet_data: PetUpdateDTO, db: Session = Depends(get_db)):
    return modify_pet(pet_id, pet_data, db)


@app.delete("/pets/{pet_id}", status_code = 204, dependencies=[Depends(verify_api_key)])
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    remove_pet(db, pet_id)
    return "Pet Deleted"
#======================================PET END=========================================



#======================================VET=========================================

@app.post("/vets", status_code = 201, response_model=VetResponseDTO, dependencies=[Depends(verify_api_key)])
def create_vet(vet_data: VetCreateDTO, db: Session = Depends(get_db)):
    return add_vet(vet_data, db)



@app.get("/vets/{vet_id}", response_model=VetResponseDTO, dependencies=[Depends(verify_api_key)])
def show_vet(vet_id: int, db: Session = Depends(get_db)):
    return get_vet(db, vet_id)


@app.get("/vets", response_model=list[VetResponseDTO], dependencies=[Depends(verify_api_key)])
def list_vets(db: Session = Depends(get_db)):
    return get_all_vets(db)


@app.put("/vets/{vet_id}", response_model=VetResponseDTO, dependencies=[Depends(verify_api_key)])
def update_vet(vet_id: int, vet_data: VetUpdateDTO, db: Session = Depends(get_db)):
    return modify_vet(vet_id, vet_data, db)


@app.delete("/vets/{vet_id}", status_code = 204, dependencies = [Depends(verify_api_key)])
def delete_vet(vet_id: int, db: Session = Depends(get_db)):
    remove_vet(db, vet_id)
    return "Vet Deleted"

#======================================VET END=========================================
