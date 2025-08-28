from farm_cli.commands.animals_menu import animals_menu
from farm_cli.commands.feeds_menu import feeds_menu
from farm_cli.db.session import init_db

MENU = {
    "1": ("Manage Animals", animals_menu),
    "2": ("Manage Feeds", feeds_menu),
    "0": ("Exit", None),
}

def main():
    # create DB/tables if not present
    init_db()

    while True:
        print("\n=== Farm CLI Main Menu ===")
        for k, (label, _) in MENU.items():
            print(f"{k}. {label}")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        entry = MENU.get(choice)
        if not entry:
            print("Invalid choice — try again.")
            continue
        _, func = entry
        func()

if __name__ == '__main__':
    main()