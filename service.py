from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Owner, Pet, User
from schemas import PetCreateDTO, PetUpdateDTO, OwnerCreateDTO, UserCreateDTO


def insert_pet(pet_data: PetCreateDTO, db: Session):
    owner = db.query(Owner).filter(Owner.id == pet_data.owner_id).first()
    if owner is None:
        raise HTTPException(status_code=400, detail="Owner with this id does not exist")
    pet = pet_data.to_pet()
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


def get_all_pets(db: Session):
    return db.query(Pet).all()


def get_pet_by_id(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


def modify_pet(pet_id: int, pet_data: PetUpdateDTO, db: Session):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail=f"Pet with {pet_id} id is not found")
    owner = db.query(Owner).filter(Owner.id == pet_data.owner_id).first()
    if owner is None:
        raise HTTPException(status_code=400, detail="Owner with this id does not exist")
    pet = pet_data.apply_to(pet)
    db.commit()
    return pet


def remove_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail=f"Pet with {pet_id} id is not found")
    db.delete(pet)
    db.commit()


def add_user(user_data: UserCreateDTO, db: Session):
    user = user_data.to_user()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def add_owner(owner_data: OwnerCreateDTO, db: Session):
    user = db.query(User).filter(User.id == owner_data.user_id).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User with this id does not exist")
    owner = owner_data.to_owner()
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return {"id": owner.id, "name": user.name, "phone": user.phone}


def get_owner(db: Session, owner_id: int):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=404, detail="Error, id is not found")
    return {"id": owner.id, "name": owner.user.name, "phone": owner.user.phone}