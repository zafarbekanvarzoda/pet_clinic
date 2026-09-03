from faker import Faker
from service import add_owner, insert_pet, add_user, add_vet
from schemas import UserCreateDTO, VetCreateDTO, OwnerCreateDTO, PetCreateDTO
from database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)

fake = Faker()
db = SessionLocal()

pet_names = ["Barsik", "Reks", "Murka", "Tuzik", "Kuzys", "Snejok", "Drujok", "Pushok", "Charlie", "Laska"]
species_list = ["Cat", "Dog", "Rabbit", "Hamster", "Bird"]
service_options = ["Vaccination", "Checkup", "Surgery", "Grooming", "Dental care"]
uz_prefixes = ["90", "91", "93", "94", "95", "97", "98", "99", "33", "88"]

def uz_phone():
    prefix = fake.random_element(uz_prefixes)
    rest = fake.numerify("### ## ##")
    return f"+998 {prefix} {rest}"

users = []
for i in range(1000):
    user_data = UserCreateDTO(name=fake.name(), phone=uz_phone())
    user = add_user(user_data, db)
    users.append(user)

# doktor yaratish
vets = []
for i in range(300):
    chosen_services = list(fake.random_elements(service_options, length=2, unique=True))
    vet_data = VetCreateDTO(name=fake.name(), services=chosen_services)
    vet = add_vet(vet_data, db)  #dict
    vets.append(vet)

# owner qilish (doktorga ulash)
owners = []
for user in users:
    chosen_vets = fake.random_elements(vets, length=2, unique=True)
    vet_ids = [v["id"] for v in chosen_vets]
    owner_data = OwnerCreateDTO(user_id=user.id, vet_ids=vet_ids)
    owner = add_owner(owner_data, db)  # also dictionary
    owners.append(owner)

# pet yaratish
for i in range(400):
    random_owner = fake.random_element(owners)
    random_vet = fake.random_element(vets)
    pet_data = PetCreateDTO(
        name=fake.random_element(pet_names),
        species=fake.random_element(species_list),
        age=fake.random_int(min=1, max=15),
        owner_id=random_owner["id"],
        vet_id=random_vet["id"],
    )
    insert_pet(pet_data, db)

db.close()