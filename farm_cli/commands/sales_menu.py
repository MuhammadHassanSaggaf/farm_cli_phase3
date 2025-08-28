from farm_cli.db.session import get_session
from farm_cli.db.models import Sale
from farm_cli.banners import sales_banner

def sales_menu():
    sales_banner()
    while True:
        print("\n=== Sales Menu ===")
        print("1. Record Sale")
        print("2. List Sales")
        print("3. Find Sale by ID")
        print("4. Delete Sale")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            product = input("Product name: ")
            quantity = float(input("Quantity: "))
            unit_price = float(input("Unit Price: "))
            with get_session() as session:
                sale = Sale.create(session, product, quantity, unit_price)
                session.commit()
                print(f"✅ Recorded sale: {sale.product} for {sale.total_amount}")
        elif choice == "2":
            with get_session() as session:
                sales = Sale.get_all(session)
                for s in sales:
                    print(f"{s.id}: {s.product} - {s.quantity} @ {s.unit_price} = {s.total_amount} ({s.date})")
        elif choice == "3":
            id_ = int(input("Enter Sale ID: "))
            with get_session() as session:
                sale = Sale.find_by_id(session, id_)
                if sale:
                    print(f"Found: {sale.product} - {sale.quantity} @ {sale.unit_price} = {sale.total_amount}")
                else:
                    print("❌ Not found")
        elif choice == "4":
            id_ = int(input("Enter ID to delete: "))
            with get_session() as session:
                if Sale.delete_by_id(session, id_):
                    session.commit()
                    print("✅ Deleted")
                else:
                    print("❌ Not found")
        else:
            print("Invalid choice.")
