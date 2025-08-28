from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

def reset():
    return Style.RESET_ALL

# 🌟 Main Banner
def print_banner():
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
    █████╗   ██████╗ ██████╗ ██╗███╗   ███╗ █████╗ ████████╗███████╗
   ██╔══██╗ ██╔════╝██╔═══██╗██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
   ███████║ ██║     ██║   ██║██║██╔████╔██║███████║   ██║   █████╗  
   ██╔══██║ ██║     ██║   ██║██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝  
   ██║  ██║ ╚██████╗╚██████╔╝██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
   ╚═╝  ╚═╝  ╚═════╝ ╚═════╝ ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                                    
{Fore.YELLOW}{Style.BRIGHT}🌱 Your friendly farm management assistant 🌱
    """
    print(banner)

def welcome_farmer(name: str):
    print(f"{Fore.CYAN}{Style.BRIGHT}Welcome, {name}! 🌾 Let's grow together with AgriMate.\n")

# 🐄 Animals Menu
def animal_banner():
    print(Fore.GREEN + r"""
     __     _
    /  \~~~/ \
   (    . . )   🐄
    \__\_v_/__/
     ||     ||
    ==     ==
   Welcome to the Barn!
    """ + reset())

# 🌾 Feeds Menu
def feeds_banner():
    print(Fore.YELLOW + r"""
      |||||||
      |||||||   🌾
      |||||||
      |||||||
      |||||||
      |||||||
     =========
   Feed Storage Silo
    """ + reset())

# 🛠️ Inventory Menu
def inventory_banner():
    print(Fore.CYAN + r"""
     ______
    /      \__
   /  🛠️ Shed  \
  /__________/
   |  ||  || 
   |  ||  || 
   |__||__|| 
   Tool Storage Ready!
    """ + reset())

# 💰 Sales Menu
def sales_banner():
    print(Fore.MAGENTA + r"""
     _________
    /         \
   /  Market   \ 💰
  /_____________\
  |  |     |    |
  |__|_____|____|
   Farm Sales Hub
    """ + reset())

# 👥 Personnel Menu
def personnel_banner():
    print(Fore.BLUE + r"""
      /\ 
     /  \  🏡
    /____\ 
    |    |
    |👥  |
    |____|
   Farmhouse Office
    """ + reset())
