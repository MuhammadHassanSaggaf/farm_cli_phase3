from farm_cli.commands.animals_menu import animals_menu
from farm_cli.commands.feeds_menu import feeds_menu
from farm_cli.db.session import init_db

MENU = {
    "1": ("Manage Animals", animals_menu),
    "2": ("Manage Feeds", feeds_menu),
    "0": ("Exit", None),
}

def welcome():
    print("🌱 Welcome to Farm CLI 🌱")
    name = input("Please enter your name, Farmer: ").strip()
    if not name:
        name = "Farmer"
    print(f"\nHello, {name}! 👩‍🌾👨‍🌾")
    print("Farm CLI helps you manage your farm by keeping track of animals, feeds, and more.")
    print("Use the menus to add, update, and view your farm records.\n")
    return name

def main():
    # Ensure database and tables exist
    init_db()

    farmer = welcome()

    while True:
        print("\n=== Main Menu ===")
        for k, (label, _) in MENU.items():
            print(f"{k}. {label}")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print(f"Goodbye, {farmer}! 👋")
            break

        entry = MENU.get(choice)
        if not entry:
            print("❌ Invalid choice — try again.")
            continue

        _, func = entry
        func()

if __name__ == "__main__":
    main()
