from faker import Faker
from service import add_owner, insert_pet
from database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)

fake = Faker()
db = SessionLocal()

pet_names = ["Barsik", "Reks", "Murka", "Tuzik", "Kuzys", "Snejok", "Drujok", "Pushok", "Charlie", "Laska"]
species_list = ["Cat", "Dog", "Rabbit", "Hamster", "Bird"]

owners = []
for i in range(10):
    owner = add_owner(db, fake.name(), fake.phone_number())
    owners.append(owner)


for y in range(20):
    random_owner = fake.random_element(owners)
    insert_pet(
        fake.random_int(min=1, max=15),
        db,
        fake.random_element(pet_names),
        random_owner.id,
        fake.random_element(species_list),
    )