from farm_cli.db.session import SessionLocal
from farm_cli.db.models import Feed

def feeds_menu():
    session = SessionLocal()

    while True:
        print("\n--- Feeds Menu ---")
        print("1. Add Feed")
        print("2. View All Feeds")
        print("3. Find by ID")
        print("4. Find by Name")
        print("5. Delete Feed")
        print("0. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                name = input("Enter feed name: ")
                unit = input("Enter unit (default=kg): ") or "kg"
                cost = float(input("Enter cost per unit: ") or 0)
                stock = float(input("Enter stock quantity: ") or 0)
                feed = Feed.create(session, name, unit, cost, stock)
                session.commit()
                print(f"✅ Feed added: {feed.id} - {feed.name}")
            except Exception as e:
                session.rollback()
                print("❌ Error:", e)

        elif choice == "2":
            feeds = Feed.get_all(session)
            if not feeds:
                print("No feeds found.")
            for f in feeds:
                print(f"[{f.id}] {f.name} | Stock: {f.stock_quantity}{f.unit}")

        elif choice == "3":
            id_ = input("Enter ID: ")
            feed = Feed.find_by_id(session, id_)
            print(feed if feed else "❌ Not found")

        elif choice == "4":
            name = input("Enter name: ")
            feed = Feed.find_by_name(session, name)
            print(feed if feed else "❌ Not found")

        elif choice == "5":
            id_ = input("Enter ID to delete: ")
            if Feed.delete_by_id(session, id_):
                session.commit()
                print("✅ Deleted")
            else:
                print("❌ Not found")

        elif choice == "0":
            break
        else:
            print("❌ Invalid choice")

    session.close()
