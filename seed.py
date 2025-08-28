# seed.py
import random
from datetime import date
from faker import Faker
from farm_cli.db.session import SessionLocal
from farm_cli.db.models import Animal, Feed, Inventory, Personnel, Sale

fake = Faker()
session = SessionLocal()

def seed_data():
    print("🌱 Seeding database...")

    # --- Seed Animals ---
    animals = []
    species_list = ["Cow", "Goat", "Chicken", "Sheep"]
    for _ in range(20):
        animal = Animal.create(
            session,
            tag=fake.unique.bothify(text='??###'),
            species=random.choice(species_list),
            breed=fake.word(),
            dob=fake.date_of_birth(minimum_age=1, maximum_age=10)
        )
        animals.append(animal)

    # --- Seed Feeds ---
    feeds = []
    feed_names = ["Corn", "Hay", "Soybean", "Barley", "Oats"]
    for name in feed_names:
        feed = Feed.create(
            session,
            name=name,
            unit='kg',
            cost_per_unit=round(random.uniform(0.5, 5), 2),
            stock_quantity=round(random.uniform(50, 500), 2)
        )
        feeds.append(feed)

    # --- Seed Inventory ---
    categories = ["Hardware", "Tools", "Supplies"]
    for _ in range(20):
        Inventory.create(
            session,
            name=fake.unique.word().capitalize(),
            category=random.choice(categories),
            quantity=random.randint(10, 100),
            unit='pcs'
        )

    # --- Seed Personnel ---
    roles = ["Farmer", "Caretaker", "Veterinarian", "Manager"]
    for _ in range(10):
        Personnel.create(
            session,
            name=fake.name(),
            role=random.choice(roles),
            salary=round(random.uniform(1000, 5000), 2)
        )

    # --- Seed Sales ---
    for _ in range(30):
        animal = random.choice(animals)
        price = round(random.uniform(50, 500), 2)
        Sale.create(
            session,
            animal=animal,
            price=price,
            date_=fake.date_between(start_date='-1y', end_date='today')
        )

    session.commit()
    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
    session.close()
