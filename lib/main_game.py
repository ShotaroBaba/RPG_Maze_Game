# Reading all necessary packages
import sys
sys.path.insert(0, 'lib/maze_generation.py')

import os
import json 
from copy import deepcopy
from random import shuffle
from random import randint
from random import choice
from random import uniform
from getch import _Getch
from clear_screen import clear
from maze_generation import generate_maze_grid, make_maze_grid
from random import random
from maze_object import MazeObject
from default_values import *
from item import *

# The value which determine the difficulty of level increase.
constant_next_level_exp = 1.4
default_amount_to_reveal = 3
# Load creatures.
creature_file_path = os.path.join(data_dir,creature_data_file_name)
enemy_json = json.loads(open(creature_file_path, "r").read())

# Reads item data for creating the objects.
# Note: the object will not be create unless it is 
# the temporary effective items.
item_data_file_path = os.path.join(data_dir, item_data_file_name)
item_json = json.loads(open(item_data_file_path, "r").read())

# Set the colors of characters in the terminal.
os.system("color 0") 
getch = _Getch()

# Initialize and set directions
direction = {"N": (0,-1), "S":(0,1),"E":(1,0), "W":(-1,0)}

# Set the directions to create...
arrow_key_to_directions = {"UP_KEY": "N", "DOWN_KEY": "S", "RIGHT_KEY": "E", "LEFT_KEY": "W"}

# Enemy encounter probability is calculated based on the luckiness.
default_ememy_encounter = 0.2
min_enemy_encounter = 0.1

numerical_player_strengh = ["hp", "mp", "sp", "ep"]
current_status_player = ["current_hp", "current_mp", "current_sp", "current_ep", "level"]

non_numerical_player_strength = ["strength", "agility", "vitality", "dexterity",
                                 "smartness", "magic_power", "mental_strength", "luckiness"]   

string_numerical_player_strength = ["player_name", "is_living", "is_player", 
                                    "is_enemy", "head", "arm", "leg", "body_armor","right_wrist", "left_wrist", 
                                    "right_finger", "left_finger", "status", "displayed_character",
                                    "max_item_hold", "exp", "current_exp", "bonus_point", "next_exp", "items",
                                    "skills", "rank", "drop_item"]

# These parameters will not be selected in the selection menu.
non_selected_parameters = ["current_exp","next_exp","level","current_hp", 
                                   "current_mp", "current_sp", "current_ep"]
        

# TODO: Create methods for saving and loading game.


# The map for players to walk at the beginning
# TODO: Change Map name to a proper name

# TODO: Differentiate the apprearance of the items based on the level.
def random_item_selection(level = 1):
    return choice(list(item_json.keys()))

class MainGame(object):

    # When initialised, Map object puts players and item boxes at the
    # places.

    # When loading the game the game will
    # loaded_map: map to be loaded.
    # loaded_player: player data to be loaded.
    def __init__(self, load_data = False):
        
        # Amount to reveal.
        self.default_amount_to_reveal = default_amount_to_reveal

        self.width = width
        self.height = height
        

        # Set the symbols below this line:
        self.goal_symbol = "\033[93m" + "G" + "\033[0m"
        self.treasure_symbol = "\033[36m" + "T" + "\033[0m"

        # Putting player object first
        # Test purpose for putting player.
        if load_data:
            self.load_data()
            self.map_grid = deepcopy(self.original_map_grid)
            self.map_grid[self.player.object_pos[0]][self.player.object_pos[1]] = self.player.displayed_character
        else:
            self.player = MazeObject()
            self.level = 1
            self._initialize_map()

        clear()

        # Reveal map grid from the center of the player.
        

        self._draw_hidden_map()
        
        self._manipulate_map()

    def _exit_game(self):
        clear()
        
        selection_list = ["Yes", "No"]
        cursor_not_selected = " "
        cursor_selected = ">"
        tmp_cursor = deepcopy(selection_list)
        cursor_selection = 1
        
        while True:

            self._draw_hidden_map()
            for i in range(len(tmp_cursor)):
                if i == cursor_selection:
                    tmp_cursor[i] = cursor_selected + tmp_cursor[i]
                else:
                    tmp_cursor[i] = cursor_not_selected + tmp_cursor[i]

            print("Will you exit the game?")
            print("".join(tmp_cursor))
            tmp_cursor = deepcopy(selection_list)
            tmp = getch()
            if tmp == "LEFT_KEY":
                if cursor_selection > 0:
                        cursor_selection -= 1
                
            elif tmp == "RIGHT_KEY":
                if cursor_selection < len(tmp_cursor) - 1:
                        cursor_selection += 1

            elif tmp == b"\r":
                # Yes case --> Initialise map.
                if cursor_selection == 0:
                    return True
                
                # No case --> Do nothing.
                if cursor_selection == 1:
                    return False
            clear()
        clear()

    def _manipulate_map(self):
        while True:
            character = getch()
            
            # This condition will be removed later.
            if character == b"n":
                if self._exit_game():
                    break
            else:
                if character in ["UP_KEY", "DOWN_KEY", "LEFT_KEY", "RIGHT_KEY"]:
                    if self._move_player(character):
                        break

                elif character == b"\x1b":
                    self.player_menu()
            

    # Turn-based fight is now imminent
    # TODO: Enable the random appearance of the enemy based on the depth of the level.
    # TODO: Enable to fight several enemies.

    # TODO: Create class for fight screen.
    # It will become too long and complicated if it hasn't done.
    # enemy_fight will handle the map object..
    def _enemy_fight(self):
        
        # Create selection screen
        selection_list = ["Fight", "Skills", "Item","Status", "Escape"]
        cursor_not_selected = " "
        cursor_selected = ">"
        tmp_cursor = deepcopy(selection_list)
        cursor_selection = 0
        
        enemy_list = [enemy for enemy in enemy_json.keys() if enemy_json[enemy]["level"] - self.level <= 0]

        random_enemy = choice(list(enemy_list))
        enemy = MazeObject(json_data = enemy_json[random_enemy], level = self.level, is_random= "yes")

        # TODO: Take player's luckiness into account.
        def _player_turn_normal_attack():
            # Player turn
            player_base_attack_value = self.player.strength
            player_attack_value = int(round(uniform(0.8,1.0) * player_base_attack_value, 0))
            enemy.current_hp -= player_attack_value
            
            if enemy.current_hp < 1:
                print("You defeated the creature!")
                print("Player acquire {} exp".format(enemy.exp))
                print("Press any key to return to map...")
                self.player._get_experience(enemy.exp)
                
                # If it is bigger, then the enemy will drop the 
                if uniform(0,1.0) > 0.8 - (0.8 / (100 / (self.player.luckiness ** 0.70))):
                    print("Enemy dropped item!")
                    print("The content of the item is {}".format(enemy.drop_item))
                    self.player.items.append(enemy.drop_item)
                
                getch()
                clear()
                return True
            else:
                print("Player delivers {} damage".format(player_attack_value))
                getch()
                return False

        def _enemy_turn_normal_attack():
            # Enemy turn
            enemy_base_attack_value = enemy.strength
            enemy_attack_value = int(round(uniform(0.8,1.0) * enemy_base_attack_value, 0))
            self.player.current_hp -= enemy_attack_value
            
            if self.player.current_hp < 1:
                print("You are defeated...")
                print("Game Over...")
                getch()
                clear()
                return True

            else:
                print("Enemy delivers {} damage".format(enemy_attack_value))
                getch()
                return False


        # Displayed for generating 
        while True:

            for i in range(len(tmp_cursor)):
                if i == cursor_selection:
                    tmp_cursor[i] = cursor_selected + tmp_cursor[i]
                else:
                    tmp_cursor[i] = cursor_not_selected + tmp_cursor[i]

            print("{} appears!".format(random_enemy))
            self._display_status()
            print("\n".join(tmp_cursor))
            tmp_cursor = deepcopy(selection_list)
            tmp = getch()

            if tmp == "UP_KEY":
                if cursor_selection > 0:
                        cursor_selection -= 1
                
            elif tmp == "DOWN_KEY":
                if cursor_selection < len(tmp_cursor) - 1:
                        cursor_selection += 1

            elif tmp == b"\r":

                # Normally attack the enemy.
                if cursor_selection == 0:

                    # Turn based fight. The player can firstly fight for the enemy this value is higher.
                    if uniform(0.8, 1.0)*self.player.agility > uniform(0.8,1.0)* enemy.agility:
                        if _player_turn_normal_attack():
                            break
                        if _enemy_turn_normal_attack():
                            return True

                    else:
                        if _enemy_turn_normal_attack():
                            return True
                        if _player_turn_normal_attack():
                            break
                    
                # TODO: Create the function that handles player's skills.
                # Displays the player's status.
                elif cursor_selection == 1:    
                    print("This feature will be implemented later...")
                    getch()
                    clear()

                # Escape from the enemy.
                # The rate of the escape depends on the values of
                # the success.
                elif cursor_selection == 2:            
                    print("This feature will be implemented later...")
                    getch()
                    clear()
                    break

                elif cursor_selection == 3:
                    print("This feature will be implemented later...")
                    getch()
                    clear()
                    break
            clear()

    # TODO: The encounter percentage must be changed
    # Take the luck of the player into account.
    def _enemy_encounter(self, player_luck_value):
        k = random()

        # TODO: Make the possibility calculation possible...
        tmp = max(default_ememy_encounter, min_enemy_encounter)

        # Create the object instead of calling function...
        if 0 < k and k < tmp:
            return self._enemy_fight()

    def _initialize_map(self):
        self.map_grid = generate_maze_grid(make_maze_grid(self.width,self.height))

        # Randomly place objects, including goals and treasure boxes.
        self._randomly_place_objects(self.goal_symbol)
        
        # Randomly place treasure.
        for _ in range(randint(0,10)):
            self._randomly_place_objects(self.treasure_symbol)
        
        self.original_map_grid = deepcopy(self.map_grid)

        # TODO: Create and show the hidden map grid.
        self.hidden_map_grid = [["." for _ in range(len(self.map_grid))] for _ in range(len(self.map_grid[0]))]
       
        self.direction = direction
        
        # Randomly place goal
        self._randomly_place_player(self.player)

    
    # Reveal the grid of the map based on the player's location.
    def _reveal_map_grid(self):

        for i in range(max(0, self.player.object_pos[0] - self.default_amount_to_reveal),\
            min(self.player.object_pos[0] + self.default_amount_to_reveal, len(self.map_grid[0]))):
            for j in range(max(0, self.player.object_pos[1] - self.default_amount_to_reveal),\
                min(self.player.object_pos[1] + self.default_amount_to_reveal, len(self.map_grid))):
                # Find Reveal the maps.
                    self.hidden_map_grid[i][j] = self.map_grid[i][j]

    def _move_player_sub(self,str_direction, next_player_pos):
        # Initialize map using originally created random map.
        self.map_grid = deepcopy(self.original_map_grid)

        # Place player on the map based on the move player made.
        self.map_grid[next_player_pos[0]][next_player_pos[1]] = self.player.displayed_character

        # Update player position.
        self.player.object_pos = next_player_pos
        
        self.player.current_ep = max(self.player.current_ep - 1, 0)

        # if the current ep is zero. the current hp will decreases.
        if self.player.current_ep == 0:
            self.player.current_hp = max(self.player.current_hp - 1, 1)

    # Allows the users to select whether they will proceed to the next floor...
    def _map_proceed_selection(self):
        clear()
        
        selection_list = ["Yes", "No"]
        cursor_not_selected = " "
        cursor_selected = ">"
        tmp_cursor = deepcopy(selection_list)
        cursor_selection = 1
        
        while True:

            self._draw_hidden_map()
            for i in range(len(tmp_cursor)):
                if i == cursor_selection:
                    tmp_cursor[i] = cursor_selected + tmp_cursor[i]
                else:
                    tmp_cursor[i] = cursor_not_selected + tmp_cursor[i]

            print("Will you proceed to the next level?")
            print("".join(tmp_cursor))

            tmp_cursor = deepcopy(selection_list)
            tmp = getch()
            if tmp == "LEFT_KEY":
                if cursor_selection > 0:
                        cursor_selection -= 1
                
            elif tmp == "RIGHT_KEY":
                if cursor_selection < len(tmp_cursor) - 1:
                        cursor_selection += 1

            elif tmp == b"\r":
                # Yes case --> Initialise map.
                if cursor_selection == 0:
                    
                    self._initialize_map()
                    self.level += 1
                    break
                
                # No case --> Do nothing.
                if cursor_selection == 1:
                    break
            clear()


    def _display_status(self):
        print("HP: {}, MP: {}, SP: {}, EP: {}".format(self.player.current_hp, 
        self.player.current_mp,
        self.player.current_sp, 
        self.player.current_ep))
    

    def player_menu(self):
        clear()
        
        # There is no load function until player moves to exit.
        selection_list = ["Item", "Save","Status", "Exit"]
        cursor_not_selected = " "
        cursor_selected = ">"
        tmp_cursor = deepcopy(selection_list)
        cursor_selection = 0
        
        while True:
            for i in range(len(tmp_cursor)):
                if i == cursor_selection:
                    tmp_cursor[i] = cursor_selected + tmp_cursor[i]
                else:
                    tmp_cursor[i] = cursor_not_selected + tmp_cursor[i]
            print("Player Menu")
            print("\n".join(tmp_cursor))

            tmp_cursor = deepcopy(selection_list)
            tmp = getch()
            
            if tmp == "UP_KEY":
                if cursor_selection > 0:
                    cursor_selection -= 1
                
            elif tmp == "DOWN_KEY":
                if cursor_selection < len(tmp_cursor) - 1:
                    cursor_selection += 1

            elif tmp == b"\r":

                if cursor_selection == 0:
                    self._display_item()

                if cursor_selection == 1:
                    self.save_data()
                
                # Displaying player's status, allowing users to
                # improve status using bonus points.
                if cursor_selection == 2:
                    self._display_player_status()

                if cursor_selection == 3:
                    clear()
                    self._draw_hidden_map()
                    break

                clear()

            elif tmp == b"\x1b":
                clear()
                self._draw_hidden_map()
                break

            clear()
    
    def _display_player_status(self):

        exit_to_player_menu = ["Exit"]

        section_selected = ">"
        section_non_selected = " "
        selection_idx = 0
        selection_str_list = numerical_player_strengh + non_numerical_player_strength + exit_to_player_menu
        clear()

        while True:
            
            tmp = deepcopy(selection_str_list)
            menu_length = len(tmp)
            for i in range(menu_length):
                if i < menu_length -1:
                    if selection_idx  == i:
                        tmp[i] = section_selected + tmp[i] + ": "+ str(eval("self.player.{}".format(tmp[i])))
                    else:
                        tmp[i] = section_non_selected + tmp[i] + ": "+ str(eval("self.player.{}".format(tmp[i])))
                else:
                    if selection_idx  == i:
                        tmp[i] = section_selected + tmp[i]
                    else:
                        tmp[i] = section_non_selected + tmp[i]
            
            print("Status Menu")
            print("="*30)
            print("\n".join(tmp))
            print("="*30)
            print("Bonus point: {}".format(self.player.bonus_point))
            
            tmp = []
            for i in non_selected_parameters[:3]:
                tmp.append("{0}: {1}".format(i, eval("self.player.{0}".format(i))))
        
            print(" ".join(tmp))
            
            tmp = []
            for i in non_selected_parameters[3:]:
                tmp.append("{0}: {1}".format(i, eval("self.player.{0}".format(i))))
                
            print(" ".join(tmp))
            ch = getch()

            if ch == b'\r':
                
                if selection_idx < 3 and self.player.bonus_point > 0:
                    exec("self.player.{} += 5".format(selection_str_list[selection_idx]))
                    self.player.bonus_point -= 1
                elif selection_idx >= 3 and selection_idx < menu_length - 1 and self.player.bonus_point > 0:
                    exec("self.player.{} += 1".format(selection_str_list[selection_idx]))
                    self.player.bonus_point -= 1

                elif selection_idx == menu_length - 1:
                    break
            
            elif ch == "UP_KEY":
                if selection_idx > 0:
                    selection_idx -= 1
                
            elif ch == "DOWN_KEY":
                if selection_idx < menu_length - 1:
                    selection_idx += 1
            
            elif ch == b'\x1b':
                break

            clear()
        clear()


    def _display_item(self):
        
        section_selected = ">"
        section_non_selected = " "
        selection_idx = 0
        clear()

        while True:
            selection_str_list = self.player.items + ["Exit"]
            tmp = deepcopy(selection_str_list)
            menu_length = len(tmp)
            for i in range(menu_length):
                if selection_idx  == i:
                    tmp[i] = section_selected + tmp[i] 
                else:
                    tmp[i] = section_non_selected + tmp[i] 

            print("="*30)
            print("\n".join(tmp))
            print("="*30)
            print("Bonus point: {}".format(self.player.bonus_point))
            
            tmp = []
            for i in non_selected_parameters[:3]:
                tmp.append("{0}: {1}".format(i, eval("self.player.{0}".format(i))))
        
            print(" ".join(tmp))
            
            tmp = []
            for i in non_selected_parameters[3:]:
                tmp.append("{0}: {1}".format(i, eval("self.player.{0}".format(i))))
                
            print(" ".join(tmp))
            ch = getch()

            if ch == b'\r':
                
                if selection_idx < menu_length - 1:
                    # TODO: The temporary effect needs to be considered.
                    item_name = selection_str_list[selection_idx]
                    item_effect = item_json[selection_str_list[selection_idx]]
                    item = Item(item_name, item_effect)
                    
                    if item.use_item(self.player):
                        del self.player.items[selection_idx]

                # Exit Item menu.
                elif selection_idx == menu_length - 1:
                    break
            
            elif ch == "UP_KEY":
                if selection_idx > 0:
                    selection_idx -= 1
                
            elif ch == "DOWN_KEY":
                if selection_idx < menu_length - 1:
                    selection_idx += 1
            
            elif ch == b'\x1b':
                break

            clear()
        clear()

    # Save player's data and attributes.
    def save_data(self):
        # The value for storing player data.
        saved_data_dic = {}
        
        saved_json_file_path = os.path.join(save_data_folder, save_data_file_name)

        # If directory does not exist, then it will be created.
        if not os.path.isdir(save_data_folder):
            os.mkdir(save_data_folder)

        # File is created if it does not exist.
        if not os.path.isfile(saved_json_file_path):
            open(saved_json_file_path, 'a').close()

        for attribute in numerical_player_strengh + current_status_player + non_numerical_player_strength + \
            string_numerical_player_strength:
            exec("""saved_data_dic["{0}"] = self.player.{0}""".format(attribute))

        
        # Save map information and player location.
        saved_data_dic["object_pos"] = self.player.object_pos
        saved_data_dic["map_grid"] = self.original_map_grid
        saved_data_dic["hidden_map_grid"] = self.hidden_map_grid
        saved_data_dic["map_level"] = self.level

        with open(saved_json_file_path, 'w') as f:
            f.write(json.dumps(saved_data_dic, indent = 4)) 


    # Load saved json data and restore a game session.
    def load_data(self):
        saved_json_file_path = os.path.join(save_data_folder, save_data_file_name)

        # Read all player's data.
        try:
            with open (saved_json_file_path, 'r') as f:
                json_data = json.loads(f.read())
        except:
            print('Error while loading game...')

        self.player = MazeObject(json_data)
        self.original_map_grid = json_data["map_grid"]
        self.hidden_map_grid = json_data["hidden_map_grid"]
        self.level = json_data["map_level"]

    # It is called every time the cursor is moved.
    def _move_player(self,str_direction):
        
        pos_move = direction[arrow_key_to_directions[str_direction]]
        next_player_pos = (self.player.object_pos[0] + pos_move[0],self.player.object_pos[1] + pos_move[1])
        
        # If there is a collision, then it will simply draw the map.
        if self.original_map_grid[next_player_pos[0]][next_player_pos[1]] == self.goal_symbol:
           
            clear()

            # Enemy appears before reaches a goal.
            if self._enemy_encounter(self.player.luckiness):
                return True

            self._move_player_sub(str_direction, next_player_pos)

            # TODO: Allow player to select yes or no to proceed to the next level.
            self._map_proceed_selection()

            clear()
            self._draw_hidden_map()

        elif self.original_map_grid[next_player_pos[0]][next_player_pos[1]] == self.treasure_symbol:
            clear()

            if self._enemy_encounter(self.player.luckiness):
                return True

            self._move_player_sub(str_direction, next_player_pos)

            self._treasure_selection(next_player_pos)
            
            clear()
            self._draw_hidden_map()


        elif self.original_map_grid[next_player_pos[0]][next_player_pos[1]] != "#":
            clear()

            self._move_player_sub(str_direction, next_player_pos)
            
            # Draw the enemy encouter screen.
            if self._enemy_encounter(self.player.luckiness):
                return True

            self._draw_hidden_map()
            
        else:
            clear()
            self._draw_hidden_map()
    
    def _treasure_selection(self, next_player_pos):
         # Allows the users to select whether they will proceed to the next floor...
        
        selection_list = ["Yes", "No"]
        cursor_not_selected = " "
        cursor_selected = ">"
        tmp_cursor = deepcopy(selection_list)
        cursor_selection = 1
        
        while True:

            self._draw_hidden_map()
            for i in range(len(tmp_cursor)):
                if i == cursor_selection:
                    tmp_cursor[i] = cursor_selected + tmp_cursor[i]
                else:
                    tmp_cursor[i] = cursor_not_selected + tmp_cursor[i]

            print("Will you pick up the item?")
            print("".join(tmp_cursor))

            tmp_cursor = deepcopy(selection_list)
            tmp = getch()
            if tmp == "LEFT_KEY":
                if cursor_selection > 0:
                        cursor_selection -= 1
                
            elif tmp == "RIGHT_KEY":
                if cursor_selection < len(tmp_cursor) - 1:
                        cursor_selection += 1

            elif tmp == b"\r":

                # Yes case --> Initialise map.
                if cursor_selection == 0:
                    obtained_item = random_item_selection()
                    self.player.items.append(obtained_item)

                    # Remove the treasure from map.
                    self.original_map_grid[next_player_pos[0]][next_player_pos[1]] = " "
                    self.map_grid = deepcopy(self.original_map_grid)
                    self.map_grid[next_player_pos[0]][next_player_pos[1]] = self.player.displayed_character
                    print("Player obtained {}".format(obtained_item))
                    getch()
                    break

                # No case --> Do nothing.
                if cursor_selection == 1:
                    break
            clear()
        clear()
    
    # Randomly place player
    def _randomly_place_player(self,player):
        space_list_to_place_player = []
        for y in range(len(self.map_grid[0])):
            for x in range(len(self.map_grid)):
                if self.map_grid[x][y] == " ":
                    space_list_to_place_player.append((x,y))
        
        # Choose the place where the player can begin journey
        chosen_place = choice(space_list_to_place_player)
        self.map_grid[chosen_place[0]][chosen_place[1]] = self.player.displayed_character
        self.player.object_pos = chosen_place

    def _randomly_place_objects(self, symbol_to_use):
        
        # Only one goal can be created
        # Choose the place for a goal
        space_list_to_place_goal = []
        for y in range(len(self.map_grid[0])):
            for x in range(len(self.map_grid)):
                if self.map_grid[x][y] == " ":
                    space_list_to_place_goal.append((x,y))
        
        # Choose the location of goal
        chosen_place = choice(space_list_to_place_goal)
        self.map_grid[chosen_place[0]][chosen_place[1]] = symbol_to_use

    # Mainly used for drawing maps.
    # Draw the hidden map on the screen.
    def _draw_hidden_map(self):

        self._reveal_map_grid()
        tmp_str = ""

        # NOTE: x: height, y: length
        for y in range(len(self.hidden_map_grid[0])):
            for x in range(len(self.hidden_map_grid)):
                tmp_str += self.hidden_map_grid[x][y]
            tmp_str += "\n"
        
        # Print map
        print(tmp_str)
        self._display_status()