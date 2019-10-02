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
from sub_func import *

# Possibility of using the skill: 20%
# To test the skills using enemy: Set this to 100% (1.0)
enemy_use_skill_possibility = 0.0

# The value which determine the difficulty of level increase.
constant_next_level_exp = 1.4
default_amount_to_reveal = 3
# Load creatures.

"""
Reads item data for creating the objects.
Note: The object will not be create unless it is 
the temporary effective items.
"""

creature_file_path = os.path.join(data_dir,creature_data_file_name)
enemy_json = json.loads(open(creature_file_path, "r").read())

item_data_file_path = os.path.join(data_dir, item_data_file_name)
item_json = json.loads(open(item_data_file_path, "r").read())

skill_data_file_path = os.path.join(data_dir, skill_data_file_name)
skill_json = json.loads(open(skill_data_file_path, "r").read())

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

non_numerical_current_player_strength =   ["current_strength", "current_agility", "current_vitality", "current_dexterity",
                                           "current_smartness", "current_magic_power", "current_mental_strength", "current_luckiness"]

current_maximum_player_strength = ["current_max_hp", "current_max_mp", "current_max_sp", "current_max_ep"]

# These parameters will not be selected in the selection menu.
non_selected_parameters = ["current_exp","next_exp","level","current_hp", 
                                   "current_mp", "current_sp", "current_ep"]
        
body_parts_list = ["hand","head", "arm","leg","body_armor","right_wrist","left_wrist","right_finger","left_finger"]
# The map for players to walk at the beginning

# Randomly select the items from the list based on the item's list and level....
def random_item_selection(level = 1):
    return choice(list(item_json.keys()))

class MainGame(object):

    """
    When initialised, Map object puts players and item boxes at the
    places.

    When loading the game the game will load the following data:
    loaded_map: map to be loaded.
    loaded_player: player data to be loaded.

    If not, all the data will be initialized to start the game.
    """
    
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
            self.map_grid[self.player.object_data["object_pos"][0]][self.player.object_data["object_pos"][1]]\
                = self.player.object_data["displayed_character"] 
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
    def _fight_with_enemy(self):
        
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
            player_base_attack_value = self.player.object_data["current_strength"]
            enemy_durability = enemy.object_data["current_vitality"]

            player_attack_value = int(round(uniform(0.8,1.0) *(player_base_attack_value - (0.2 * enemy_durability)), 0))

            
            # Determine whether an attack is hit.
            if (uniform(0.1, 1.0) * self.player.object_data["current_dexterity"]) > (uniform(0 ,0.2) * enemy.object_data["current_agility"]):
                enemy.object_data["current_hp"]  -= max(player_attack_value, 0)
            else:
                print("You missed the attack!")

            if enemy.object_data["current_hp"]  < 1:
                print("You defeated the creature!")
                print("Player acquire {} exp".format(enemy.object_data["exp"]))
                print("Press any key to return to map...")
                self.player._get_experience(enemy.object_data["exp"])
                
                # If it is bigger, then the enemy will drop an item.
                if uniform(0,1.0) > 0.8 - (0.8 / (100 / (self.player.object_data["current_luckiness"] ** 0.70))):
                    print("Enemy dropped item!")
                    print("The content of the item is {}".format(enemy.object_data["drop_item"]))
                    tmp = {}
                    tmp[enemy.object_data["drop_item"]] = item_json[enemy.object_data["drop_item"]]
                    self.player.object_data["items"].append(tmp)
                
                getch()
                clear()
                return True
            else:
                print("Player delivers {} damage".format(player_attack_value))
                getch()
                return False
        
        # TODO: Allow enemy to use their skills.
        def _enemy_turn_normal_attack():
            # Enemy turn
            enemy_base_attack_value = enemy.object_data["current_strength"]
            player_durability = self.player.object_data["current_vitality"]
            enemy_attack_value = int(round(uniform(0.8,1.0) *(enemy_base_attack_value - (0.2 * player_durability)), 0))

            # Determine whether an attack is hit.
            if (uniform(0.1, 1.0) * enemy.object_data["current_dexterity"]) > (uniform(0 ,0.2) * self.player.object_data["current_agility"]):
                self.player.object_data["current_hp"]  -= max(enemy_attack_value, 0)
            else:
                print("Enemy missed the attack!")
            if self.player.object_data["current_hp"]  < 1:
                print("You are defeated...")
                print("Game Over...")
                getch()
                clear()
                return True

            else:
                print("Enemy delivers {} damage".format(enemy_attack_value))
                getch()
                return False
        
        # NOTE: Enemy use the skill randomly (20% of chance).
        # TODO: Both enemy and player can use the same function.
        def _turn_use_skill(skill_data, skill_user, opponent, is_enemy = False, message = "player"):
            
            if is_enemy and skill_data == None:
            # If there is no skills, then it will conduct an normal attack
                _enemy_turn_normal_attack()
                return

            hp_change, mp_change, sp_change, ep_change, is_against_player =\
                use_skill(skill_user,skill_data, opponent, False)
            
            print("{} use skill".format(message))
            if is_enemy and opponent.object_data["current_hp"] < 1:
                print("You are defeated...")
                print("Game Over...")
                getch()
                clear()
                return True

            elif not is_enemy and opponent.object_data["current_hp"]  < 1:
                print("You defeated the creature!")
                print("Player acquire {} exp".format(opponent.object_data["exp"]))
                print("Press any key to return to map...")
                skill_user._get_experience(opponent.object_data["exp"])
                
                # If it is bigger, then the enemy will drop an item.
                if uniform(0,1.0) > 0.8 - (0.8 / (100 / (skill_user.object_data["current_luckiness"] ** 0.70))):
                    print("Enemy dropped item!")
                    print("The content of the item is {}".format(opponent.object_data["drop_item"]))
                    tmp = {}
                    tmp[opponent.object_data["drop_item"]] = item_json[opponent.object_data["drop_item"]]
                    skill_user.object_data["items"].append(tmp)
                
                getch()
                clear()
                return True
            
            else:
                if is_against_player:
                    if hp_change > 0:
                        print("{} gained {} hp point(s)".format(message,hp_change))
                    if mp_change > 0:
                        print("{} gained {} mp point(s)".format(message,mp_change))
                    if sp_change > 0:
                        print("{} gained {} sp point(s)".format(message,sp_change))
                    if ep_change > 0:
                        print("{} gained {} ep point(s)".format(message, ep_change))
                    getch()
                
                # TODO: Remove abs.
                else:
                    if hp_change > 0:
                        print("{} delivered {} damage".format(message, hp_change))
                    if mp_change > 0:
                        print("{} delivered {} mp damage".format(message, mp_change))
                    if sp_change > 0:
                        print("{} delivered {} sp damage".format(message, sp_change))
                    if ep_change > 0:
                        print("{} delivered {} ep damage".format(message, ep_change))
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
            tmp_key = getch()

            if tmp_key == "UP_KEY":
                if cursor_selection > 0:
                        cursor_selection -= 1
                
            elif tmp_key == "DOWN_KEY":
                if cursor_selection < len(tmp_cursor) - 1:
                        cursor_selection += 1

            elif tmp_key == b"\r":
                
                # TODO: Enable player to act simultaneously.
                # Normally attack the enemy.
                if cursor_selection == 0:

                    # Turn based fight. The player can firstly fight for the enemy this value is higher.
                    if uniform(0.8, 1.0)*self.player.object_data["agility"] > uniform(0.8,1.0)* enemy.object_data["agility"]:
                        
                        # Player turn.
                        if _player_turn_normal_attack():
                            break
                        
                        # Enemy turn
                        if uniform (0, 1.0) < enemy_use_skill_possibility:
                            if _enemy_turn_normal_attack():
                                return True
                        else:
                            if _turn_use_skill(choice(enemy.object_data["skills"]) if enemy.object_data["skills"] != [] else None
                            ,enemy,self.player, True, "Enemy"):
                                return True

                    else:
                        # Enemy turn
                        if uniform (0, 1.0) < enemy_use_skill_possibility:
                            if _enemy_turn_normal_attack():
                                return True
                        else:
                            if _turn_use_skill(choice(enemy.object_data["skills"]) if enemy.object_data["skills"] != [] else None
                            ,enemy,self.player, True, "Enemy"):
                                return True

                        # Player turn.
                        if _player_turn_normal_attack():
                            break
                    
                # TODO: Create the function that handles player's skills.
                # Displays the player's status.
                elif cursor_selection == 1:
                    skill_data = self._display_skills(True)
                    if skill_data != None: 
                         
                        # Turn based fight. The player can firstly fight for the enemy this value is higher.
                        if uniform(0.8, 1.0)*self.player.object_data["agility"] > uniform(0.8,1.0)* enemy.object_data["agility"]:
                            
                            # Player turn
                            if _turn_use_skill(skill_data,self.player, enemy):
                                break
                            
                            # Enemy turn
                            if uniform (0, 1.0) < enemy_use_skill_possibility:
                                if _enemy_turn_normal_attack():
                                    return True
                            else:
                                if _turn_use_skill(choice(enemy.object_data["skills"]) if enemy.object_data["skills"] != [] else None
                                ,enemy,self.player, True, "Enemy"):
                                    return True
                        else:

                            # Enemy turn
                            if uniform (0, 1.0) < enemy_use_skill_possibility:
                                if _enemy_turn_normal_attack():
                                    return True
                            else:
                                if _turn_use_skill(choice(enemy.object_data["skills"]) if enemy.object_data["skills"] != [] else None
                                ,enemy,self.player, True, "Enemy"):
                                    return True
                            
                            # Player Turn
                            if _turn_use_skill(skill_data,self.player, enemy):
                                break
                        getch()

                    clear()
                    """
                    Escape from the enemy.
                    The rate of the escape depends on the values of
                    the success.
                    """
                # TODO: Enable player to use item.
                elif cursor_selection == 2:            
                    print("This feature will be implemented later...")
                    getch()
                    clear()
                    
                
                elif cursor_selection == 3:
                    print("This feature will be implemented later...")
                    getch()
                    clear()
                    

                # Escape function.
                # Escape will be successful if the value is bigger than enemy's.
                elif cursor_selection == 4:
                    if uniform(0.8, 1.0)* self.player.object_data["agility"] > uniform(0.2,0.5)* enemy.object_data["agility"]:
                        print("Player managed to escape...")
                        getch()
                        break
                    else:
                        print("Cannot escape!")
                        _enemy_turn_normal_attack()

            clear()
        clear()
        
    # TODO: The encounter percentage must be changed
    # Take the luck of the player into account.
    def _enemy_encounter(self, player_luck_value):
        k = random()

        # TODO: Make the possibility calculation possible...
        tmp = max(default_ememy_encounter, min_enemy_encounter)

        # Create the object instead of calling function...
        if 0 < k and k < tmp:
            return self._fight_with_enemy()

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
        for i in range(max(0, self.player.object_data["object_pos"][0] - self.default_amount_to_reveal),\
            min(self.player.object_data["object_pos"][0] + self.default_amount_to_reveal, len(self.map_grid[0]))):
            for j in range(max(0, self.player.object_data["object_pos"][1] - self.default_amount_to_reveal),\
                min(self.player.object_data["object_pos"][1] + self.default_amount_to_reveal, len(self.map_grid))):
                # Reveal a part of maps around player at a certain amount.
                    self.hidden_map_grid[i][j] = self.map_grid[i][j]

    def _move_player_sub(self,str_direction, next_player_pos):
        # Initialize map using originally created random map.
        self.map_grid = deepcopy(self.original_map_grid)

        # Place player on the map based on the move player made.
        self.map_grid[next_player_pos[0]][next_player_pos[1]] = self.player.object_data["displayed_character"]

        # Update player position.
        self.player.object_data["object_pos"] = next_player_pos
        
        self.player.object_data["current_ep"] = max(self.player.object_data["current_ep"] - 1, 0)


        # if the current ep is zero. the current hp will decreases.
        if self.player.object_data["current_ep"] == 0:
            self.player.object_data["current_hp"] = max(self.player.object_data["current_hp"] - 1, 1)

        # Update player's abilities every time the player make movement.
        self.player.update_object()

        # This methods is used only when player moves.
        self.player.move_update_object()

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
            tmp_key = getch()
            if tmp_key == "LEFT_KEY":
                if cursor_selection > 0:
                        cursor_selection -= 1
                
            elif tmp_key == "RIGHT_KEY":
                if cursor_selection < len(tmp_cursor) - 1:
                        cursor_selection += 1

            elif tmp_key == b"\r":
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
        print("HP: {}, MP: {}, SP: {}, EP: {}".format(self.player.object_data["current_hp"], 
        self.player.object_data["current_mp"],
        self.player.object_data["current_sp"], 
        self.player.object_data["current_ep"]))
    

    def player_menu(self):
        clear()
        
        # There is no load function until player moves to exit.
        selection_list = ["Item", "Skills","Save","Status", "Equip", "Exit"]
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
            tmp_key = getch()
            
            if tmp_key == "UP_KEY":
                if cursor_selection > 0:
                    cursor_selection -= 1
                
            elif tmp_key == "DOWN_KEY":
                if cursor_selection < len(tmp_cursor) - 1:
                    cursor_selection += 1

            elif tmp_key == b"\r":

                # Display items player has got.
                if cursor_selection == 0:
                    self._display_item()

                # Display skills
                if cursor_selection == 1:
                    self._display_skills()

                
                if cursor_selection == 2:
                    self.save_data()
                
                # Displaying player's status, allowing users to
                # improve status using bonus points.
                if cursor_selection == 3:
                    self._display_player_status()

                # Display only the equittable items.
                if cursor_selection == 4:
                    self._display_equitable_items()

                if cursor_selection == 5:  
                    break

                clear()

            elif tmp_key == b"\x1b":
                break

            clear()
        clear()
        self._draw_hidden_map()
    
    # The function which allows player to dispose items.
    # TODO: Enable the scroll of the item.
    def _dispose_item(self, previous_str):
        selection_list = ["Yes", "No"]
        cursor_not_selected = " "
        cursor_selected = ">"
        tmp_cursor = deepcopy(selection_list)
        cursor_selection = 1
        
        while True:
            clear()
            for i in range(len(tmp_cursor)):
                if i == cursor_selection:
                    tmp_cursor[i] = cursor_selected + tmp_cursor[i]
                else:
                    tmp_cursor[i] = cursor_not_selected + tmp_cursor[i]
            
            print(previous_str)
            print("Will you dispose the selected item?")
            print("".join(tmp_cursor))
            tmp_cursor = deepcopy(selection_list)
            tmp_key = getch()
            if tmp_key == "LEFT_KEY":
                if cursor_selection > 0:
                        cursor_selection -= 1
                
            elif tmp_key == "RIGHT_KEY":
                if cursor_selection < len(tmp_cursor) - 1:
                        cursor_selection += 1

            elif tmp_key == b"\r":
                # Yes case --> Initialise map.
                if cursor_selection == 0:
                    return True
                
                # No case --> Do nothing.
                if cursor_selection == 1:
                    return False
            clear()
        clear()
        pass

    def _display_item(self):
        
        section_selected = ">"
        section_non_selected = " "
        selection_idx = 0
        clear()
        item_list, other_items = find_item_type(self.player.object_data["items"], ["item", "skill_book"])
        while True:
            selection_str_list = extract_item_names(item_list) + ["Exit"]\
                if len(self.player.object_data["items"]) > 0 else ["Exit"] 
            tmp = deepcopy(selection_str_list)
            menu_length = len(tmp)
            for i in range(menu_length):
                if selection_idx  == i:
                    tmp[i] = section_selected + tmp[i] 
                else:
                    tmp[i] = section_non_selected + tmp[i] 

            displayed_str = "Equipment Menu\n" +\
            "="*30+"\n" +\
            "\n".join(tmp) + "\n" +\
            "="*30+"\n" +\
            "Bonus point: {}".format(self.player.object_data["bonus_point"]) + "\n"

            tmp = []
            for i in non_selected_parameters[:3]:
                tmp.append("{0}: {1}".format(i, self.player.object_data[i]))
            
            displayed_str +=  " ".join(tmp) + "\n"
            
            tmp = []
            for i in non_selected_parameters[3:]:
                tmp.append("{0}: {1}".format(i, self.player.object_data[i]))    
            displayed_str +=  " ".join(tmp) + "\n"
            print(displayed_str)
            tmp_key = getch()

            if tmp_key == b'\r':

                if selection_idx < menu_length - 1:
                    # TODO: The temporary effect needs to be considered.
                    item = item_list[selection_idx]
                    item_name = list(item.keys())[0]

                    if item[item_name]["is_item"]:
                        if use_item(self.player, item_name, item):
                            del item_list[selection_idx]
                    elif item[item_name]["is_skill_book"]:
                        # Put the skills on the player if the skill slot is not beyond the skils.
                        self.player.object_data["skills"].append(use_skill_book(skill_json, item[item_name]["level"]))
                        del item_list[selection_idx]

                # Exit Item menu.
                elif selection_idx == menu_length - 1:
                    break
            
            elif tmp_key == "UP_KEY":
                if selection_idx > 0:
                    selection_idx -= 1
                
            elif tmp_key == "DOWN_KEY":
                if selection_idx < menu_length - 1:
                    selection_idx += 1
            
            elif tmp_key == b"d" or tmp_key == b"D":
                if self._dispose_item(displayed_str):
                    del item_list[selection_idx]

            elif tmp_key == b'\x1b':
                break

            clear()
        self.player.object_data["items"] = item_list + other_items
        clear()

    # Display which item to equip.
    # When equipping, the player's status is
    # altered.
    # TODO: Add the resistance to negative status effects on the players.
    def _display_equitable_items(self):
        
        exit_to_player_menu = ["Exit"]
        section_selected = ">"
        section_non_selected = " "
        selection_idx = 0
        selection_str_list = body_parts_list + exit_to_player_menu
        clear()

        while True:
            
            tmp = deepcopy(selection_str_list)
            menu_length = len(tmp)
            
            for i in range(menu_length):
                if i < menu_length - 1:
                    if selection_idx  == i:
                        tmp[i] = section_selected + tmp[i] + ": {}".format(list(self.player.object_data[tmp[i]].keys())[0] if\
                            self.player.object_data[tmp[i]] != [] else "None")
                    else:
                        tmp[i] = section_non_selected + tmp[i] + ": {}".format(list(self.player.object_data[tmp[i]])[0] if\
                            self.player.object_data[tmp[i]] != [] else "None")
                else:
                    if selection_idx  == i:
                        tmp[i] = section_selected + tmp[i]
                    else:
                        tmp[i] = section_non_selected + tmp[i]
            
            displayed_str = "Equipment Menu\n" +\
            "="*30+"\n" +\
            "\n".join(tmp) + "\n" +\
            "="*30+"\n" +\
            "Bonus point: {}".format(self.player.object_data["bonus_point"]) + "\n"

            tmp = []
            for i in non_selected_parameters[:3]:
                tmp.append("{0}: {1}".format(i, self.player.object_data[i]))
            
            displayed_str +=  " ".join(tmp) + "\n"
            
            tmp = []
            for i in non_selected_parameters[3:]:
                tmp.append("{0}: {1}".format(i, self.player.object_data[i]))    
            print(displayed_str)
            tmp_key = getch()
            displayed_str +=  " ".join(tmp) + "\n"

            
            if tmp_key == b'\r':
                # TODO: Select only the items labelled as one of body parts.
                if selection_idx < menu_length - 1:
                    if "hand" in body_parts_list[selection_idx]:
                        self._display_equitable_items_sub("weapon", "weapon")
                    elif "wrist" in body_parts_list[selection_idx]:
                        self._display_equitable_items_sub("wrist", body_parts_list[selection_idx])
                    elif "finger" in body_parts_list[selection_idx]:
                        self._display_equitable_items_sub("ring", body_parts_list[selection_idx])
                    else:
                        self._display_equitable_items_sub(body_parts_list[selection_idx], body_parts_list[selection_idx])
                    
                elif selection_idx == menu_length - 1:
                    break
            
            elif tmp_key == "UP_KEY":
                if selection_idx > 0:
                    selection_idx -= 1
                
            elif tmp_key == "DOWN_KEY":
                if selection_idx < menu_length - 1:
                    selection_idx += 1

            elif tmp_key == b'\x1b':
                break

            clear()
        clear()

    def _display_equitable_items_sub(self, selected_item_type, item_type_for_display):
        
        exit_and_unequip_to_player_menu = ["Unequip", "Exit"]
        section_selected = ">"
        section_non_selected = " "
        selection_idx = 0
        selection_str_list = body_parts_list + exit_and_unequip_to_player_menu
        clear()

        item_list, other_items = find_item_type(self.player.object_data["items"], selected_item_type)
        
        while True:
            selection_str_list = extract_item_names(item_list) + exit_and_unequip_to_player_menu\
                if item_list != [] else exit_and_unequip_to_player_menu
            selection_str_list = selection_str_list
            
            tmp = deepcopy(selection_str_list)
            menu_length = len(tmp)
            
            for i in range(menu_length):
                if selection_idx  == i:
                    tmp[i] = section_selected + tmp[i]
                else:
                    tmp[i] = section_non_selected + tmp[i]
        
            print("Equipment Menu")
            print("="*30)
            print("\n".join(tmp)) 
            print("="*30)
            print("Current Equipment: {}".format(list(self.player.object_data[item_type_for_display].keys())[0]
            if self.player.object_data[item_type_for_display] != [] else "None"))
            print("="*30)
            
            tmp = []
            for i in non_selected_parameters[:3]:
                tmp.append("{0}: {1}".format(i, self.player.object_data[i]))
        
            print(" ".join(tmp))
            
            tmp = []
            for i in non_selected_parameters[3:]:
                tmp.append("{0}: {1}".format(i, self.player.object_data[i]))
                
            print(" ".join(tmp))
            tmp_key = getch()            

            if tmp_key == b'\r':
                # Equip the item by inserting the data to the corresponding part of dictionary.
                # TODO: Select only the items labelled as one of body parts.
                # Equip the item for player.
                if selection_idx < menu_length - 2:
                    if self.player.object_data[item_type_for_display] != []:
                        item_list += [self.player.object_data[item_type_for_display]]

                    self.player.object_data[item_type_for_display] = item_list[selection_idx]
                    del item_list[selection_idx]

                    self.player.update_object()

                elif selection_idx == menu_length - 2:
                    if self.player.object_data[item_type_for_display] != []:
                        tmp_item = self.player.object_data[item_type_for_display]
                        # Unequip the item by putting [] on the data.
                        # TODO: Implement the update of the player's status every time
                        # equipment is stripped or worn
                        self.player.object_data[item_type_for_display] = []
                        item_list += [tmp_item]
                        self.player.update_object()

                elif selection_idx == menu_length - 1:
                    break
            
            elif tmp_key == "UP_KEY":
                if selection_idx > 0:
                    selection_idx -= 1
                
            elif tmp_key == "DOWN_KEY":
                if selection_idx < menu_length - 1:
                    selection_idx += 1
            
            elif tmp_key == b"d" or tmp_key == b"D":
                if self._dispose_item(""):
                    del item_list[selection_idx]

            elif tmp_key == b'\x1b':
                break

            clear()
        self.player.object_data["items"] = item_list + other_items
        clear()
    

    def _display_skills(self, is_in_fight = False):
        section_selected = ">"
        section_non_selected = " "
        selection_idx = 0
        clear()
        
        while True:
            selection_str_list = extract_item_names(self.player.object_data["skills"]) + ["Exit"]\
                if len(self.player.object_data["skills"]) > 0 else ["Exit"] 
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
            print("Bonus point: {}".format(self.player.object_data["bonus_point"]))
            
            tmp = []
            for i in non_selected_parameters[:3]:
                tmp.append("{0}: {1}".format(i, self.player.object_data[i]))
        
            print(" ".join(tmp))
            
            tmp = []
            for i in non_selected_parameters[3:]:
                tmp.append("{0}: {1}".format(i, self.player.object_data[i]))
                
            print(" ".join(tmp))
            tmp_key = getch()

            if tmp_key == b'\r':
                
                if selection_idx < menu_length - 1:
                    # The function that will use player's skills
                    if is_in_fight:
                        return self.player.object_data["skills"][selection_idx]
                    else:
                        use_skill(self.player, self.player.object_data["skills"][selection_idx])                
                    break

                # Exit Item menu.
                elif selection_idx == menu_length - 1:
                    break
            
            elif tmp_key == "UP_KEY":
                if selection_idx > 0:
                    selection_idx -= 1
                
            elif tmp_key == "DOWN_KEY":
                if selection_idx < menu_length - 1:
                    selection_idx += 1

            elif tmp_key == b'\x1b':
                break

            clear()
        clear()

    # The item
    # selected_item_type: item type to be equipped.
    # equipped item 
    
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
                        tmp[i] = section_selected + tmp[i] + ": "+ str(self.player.object_data[tmp[i]])
                    else:
                        tmp[i] = section_non_selected + tmp[i] + ": "+ str(self.player.object_data[tmp[i]])
                else:
                    if selection_idx  == i:
                        tmp[i] = section_selected + tmp[i]
                    else:
                        tmp[i] = section_non_selected + tmp[i]
            
            print("Status Menu")
            print("="*30)
            print("\n".join(tmp))
            print("="*30)

            tmp = []
            print("\n".join(["{0}: {1}".format(x, str(self.player.object_data[x]))
            for x in current_maximum_player_strength + non_numerical_current_player_strength]))
            print("="*30)
            print("Bonus point: {}".format(self.player.object_data["bonus_point"]))
            
            tmp = []
            for i in non_selected_parameters[:3]:
                tmp.append("{0}: {1}".format(i, self.player.object_data[i]))
            print(" ".join(tmp))
            
            tmp = []
            for i in non_selected_parameters[3:]:
                tmp.append("{0}: {1}".format(i, self.player.object_data[i]))
                
            print(" ".join(tmp))
            tmp_key = getch()

            if tmp_key == b'\r':
                
                if selection_idx < 3 and self.player.object_data["bonus_point"] > 0:
                    self.player.object_data[selection_str_list[selection_idx]] += 5
                    self.player.object_data["bonus_point"] -= 1

                elif selection_idx >= 3 and selection_idx < menu_length - 1 and self.player.object_data["bonus_point"] > 0:
                    self.player.object_data[selection_str_list[selection_idx]] += 1
                    self.player.object_data["bonus_point"] -= 1

                elif selection_idx == menu_length - 1:
                    break
            
            elif tmp_key == "UP_KEY":
                if selection_idx > 0:
                    selection_idx -= 1
                
            elif tmp_key == "DOWN_KEY":
                if selection_idx < menu_length - 1:
                    selection_idx += 1
            
            elif tmp_key == b'\x1b':
                break

            self.player.update_object()
            clear()
        
        # Just in case to prevent the errors.
        self.player.update_object()
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
            saved_data_dic[attribute] = self.player.object_data[attribute]
        
        # Save map information and player location.
        saved_data_dic["object_pos"] = self.player.object_data["object_pos"]
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
        next_player_pos = (self.player.object_data["object_pos"][0]+ pos_move[0], \
            self.player.object_data["object_pos"][1] + pos_move[1])
        
        # If there is a collision, then it will simply draw the map.
        if self.original_map_grid[next_player_pos[0]][next_player_pos[1]] == self.goal_symbol:
           
            clear()

            # Enemy appears before reaches a goal.
            if self._enemy_encounter(self.player.object_data["luckiness"]):
                return True

            self._move_player_sub(str_direction, next_player_pos)

            # TODO: Allow player to select yes or no to proceed to the next level.
            self._map_proceed_selection()

            clear()
            self._draw_hidden_map()

        elif self.original_map_grid[next_player_pos[0]][next_player_pos[1]] == self.treasure_symbol:
            clear()

            if self._enemy_encounter(self.player.object_data["luckiness"]):
                return True

            self._move_player_sub(str_direction, next_player_pos)

            self._treasure_selection(next_player_pos)
            
            clear()
            self._draw_hidden_map()


        elif self.original_map_grid[next_player_pos[0]][next_player_pos[1]] != "#":
            clear()

            self._move_player_sub(str_direction, next_player_pos)
            
            # Draw the enemy encouter screen.
            if self._enemy_encounter(self.player.object_data["luckiness"]):
                return True

            self._draw_hidden_map()
            
        else:
            clear()
            self._draw_hidden_map()
    
    # NOTE: The item drop is completely random.
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
            tmp_key = getch()
            if tmp_key == "LEFT_KEY":
                if cursor_selection > 0:
                        cursor_selection -= 1
                
            elif tmp_key == "RIGHT_KEY":
                if cursor_selection < len(tmp_cursor) - 1:
                        cursor_selection += 1

            elif tmp_key == b"\r":

                # Yes case --> Initialise map.
                if cursor_selection == 0:
                    obtained_item = random_item_selection()
                    tmp_key = {}
                    tmp_key[obtained_item] = item_json[obtained_item]
                    self.player.object_data["items"].append(tmp_key)

                    # Remove the treasure from original map.
                    self.original_map_grid[next_player_pos[0]][next_player_pos[1]] = " "
                    self.map_grid = deepcopy(self.original_map_grid)
                    self.map_grid[next_player_pos[0]][next_player_pos[1]] = self.player.object_data["displayed_character"]
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
        self.map_grid[chosen_place[0]][chosen_place[1]] = self.player.object_data["displayed_character"]
        self.player.object_data["object_pos"] = chosen_place

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