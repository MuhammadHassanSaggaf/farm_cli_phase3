#!/usr/bin/env python3

from colorama import Fore, Style, init

from farm_cli.banners import print_banner, welcome_farmer
from farm_cli.commands.animals_menu import animals_menu
from farm_cli.commands.feeds_menu import feeds_menu
from farm_cli.commands.inventory_menu import inventory_menu
from farm_cli.commands.sales_menu import sales_menu
from farm_cli.commands.personnel_menu import personnel_menu
from farm_cli.commands.feed_events_menu import feed_events_menu  # <-- new

init(autoreset=True)


def main_menu():
    print_banner()
    farmer_name = input(f"{Fore.CYAN}{Style.BRIGHT}👩‍🌾 Please enter your name: {Style.RESET_ALL}")
    welcome_farmer(farmer_name)

    while True:
        print(f"""
{Fore.GREEN}{Style.BRIGHT}Main Menu 🌱
1. Animals 🐄
2. Feeds 🌾
3. Feed Events 🥣 
4. Inventory 🛠️
5. Sales 💰
6. Personnel 👥
0. Exit 🚪
""")
        choice = input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")

        if choice == "1":
            animals_menu()
        elif choice == "2":
            feeds_menu()
        elif choice == "3":
            feed_events_menu() 
        elif choice == "4":
            inventory_menu()
        elif choice == "5":
            sales_menu()
        elif choice == "6":
            personnel_menu()
        elif choice == "0":
            print(f"{Fore.MAGENTA}Goodbye, happy farming! 🌻{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice, please try again!{Style.RESET_ALL}")


if __name__ == "__main__":
    main_menu()
