import sys
sys.path.insert(0, 'lib')


from lib.clear_screen import clear
from lib.main_game import MainGame
from lib.getch import _Getch
from copy import deepcopy

getch = _Getch()

# Create the object to start the game...
class GameMenu():
    
    # TODO: The section "Special" will be created...
    
    def __init__(self):
        
        # Start: Start the game from the beginning
        # Load: Load all game status
        # Exit: Leave game to desktop

        self.menu_selection = ["Start", "Load", "Exit"]
        self.selection_cursor = ">"
        self.selection_not_made = " "
        self.start_main_menu()

    # Check whether it will load the games or not.
    def start_main_menu(self):
        clear()
        # Set the position of cursor.
        cursor_value = 0
        
        # Deep copy the selection values
        # to allow arrow movements.
        tmp = deepcopy(self.menu_selection)

        # Initialize the start menu.
        for i in range(len(tmp)):
            if i == cursor_value:
                tmp[i] = self.selection_cursor + tmp[i]
            else:
                tmp[i] = self.selection_not_made + tmp[i]

        # Create the menu in accordance with player's input.
        while True:
            print("Main menu")
            print("\n".join(tmp))
            character = getch()
            tmp = deepcopy(self.menu_selection)

            # Temporary breaking point for testing program
            if character == b"\r" and cursor_value == 0:
                # Create 10x10 maps after creating maps.
                self.random_map = MainGame()
                
            # TODO: Allows to load the data.
            elif character == b"\r" and cursor_value == 1:
                self.random_map = MainGame(load_data = True)
            
            # Exit game.
            elif character == b"\r" and cursor_value == 2:
                break

            else:
                if character == "UP_KEY":
                    if cursor_value > 0:
                        cursor_value -= 1
                elif character == "DOWN_KEY":
                    if cursor_value < len(self.menu_selection) - 1:
                        cursor_value += 1

            for i in range(len(tmp)):
                
                if i == cursor_value:
                    tmp[i] = self.selection_cursor + tmp[i]
                
                else:
                    tmp[i] = self.selection_not_made + tmp[i]
            
            clear()
        clear()

class Menu(object):
    def __init__(self):
        pass

    # Draw menu.
    def draw_menu(self):
        pass

# TODO: Putting codes that allows player to move in the main program.
# Create first main game here.
def main():
    GameMenu()

if __name__ == '__main__':
    main()

