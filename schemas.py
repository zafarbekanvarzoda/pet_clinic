from pydantic import BaseModel, ConfigDict
from models import Pet, Owner, User


class PetCreateDTO(BaseModel):
    name: str
    species: str
    age: int
    owner_id: int

    def to_pet(self) -> Pet:
        return Pet(name=self.name, species=self.species, age=self.age, owner_id=self.owner_id)


class PetUpdateDTO(BaseModel):
    name: str
    species: str
    age: int
    owner_id: int

    def apply_to(self, pet: Pet) -> Pet:
        pet.name = self.name
        pet.species = self.species
        pet.age = self.age
        pet.owner_id = self.owner_id
        return pet


class PetResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    species: str
    age: int
    owner_id: int




class OwnerCreateDTO(BaseModel):
    user_id: int

    def to_owner(self) -> Owner:
        return Owner(user_id=self.user_id)


class OwnerResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str




class UserCreateDTO(BaseModel):
    name: str
    phone: str

    def to_user(self) -> User:
        return User(name=self.name, phone=self.phone)


class UserResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str

