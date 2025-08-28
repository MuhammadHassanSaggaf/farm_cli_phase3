from farm_cli.db.session import get_session
from farm_cli.db.models import Inventory
from farm_cli.banners import inventory_banner


def inventory_menu():
    inventory_banner()
    while True:
        print("\n=== Inventory Menu ===")
        print("1. Add Inventory Item")
        print("2. List Inventory")
        print("3. Find Item by ID")
        print("4. Delete Item")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            name = input("Item name: ")
            category = input("Category: ")
            quantity = float(input("Quantity: "))
            unit = input("Unit (default=pcs): ") or "pcs"
            with get_session() as session:
                item = Inventory.create(session, name, category, quantity, unit)
                session.commit()
                print(f"✅ Added {item.name}")
        elif choice == "2":
            with get_session() as session:
                items = Inventory.get_all(session)
                for i in items:
                    print(f"{i.id}: {i.name} ({i.category}) - {i.quantity} {i.unit}")
        elif choice == "3":
            id_ = int(input("Enter ID: "))
            with get_session() as session:
                item = Inventory.find_by_id(session, id_)
                if item:
                    print(f"Found: {item.name} ({item.category}) - {item.quantity} {item.unit}")
                else:
                    print("❌ Not found")
        elif choice == "4":
            id_ = int(input("Enter ID to delete: "))
            with get_session() as session:
                if Inventory.delete_by_id(session, id_):
                    session.commit()
                    print("✅ Deleted")
                else:
                    print("❌ Not found")
        else:
            print("Invalid choice.")
