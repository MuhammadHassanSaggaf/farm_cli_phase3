from farm_cli.db.session import SessionLocal
from farm_cli.db.models import Feed
from farm_cli.banners import feeds_banner

def format_feed(f: Feed) -> str:
    if not f:
        return "❌ Not found."
    return f"ID: {f.id} | {f.name} | Unit: {f.unit} | Cost/unit: {f.cost_per_unit} | Stock: {f.stock_quantity}"

def feeds_menu():
    feeds_banner()
    print("Welcome to the Feeds Menu 🌾")
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
                name = input("Enter feed name: ").strip()
                unit = input("Enter unit (default=kg): ").strip() or "kg"
                cost = float(input("Enter cost per unit (default=0): ") or 0)
                stock = float(input("Enter stock quantity (default=0): ") or 0)
                feed = Feed.create(session, name, unit, cost, stock)
                session.commit()
                print(f"✅ Feed added: {format_feed(feed)}")
            except Exception as e:
                session.rollback()
                print("❌ Error:", e)

        elif choice == "2":
            feeds = Feed.get_all(session)
            if not feeds:
                print("No feeds found.")
            else:
                for f in feeds:
                    print(format_feed(f))

        elif choice == "3":
            id_ = input("Enter ID: ").strip()
            feed = Feed.find_by_id(session, int(id_))
            print(format_feed(feed))

        elif choice == "4":
            name = input("Enter name: ").strip()
            feed = Feed.find_by_name(session, name)
            print(format_feed(feed))

        elif choice == "5":
            id_ = input("Enter ID to delete: ").strip()
            deleted = Feed.delete_by_id(session, int(id_))
            if deleted:
                session.commit()
                print("✅ Deleted")
            else:
                print("❌ Not found")

        elif choice == "0":
            break
        else:
            print("❌ Invalid choice")

    session.close()
