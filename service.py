from fastapi import HTTPException
from models import Owner, Pet


def insert_pet(age, db, name, owner_id, species):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=400, detail="Owner with this id does not exist")
    pet = Pet(name=name, species=species, age=age, owner_id=owner_id)
    db.add(pet)
    db.commit()
    return pet


def get_all_pets(db):
    pets = db.query(Pet).all()
    return pets


def get_pet_by_id(db, pet_id):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


def modify_pet(age, db, name, owner_id, pet_id, species):
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
    return pet


def remove_pet(db, pet_id):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail=f"Pet with {pet_id} id is not found")
    db.delete(pet)
    db.commit()


def add_owner(db, name, phone):
    owner = Owner(name=name, phone=phone)
    db.add(owner)
    db.commit()
    return owner


def get_owner(db, owner_id):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=404, detail="Error, id is not found")
    return owner
