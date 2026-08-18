from fastapi import FastAPI, HTTPException

app = FastAPI()


class Pet:
    def __init__(self, id, name, species, age):
        self.id = id
        self.name = name
        self.species = species
        self.age = age


pets = []


@app.get("/")
def read_root():
    return {"message": "Pet clinic API is working"}


@app.post("/pets")
def create_pet(name: str, species: str, age: int):
    new_id = len(pets) + 1
    pet = Pet(new_id, name, species, age)
    pets.append(pet)
    return {"id": pet.id, "name": pet.name, "species": pet.species, "age": pet.age}


@app.get("/pets")
def list_pets():
    return [{"id": p.id, "name": p.name, "species": p.species, "age": p.age} for p in pets]


@app.get("/pets/{pet_id}")
def get_pet(pet_id: int):
    for p in pets:
        if p.id == pet_id:
            return {"id": p.id, "name": p.name, "species": p.species, "age": p.age}
    raise HTTPException(status_code=404, detail="Pet not found")