from datetime import datetime
from farm_cli.db.session import SessionLocal
from farm_cli.db.models import Animal, Feed, AnimalFeed
from farm_cli.banners import feed_events_banner

def feed_events_menu():
    feed_events_banner()
    print("Welcome to Feed Events Menu 🌱")
    session = SessionLocal()

    while True:
        print("\n--- Feed Events Menu ---")
        print("1. Record Feed Event")
        print("2. View Feed Events for Animal")
        print("3. View Feed Events for Feed")
        print("0. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                animal_id = int(input("Animal ID: "))
                feed_id = int(input("Feed ID: "))
                quantity = float(input("Quantity: "))
                date_input = input("Date (YYYY-MM-DD, optional): ")
                date_given = datetime.fromisoformat(date_input) if date_input else None

                animal = Animal.find_by_id(session, animal_id)
                feed = Feed.find_by_id(session, feed_id)

                if not animal or not feed:
                    print("❌ Invalid Animal or Feed ID")
                    continue

                event = AnimalFeed.create(session, animal, feed, quantity, date_given)
                session.commit()
                print(f"✅ Feed event recorded: {animal.tag} got {quantity} {feed.unit} of {feed.name}")
            except Exception as e:
                session.rollback()
                print("❌ Error:", e)

        elif choice == "2":
            animal_id = int(input("Animal ID: "))
            events = AnimalFeed.get_for_animal(session, animal_id)
            if not events:
                print("No feed events found.")
            for e in events:
                print(f"[{e.id}] {e.date_given.date()} - {e.quantity}{e.feed.unit} of {e.feed.name}")

        elif choice == "3":
            feed_id = int(input("Feed ID: "))
            events = AnimalFeed.get_for_feed(session, feed_id)
            if not events:
                print("No feed events found.")
            for e in events:
                print(f"[{e.id}] {e.date_given.date()} - {e.quantity}{e.feed.unit} to {e.animal.tag}")

        elif choice == "0":
            break
        else:
            print("❌ Invalid choice")

    session.close()
