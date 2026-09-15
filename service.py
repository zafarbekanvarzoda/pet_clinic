from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Owner, Pet, User, Vet
from schemas import (
    PetCreateDTO, PetUpdateDTO, OwnerCreateDTO, UserCreateDTO, UserUpdateDTO, VetCreateDTO,VetUpdateDTO,
    OwnerUpdateDTO,
)



def insert_pet(pet_data: PetCreateDTO, db: Session):
    owner = db.query(Owner).filter(Owner.id == pet_data.owner_id).first()
    if owner is None:
        raise HTTPException(status_code=400, detail="Owner with this id does not exist")

    vet = db.query(Vet).filter(Vet.id == pet_data.vet_id).first()
    if vet is None:
        raise HTTPException(status_code=400, detail="Vet with this id does not exist")
    pet = pet_data.to_pet()
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet

# ================================PET============================================
def get_all_pets(db: Session, skip, limit):
    return db.query(Pet).offset(skip).limit(limit).all()

def get_pets_by_species(db: Session):
    return (
        db.query(
            Pet.species,
            func.count(Pet.id)
        )
        .group_by(Pet.species)
        .all()
    )


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
    vet = db.query(Vet).filter(Vet.id == pet_data.vet_id).first()
    if vet is None:
        raise HTTPException(status_code=400, detail="Vet with this id does not exist")

    pet = pet_data.apply_to(pet)
    db.commit()
    return pet


def remove_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail=f"Pet with {pet_id} id is not found")
    db.delete(pet)
    db.commit()

# ================================PET END============================================

# ================================USER============================================
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

def get_all_users(db: Session):
    return db.query(User).all()


def modify_user(user_id: int, user_data: UserUpdateDTO, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_data.apply_to(user)
    db.commit()
    return user


def remove_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

# ================================USER END============================================

# =================================OWNER==============================================
def add_owner(owner_data: OwnerCreateDTO, db: Session):
    user = db.query(User).filter(User.id == owner_data.user_id).first()

    if user is None:
        raise HTTPException(status_code=400, detail="User with this id does not exist")

    vets = []
    for vet_id in owner_data.vet_ids:
        vet = db.query(Vet).filter(Vet.id == vet_id).first()
        if vet is None:
            raise HTTPException(status_code=400, detail=f"Vet with id {vet_id} does not exist")
        vets.append(vet)

    owner = owner_data.to_owner()
    owner.vets = vets
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return {"id": owner.id, "name": user.name, "phone": user.phone, "vets": [{"id": v.id, "name": v.name} for v in owner.vets]}


def get_owner(db: Session, owner_id: int):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=404, detail="Error, id is not found")
    return {"id": owner.id, "name": owner.user.name, "phone": owner.user.phone, "vets": [{"id": v.id, "name": v.name} for v in owner.vets]}

def get_all_owners(db: Session):
    owners = db.query(Owner).all()
    return [
        {"id": o.id, "name": o.user.name, "phone": o.user.phone, "vets": [{"id": v.id, "name": v.name} for v in o.vets]}
        for o in owners
    ]

def modify_owner(owner_id: int, owner_data: OwnerUpdateDTO, db: Session):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()

    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    user = db.query(User).filter(User.id == owner_data.user_id).first()

    if user is None:
        raise HTTPException(status_code=400, detail="User with this id does not exist")

    vets = []
    for vet_id in owner_data.vet_ids:
        vet = db.query(Vet).filter(Vet.id == vet_id).first()
        if vet is None:
            raise HTTPException(status_code=400, detail=f"Vet with id {vet_id} does not exist")
        vets.append(vet)

    owner = owner_data.apply_to(owner)
    owner.vets = vets
    db.commit()
    return {"id": owner.id, "name": user.name, "phone": user.phone, "vets": [{"id": v.id, "name": v.name} for v in owner.vets]}

def remove_owner(db: Session, owner_id: int):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    db.delete(owner)
    db.commit()



# ================================.OWNER END.============================================

# ===================================VET================================================
def add_vet(vet_data: VetCreateDTO, db: Session):
    vet = vet_data.to_vet()
    db.add(vet)
    db.commit()
    db.refresh(vet)
    return {"id": vet.id, "name": vet.name, "services": vet.services.split(", ")}

def get_vet(db: Session, vet_id: int):
    vet = db.query(Vet).filter(Vet.id == vet_id).first()
    if vet is None:
        raise HTTPException(status_code=404, detail="Vet is not found")
    return {"id": vet.id, "name": vet.name, "services": vet.services.split(", ")}

def get_all_vets(db: Session):
    vets = db.query(Vet).all()
    return [{"id": v.id, "name": v.name, "services": v.services.split(", ")} for v in vets]


def modify_vet(vet_id: int, vet_data: VetUpdateDTO, db: Session):
    vet = db.query(Vet).filter(Vet.id == vet_id).first()
    if vet is None:
        raise HTTPException(status_code=404, detail="Vet not found")
    vet = vet_data.apply_to(vet)
    db.commit()
    return {"id": vet.id, "name": vet.name, "services": vet.services.split(", ")}


def remove_vet(db: Session, vet_id: int):
    vet = db.query(Vet).filter(Vet.id == vet_id).first()
    if vet is None:
        raise HTTPException(status_code=404, detail="Vet not found")
    db.delete(vet)
    db.commit()

# ====================================VET END============================================