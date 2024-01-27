import os
import re
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colorful_intro(name):
    clear_terminal()
    print("\033[1;32m")  # Set text color to green
    
    print("**************************************************************")
    print("*                                                            *")
    print("*               Hi, I'm David, your Formula 1 Expert!        *")
    print("*                                                            *")
    print("**************************************************************")
    print("\033[0m")  # Reset text color
    
    # Print a simple ASCII art resembling the Formula 1 logo
    print("\033[1;33m")  # Set text color to yellow
    print("    _______  _______  _______  _______  _______  _______ ")
    print("   |       ||       ||       ||       ||       ||       |")
    print("   |    _  ||    _  ||   _   ||       ||   _   ||    ___|")
    print("   |   |_| ||   |_| ||  | |  ||       ||  | |  ||   |___ ")
    print("   |    ___||    ___||  |_|  ||      _||  |_|  ||    ___|")
    print("   |   |    |   |    |       ||     |_ |       ||   |___ ")
    print("   |___|    |___|    |_______||_______||_______||_______|")
    print("\033[0m")  # Reset text color
    
    # Print link
    print("\033[1;35m")  # Set text color to magenta
    print(name)
    print("\033[0m")  # Reset text color


def print_text_on_one_line(text):
    return re.sub(r'\s+', ' ', text.strip())
