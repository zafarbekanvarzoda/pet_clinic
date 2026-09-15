from pydantic import BaseModel, ConfigDict
from models import Pet, Owner, User, Vet
from pydantic_extra_types.phone_numbers import PhoneNumber

class PetCreateDTO(BaseModel):

    name: str
    species: str
    diagnosis: str
    age: int
    owner_id: int
    vet_id: int

    def to_pet(self) -> Pet:
        return Pet(name=self.name, species=self.species, diagnosis=self.diagnosis, age=self.age, owner_id=self.owner_id, vet_id=self.vet_id)


class PetUpdateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    species: str
    diagnosis: str
    age: int
    owner_id: int
    vet_id: int

    def apply_to(self, pet: Pet) -> Pet:
        pet.name = self.name
        pet.species = self.species
        pet.diagnosis = self.diagnosis
        pet.age = self.age
        pet.owner_id = self.owner_id
        pet.vet_id = self.vet_id
        return pet


class PetResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    species: str
    diagnosis: str
    age: int
    owner_id: int
    vet_id: int


class OwnerCreateDTO(BaseModel):
    user_id: int
    vet_ids: list[int]

    def to_owner(self) -> Owner:
        return Owner(user_id=self.user_id)

class VetShowDTO(BaseModel):
    id: int
    name: str

class OwnerResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: PhoneNumber
    vets: list[VetShowDTO]


class OwnerUpdateDTO(BaseModel):
    user_id: int
    vet_ids: list[int]

    def apply_to(self, owner: Owner) -> Owner:
        owner.user_id = self.user_id
        return owner

class UserCreateDTO(BaseModel):
    name: str
    phone: PhoneNumber
    address: str


    def to_user(self) -> User:
        return User(name=self.name, phone=self.phone, address=self.address.replace("\n", ", "))


class UserResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: PhoneNumber
    address: str

class UserUpdateDTO(BaseModel):
    name: str
    phone: PhoneNumber
    address: str

    def apply_to(self, user: User) -> User:
        user.name = self.name
        user.phone = self.phone
        user.address = self.address
        return user


class VetCreateDTO(BaseModel):
    name: str
    services: list[str]

    def to_vet(self) -> Vet:
        return Vet(name = self.name, services = ", ".join(self.services))

class VetResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    services: list[str]

class VetUpdateDTO(BaseModel):
    name: str
    services: list[str]

    def apply_to(self, vet: Vet) -> Vet:
        vet.name = self.name
        vet.services = ", ".join(self.services)
        return vet








# class ServiceCreateDTO(BaseModel):
#
#
# class ServiceResponseDTO(BaseModel):
