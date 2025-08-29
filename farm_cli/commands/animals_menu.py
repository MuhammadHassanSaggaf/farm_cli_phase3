# farm_cli/commands/animals_menu.py
from datetime import date
from farm_cli.db.session import SessionLocal
from farm_cli.db.models import Animal
from farm_cli.banners import animal_banner

def format_animal(a: Animal) -> str:
    if not a:
        return "❌ Not found."
    dob = a.dob.isoformat() if a.dob else "Unknown"
    breed = a.breed if a.breed else "Unknown"
    age = a.age if a.age is not None else "Unknown"
    return f"ID: {a.id} | Tag: {a.tag} | Species: {a.species} | Breed: {breed} | DOB: {dob} | Age: {age}"

def animals_menu():
    animal_banner()
    print("Welcome to the Animals Menu 🐄")
    session = SessionLocal()

    try:
        while True:
            print("\n--- Animals Menu ---")
            print("1. Add Animal")
            print("2. View All Animals")
            print("3. Find by ID")
            print("4. Find by Tag")
            print("5. Delete Animal")
            print("0. Back")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                try:
                    tag = input("Enter tag: ").strip()
                    species = input("Enter species: ").strip()
                    breed = input("Enter breed (optional): ").strip() or None
                    dob_input = input("Enter DOB (YYYY-MM-DD, optional): ").strip()
                    dob = date.fromisoformat(dob_input) if dob_input else None

                    animal = Animal.create(session, tag, species, breed, dob)
                    session.commit()
                    print(f"✅ Animal added: {format_animal(animal)}")
                except Exception as e:
                    session.rollback()
                    print("❌ Error adding animal:", e)

            elif choice == "2":
                animals = Animal.get_all(session)
                if not animals:
                    print("No animals found.")
                else:
                    print("\n--- All Animals ---")
                    for a in animals:
                        print(format_animal(a))

            elif choice == "3":
                id_input = input("Enter ID: ").strip()
                try:
                    id_ = int(id_input)
                except ValueError:
                    print("❌ Please enter a valid integer ID.")
                    continue
                animal = Animal.find_by_id(session, id_)
                print(format_animal(animal))

            elif choice == "4":
                tag = input("Enter tag: ").strip()
                if not tag:
                    print("❌ Tag cannot be empty.")
                    continue
                animal = Animal.find_by_tag(session, tag)
                print(format_animal(animal))

            elif choice == "5":
                id_input = input("Enter ID to delete: ").strip()
                try:
                    id_ = int(id_input)
                except ValueError:
                    print("❌ Please enter a valid integer ID.")
                    continue

                try:
                    deleted = Animal.delete_by_id(session, id_)
                    if deleted:
                        session.commit()
                        print("✅ Deleted.")
                    else:
                        print("❌ Not found.")
                except Exception as e:
                    session.rollback()
                    print("❌ Error deleting animal:", e)

            elif choice == "0":
                break
            else:
                print("❌ Invalid choice")

    finally:
        session.close()
