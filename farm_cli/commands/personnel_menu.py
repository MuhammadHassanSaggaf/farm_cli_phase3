from farm_cli.db.session import get_session
from farm_cli.db.models import Personnel
from farm_cli.banners import personnel_banner

def personnel_menu():
    personnel_banner()
    while True:
        print("\n=== Personnel Menu ===")
        print("1. Add Personnel")
        print("2. List Personnel")
        print("3. Find by ID")
        print("4. Delete Personnel")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            name = input("Name: ")
            role = input("Role: ")
            salary = float(input("Salary: "))
            with get_session() as session:
                worker = Personnel.create(session, name, role, salary)
                session.commit()
                print(f"✅ Added {worker.name} ({worker.role})")
        elif choice == "2":
            with get_session() as session:
                staff = Personnel.get_all(session)
                for p in staff:
                    print(f"{p.id}: {p.name} ({p.role}) - Salary: {p.salary}")
        elif choice == "3":
            id_ = int(input("Enter ID: "))
            with get_session() as session:
                p = Personnel.find_by_id(session, id_)
                if p:
                    print(f"Found: {p.name} ({p.role}) - Salary: {p.salary}")
                else:
                    print("❌ Not found")
        elif choice == "4":
            id_ = int(input("Enter ID to delete: "))
            with get_session() as session:
                if Personnel.delete_by_id(session, id_):
                    session.commit()
                    print("✅ Deleted")
                else:
                    print("❌ Not found")
        else:
            print("Invalid choice.")
