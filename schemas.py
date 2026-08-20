from pydantic import BaseModel

class PetCreateDTO(BaseModel):
    name: str
    species: str
    age: int
    owner_id: int

class PetUpdateDTO(BaseModel):
    name: str
    species: str
    age: int
    owner_id: int



class PetResponseDTO(BaseModel):
    id: int
    name: str
    species: str
    age: int
    owner_id: int


class OwnerCreateDTO(BaseModel):
    name: str
    phone: str

class OwnerResponseDTO(BaseModel):
    id: int
    name: str
    phone: str

