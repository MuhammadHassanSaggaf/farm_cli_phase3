from datetime import date
from farm_cli.db.session import SessionLocal
from farm_cli.db.models import Animal
from farm_cli.banners import animal_banner

def animals_menu():
    animal_banner()
    print("Welcome to the Animals Menu 🐄")
    session = SessionLocal()

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
                tag = input("Enter tag: ")
                species = input("Enter species: ")
                breed = input("Enter breed (optional): ") or None
                dob_input = input("Enter DOB (YYYY-MM-DD, optional): ")
                dob = date.fromisoformat(dob_input) if dob_input else None
                animal = Animal.create(session, tag, species, breed, dob)
                session.commit()
                print(f"✅ Animal added: {animal.id} - {animal.tag}")
            except Exception as e:
                session.rollback()
                print("❌ Error:", e)

        elif choice == "2":
            animals = Animal.get_all(session)
            if not animals:
                print("No animals found.")
            for a in animals:
                print(f"[{a.id}] {a.tag} | {a.species} ({a.breed}) Age: {a.age}")

        elif choice == "3":
            id_ = input("Enter ID: ")
            animal = Animal.find_by_id(session, id_)
            print(animal if animal else "❌ Not found")

        elif choice == "4":
            tag = input("Enter tag: ")
            animal = Animal.find_by_tag(session, tag)
            print(animal if animal else "❌ Not found")

        elif choice == "5":
            id_ = input("Enter ID to delete: ")
            if Animal.delete_by_id(session, id_):
                session.commit()
                print("✅ Deleted")
            else:
                print("❌ Not found")

        elif choice == "0":
            break
        else:
            print("❌ Invalid choice")

    session.close()
