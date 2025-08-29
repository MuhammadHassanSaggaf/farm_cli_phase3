#!/usr/bin/env python3
"""
seed.py - populate the AgriMate database with sample data using the provided models.

Places created:
- Animals
- Feeds (with good stock)
- Inventory items
- Personnel
- Animal feed events (reduces feed stock)
- Sales (some linked to animals)

Adjust the COUNT_* constants below to increase/decrease dataset size.
"""

import random
from datetime import timedelta
from faker import Faker

# Try to import engine and SessionLocal; be tolerant if module names differ slightly.
try:
    from farm_cli.db.session import SessionLocal, engine
except Exception:
    # Fallback: try sessions (older names), or only SessionLocal if available
    try:
        from farm_cli.db.session import SessionLocal, engine
    except Exception:
        from farm_cli.db.session import SessionLocal  # may raise if not found
        engine = None

# Import models
from farm_cli.db.models import (
    Base,
    Animal,
    Feed,
    Inventory,
    Personnel,
    AnimalFeed,
    Sale,
)

fake = Faker()

# --- Config: how much data to create ---
COUNT_ANIMALS = 80
COUNT_FEEDS = 12
COUNT_INVENTORY = 40
COUNT_PERSONNEL = 15
COUNT_FEED_EVENTS = 160
COUNT_SALES = 120

def ensure_tables():
    """Create tables if engine available. If engine missing, skip and hope migrations/tables exist."""
    if 'engine' in globals() and engine is not None:
        print("Ensuring tables exist (Base.metadata.create_all)...")
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            print("Warning: create_all failed:", e)
    else:
        print("Engine not available — assuming tables already exist (Alembic-managed).")

def clear_existing(session):
    """Optional: clear previous data so seeding is idempotent for development."""
    print("Clearing existing rows (Sale, AnimalFeed, Inventory, Feed, Animal, Personnel) ...")
    try:
        # delete in order respecting FKs
        session.query(AnimalFeed).delete()
        session.query(Sale).delete()
        session.query(Inventory).delete()
        session.query(Feed).delete()
        session.query(Animal).delete()
        session.query(Personnel).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        print("Warning: clearing existing data failed (continuing):", e)

def seed_animals(session):
    print(f"Seeding {COUNT_ANIMALS} animals...")
    species_list = {
        "Cow": ["Friesian", "Holstein", "Jersey"],
        "Goat": ["Boer", "Kiko", "Saanen"],
        "Chicken": ["Broiler", "Layer", "Silkie"],
        "Sheep": ["Dorper", "Merino", "Suffolk"]
    }
    animals = []
    for _ in range(COUNT_ANIMALS):
        species = random.choice(list(species_list.keys()))
        breed = random.choice(species_list[species])
        dob = fake.date_of_birth(minimum_age=1, maximum_age=10)
        tag = fake.unique.bothify(text='TAG-####')
        try:
            a = Animal.create(session, tag=tag, species=species, breed=breed, dob=dob)
            animals.append(a)
        except Exception as e:
            session.rollback()
            print("Failed to create animal:", e)
    session.commit()
    print("Animals seeded:", len(animals))
    return animals

def seed_feeds(session):
    print(f"Seeding {COUNT_FEEDS} feed types with healthy stock...")
    feed_types = ["Hay", "Silage", "Grain Mix", "Pellets", "Vegetables", "Maize", "Soy", "Barley"]
    feeds = []
    for i in range(COUNT_FEEDS):
        name = f"{random.choice(feed_types)}-{fake.word().capitalize()}"
        unit = random.choice(["kg", "bale", "bag"])
        cost_per_unit = round(random.uniform(0.5, 10.0), 2)
        # give large initial stock so many feed events can be created
        stock_quantity = random.randint(300, 2000)
        try:
            f = Feed.create(session, name=name, unit=unit, cost_per_unit=cost_per_unit, stock_quantity=stock_quantity)
            feeds.append(f)
        except Exception as e:
            session.rollback()
            print("Failed to create feed:", e)
    session.commit()
    print("Feeds seeded:", len(feeds))
    return feeds

def seed_inventory(session):
    print(f"Seeding {COUNT_INVENTORY} inventory items...")
    categories = ["Hardware", "Equipment", "Medicine", "Supplies"]
    items = []
    for _ in range(COUNT_INVENTORY):
        try:
            it = Inventory.create(
                session,
                name=fake.unique.word().capitalize(),
                category=random.choice(categories),
                quantity=random.randint(1, 200),
                unit=random.choice(["pcs", "boxes", "kg"])
            )
            items.append(it)
        except Exception as e:
            session.rollback()
            print("Failed to create inventory item:", e)
    session.commit()
    print("Inventory seeded:", len(items))
    return items

def seed_personnel(session):
    print(f"Seeding {COUNT_PERSONNEL} personnel...")
    roles = ["Farmer", "Caretaker", "Veterinarian", "Manager", "Driver"]
    staff = []
    for _ in range(COUNT_PERSONNEL):
        try:
            p = Personnel.create(
                session,
                name=fake.name(),
                role=random.choice(roles),
                salary=round(random.uniform(300.0, 2500.0), 2)
            )
            staff.append(p)
        except Exception as e:
            session.rollback()
            print("Failed to create personnel:", e)
    session.commit()
    print("Personnel seeded:", len(staff))
    return staff

def seed_feed_events(session, animals, feeds):
    print(f"Seeding up to {COUNT_FEED_EVENTS} animal feed events (will skip events if feed stock insufficient).")
    created = 0
    for _ in range(COUNT_FEED_EVENTS):
        animal = random.choice(animals)
        feed = random.choice(feeds)
        qty = round(random.uniform(1.0, 20.0), 2)
        try:
            # ensure feed has enough stock before trying
            if feed.stock_quantity >= qty:
                # AnimalFeed.create adjusts feed.stock_quantity internally
                AnimalFeed.create(session, animal=animal, feed=feed, quantity=qty)
                created += 1
            else:
                # try another feed with sufficient stock (simple attempt)
                # pick a feed that has enough stock
                candidates = [f for f in feeds if f.stock_quantity >= qty]
                if candidates:
                    f2 = random.choice(candidates)
                    AnimalFeed.create(session, animal=animal, feed=f2, quantity=qty)
                    created += 1
                else:
                    # no feed currently has sufficient stock — skip
                    continue
        except Exception as e:
            session.rollback()
            # print message and continue
            print("Skipped feed event (reason):", e)
    session.commit()
    print("Feed events created:", created)

def seed_sales(session, animals, feeds):
    print(f"Seeding {COUNT_SALES} sales (mix of product sales and animal-linked sales)...")
    created = 0
    for _ in range(COUNT_SALES):
        # sometimes sell an animal, sometimes sell feed/inventory product
        if random.random() < 0.35 and animals:
            # animal sale: product = animal.species, link animal
            animal = random.choice(animals)
            product = f"{animal.species}"
            quantity = 1  # selling animals usually in whole units
            unit_price = round(random.uniform(200.0, 2000.0), 2)
            try:
                Sale.create(session, product=product, quantity=quantity, unit_price=unit_price, animal=animal, date_=fake.date_between(start_date='-1y', end_date='today'))
                created += 1
            except Exception as e:
                session.rollback()
                print("Failed to create animal sale:", e)
        else:
            # non-animal product sale (e.g., feed or inventory)
            # pick feed or inventory name as product
            if random.random() < 0.6 and feeds:
                product_obj = random.choice(feeds)
                product_name = product_obj.name
            else:
                # fallback product name
                product_name = fake.word().capitalize()
            quantity = round(random.uniform(1.0, 100.0), 2)
            unit_price = round(random.uniform(1.0, 100.0), 2)
            try:
                Sale.create(session, product=product_name, quantity=quantity, unit_price=unit_price, animal=None, date_=fake.date_between(start_date='-1y', end_date='today'))
                created += 1
            except Exception as e:
                session.rollback()
                print("Failed to create non-animal sale:", e)
    session.commit()
    print("Sales created:", created)

def seed():
    ensure_tables()
    session = SessionLocal()

    # Optional: clear existing data (uncomment if you want a clean start)
    # clear_existing(session)

    animals = seed_animals(session)
    feeds = seed_feeds(session)
    seed_inventory(session)
    seed_personnel(session)

    # refresh animals/feeds from DB objects (some create implementations return detached or unrefreshed objects)
    animals = session.query(Animal).all()
    feeds = session.query(Feed).all()

    # feed events will consume feed stock (to make data realistic)
    seed_feed_events(session, animals, feeds)

    # sales (some linked to animals, some product sales)
    seed_sales(session, animals, feeds)

    session.close()
    print("✅ Seeding complete.")

if __name__ == "__main__":
    seed()
