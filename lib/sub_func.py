# TODO: Implement temporary status changes.
# TODO: Power up the items as the level goes up...
from random import choice
from random import uniform
from functools import reduce
from getch import _Getch
from maze_object import MazeObject
starving_ep_reduction_rate = 4
poison_hp_reduction_rate = 200
getch = _Getch()
# class Item(object):
#     def __init__(self, item_name,json_data = {}, level = 1):
strength_parameters =["strength", "agility", "vitality", "dexterity",
                      "smartness", "magic_power", "mental_strength", "luckiness"]

def extract_item_names(item_data):
    if item_data != []:
        return list(map(lambda x: list(x.keys())[0],item_data))
    else:
        return []

# Sort items based on the item types by name.
def sort_items(item_data):
    pass

def reduce_item_data(one_item, item_types):

    if len(item_types) > 1:
        return reduce(lambda x, y: one_item[list(one_item.keys())[0]]["is_" + x] 
                    or one_item[list(one_item.keys())[0]]["is_" + y], item_types)
    else:
        return one_item[list(one_item.keys())[0]]["is_" + item_types[0]]

# Find the items to list based on item_type.
def find_item_type(item_data, item_types):

    # If the item type is a string, then it will become [string]
    if isinstance(item_types, str):
        item_types = [item_types]
    
    tmp_items = []
    other_items = []

    for i,item_type in enumerate(map(lambda x: reduce_item_data(x, item_types), item_data)):
        if item_type:
            tmp_items.append(item_data[i])
        else:
            other_items.append(item_data[i])

    return tmp_items, other_items

# The skill book gives player to create the 
# Randomly select the skills from skill list.
# Skills are randomly selected based on the book level.
# When a skill book is used, he/she can obtain one skill randomly.
# Player cannot choose his/her skills from skill books.
def use_skill_book(skill_data, book_level = 1):
    # Filter the skill based on the depth of the floor.
    itemized_skill_data = skill_data.items()
    filtered_skill_data = list(filter(lambda x: x[1]["level"] <= book_level, itemized_skill_data))
    return dict((choice(filtered_skill_data),))

def filter_and_choose_monster_by_level(monster_data, floor_level = 1):
    filtered_monster_data = list(filter(lambda x: x[list(x.keys())[0]]["level"] <= floor_level, monster_data))
    return dict((choice(filtered_monster_data),))

def filter_and_choose_item_data_by_level(item_data, floor_level = 1):
    filtered_item_data = list(filter(lambda x: x[1]["level"] <= floor_level, item_data.items()))
    return dict((choice(filtered_item_data),))

# This function is mainly used for sorting purpose.
def filter_item_data_by_type(item_data, item_type):
    filtered_item_data = list(filter(lambda x: x[1][item_type], item_data.items()))
    return filtered_item_data

# Use item for player.
def use_item(player: MazeObject,item_name,item_data):

    # TODO: Do not use item when a current value is the same as a maximum value.
    hp_changed = mp_changed = sp_changed = ep_changed = False
     
    if player.object_data["current_hp"] != player.object_data["current_max_hp"] and item_data[item_name]["hp_change"] != 0:
        player.object_data["current_hp"]  = \
            min(player.object_data["current_hp"]  + item_data[item_name]["hp_change"], player.object_data["current_max_hp"])
        hp_changed = True
    
    if player.object_data["current_mp"] != player.object_data["current_max_mp"] and item_data[item_name]["mp_change"] != 0:
        player.object_data["current_mp"]  = \
            min(player.object_data["current_mp"]  + item_data[item_name]["mp_change"], player.object_data["current_max_mp"])
        mp_changed = True

    if player.object_data["current_sp"] != player.object_data["current_max_sp"] and item_data[item_name]["sp_change"] != 0:
        player.object_data["current_sp"]  = \
            min(player.object_data["current_sp"]  + item_data[item_name]["sp_change"], player.object_data["current_max_sp"])
        sp_changed = True
    
    if player.object_data["current_ep"] != player.object_data["current_max_ep"] and item_data[item_name]["ep_change"] != 0:
        player.object_data["current_ep"]  = \
            min(player.object_data["current_ep"]  + item_data[item_name]["ep_change"], player.object_data["current_max_ep"])
        ep_changed = True

    if "poison" in player.object_data["status_effects"]:
        player.object_data.remove("poison")
        player.object_data["poison_count"] = 0
        pass

    if "curse" in player.object_data["status_effects"]:
        player.object_data.remove("curse")
        player.object_data["curse_count"] = 0

    if "seal" in player.object_data["status_effects"]:
        player.object_data.remove("seal")
        player.object_data["seal_count"] = 0

    if "paralyze" in player.object_data["status_effects"]:
        player.object_data.remove("paralyze")
        player.object_data["paralyze_count"] = 0


    # The reduction of EP becomes more faster.
    if "starving" in player.object_data["status_effects"]:
        player.object_data.remove("starving")
        player.object_data["starving_count"] = 0

    return hp_changed or mp_changed or sp_changed or ep_changed

def use_skill(skill_user, skill_data, target_object = None, is_in_menu = True):
    
    # TODO: Do not use item when a current value is the same as a maximum value
    skill_name = list(skill_data.keys())[0]

    if is_in_menu and skill_data[skill_name]["is_in_fight"]:
        print("This skill cannot be used in the player's menu.")
        getch()
        return False
    
    # TODO: Add status effects on the player.
    # Heal or alter player's status.
    # When enemy us`ing the skill, whether skill is used in main menu must be considered
    elif not skill_data[skill_name]["is_in_fight"]:
        if not is_in_menu or (skill_user.object_data["current_hp"] - skill_data[skill_name]["hp_spent"] >= 0 
        or skill_data[skill_name]["hp_spent"] == 0)\
        and (skill_user.object_data["current_mp"] - skill_data[skill_name]["mp_spent"] >= 0 
        or skill_data[skill_name]["mp_spent"] == 0)\
        and (skill_user.object_data["current_sp"] - skill_data[skill_name]["sp_spent"] >= 0 
        or skill_data[skill_name]["sp_spent"] == 0)\
        and (skill_user.object_data["current_ep"] - skill_data[skill_name]["ep_spent"] >= 0 
        or skill_data[skill_name]["ep_spent"] == 0):

            if not is_in_menu or (skill_user.object_data["current_hp"] != skill_user.object_data["current_max_hp"] 
            and skill_data[skill_name]["hp_change"] != 0)\
            or (skill_user.object_data["current_mp"] != skill_user.object_data["current_max_mp"] 
            and skill_data[skill_name]["mp_change"] != 0)\
            or (skill_user.object_data["current_sp"] != skill_user.object_data["current_max_sp"] 
            and skill_data[skill_name]["sp_change"] != 0)\
            or (skill_user.object_data["current_ep"] != skill_user.object_data["current_max_ep"] 
            and skill_data[skill_name]["ep_change"] != 0):


                hp_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["hp_change"])
                skill_user.object_data["current_hp"] = min(skill_user.object_data["current_hp"] + 
                hp_change,
                skill_user.object_data["current_max_hp"])

                mp_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["mp_change"])
                skill_user.object_data["current_mp"] = min(skill_user.object_data["current_mp"] + 
                mp_change,
                skill_user.object_data["current_max_mp"])
                
                sp_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["sp_change"])
                skill_user.object_data["current_sp"] = min(skill_user.object_data["current_sp"] + 
                sp_change,
                skill_user.object_data["current_max_sp"])

                ep_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["ep_change"])
                skill_user.object_data["current_ep"] = min(skill_user.object_data["current_ep"] + 
                ep_change,
                skill_user.object_data["current_max_ep"])

            
                return hp_change, mp_change, sp_change, ep_change, True
    
    # Player can be the person who receive the damage from enemy.
    # TODO: Add the status effects on the enemy.
    # If player is in fight, then it will perform the attack against enemy.
    elif skill_data[skill_name]["is_in_fight"] and target_object != None:
        if not is_in_menu or (skill_user.object_data["current_hp"] - skill_data[skill_name]["hp_spent"] >= 0 
        or skill_data[skill_name]["hp_spent"] == 0)\
        and (skill_user.object_data["current_mp"] - skill_data[skill_name]["mp_spent"] >= 0 
        or skill_data[skill_name]["mp_spent"] == 0)\
        and (skill_user.object_data["current_sp"] - skill_data[skill_name]["sp_spent"] >= 0 
        or skill_data[skill_name]["sp_spent"] == 0)\
        and (skill_user.object_data["current_ep"] - skill_data[skill_name]["ep_spent"] >= 0 
        or skill_data[skill_name]["ep_spent"] == 0):
            
            hp_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["hp_change"])
            target_object.object_data["current_hp"] = min(target_object.object_data["current_hp"] + 
            hp_change,
            target_object.object_data["current_max_hp"])

            mp_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["mp_change"])
            target_object.object_data["current_mp"] = min(target_object.object_data["current_mp"] + 
            mp_change,
            target_object.object_data["current_max_mp"])
            
            sp_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["sp_change"])
            target_object.object_data["current_sp"] = min(target_object.object_data["current_sp"] + 
            sp_change,
            target_object.object_data["current_max_sp"])

            ep_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["ep_change"])
            target_object.object_data["current_ep"] = min(target_object.object_data["current_ep"] + 
            ep_change,
            target_object.object_data["current_max_ep"])
            
            skill_user.object_data["current_hp"]  -= skill_data[skill_name]["hp_spent"]
            skill_user.object_data["current_mp"]  -= skill_data[skill_name]["mp_spent"]
            skill_user.object_data["current_sp"]  -= skill_data[skill_name]["sp_spent"]
            skill_user.object_data["current_ep"]  -= skill_data[skill_name]["ep_spent"] 
                
            return hp_change, mp_change, sp_change, ep_change, False


# Return the value in accordance with the changes of the values.
# TODO: Add the multiplier to the skills.
def _use_skill_sub(player,skill_data,changed_value):

    tmp = changed_value
    tmp_name = list(skill_data.keys())[0]
    for i in strength_parameters:
        tmp += changed_value * (uniform(1.0, 1.5) * (player.object_data["current_" + i] * skill_data[tmp_name][i + "_multiplier"]))
    
    return int(round(tmp,0))

# NOTE: This function is firstly invoked before the status is updated everytime the player walk
# on the field. This function puts the status effects on characters or creatures on Maze.
def affects_status_on_player(maze_object: MazeObject):
    
    # Firstly, put all status normal before getting into the status effects.
    maze_object.object_data["current_strength"] = maze_object.object_data["strength"]
    maze_object.object_data["current_vitality"] = maze_object.object_data["vitality"]
    maze_object.object_data["current_dexterity"] = maze_object.object_data["dexterity"]
    maze_object.object_data["current_agility"] = maze_object.object_data["agility"]
    maze_object.object_data["current_smartness"] = maze_object.object_data["smartness"]
    maze_object.object_data["current_magic_power"] = maze_object.object_data["magic_power"]
    maze_object.object_data["current_mental_strength"] = maze_object.object_data["mental_strength"]
    maze_object.object_data["current_luckiness"] = maze_object.object_data["luckiness"]
    maze_object.object_data["unable_to_use_skill"] = False
    maze_object.object_data["cannot_act"] = False

    # This effects is effective until its development is over,
    # The status effects can be multiple.
    
    # Object hp decrases gradually
    if "poison" in maze_object.object_data["status_effects"]:
        # HP becomes zero
        maze_object.object_data["current_hp"] = min(1, maze_object.object_data["current_hp"]\
            - ( maze_object.object_data["hp"] // poison_hp_reduction_rate))
    
    # All object's status becomes half.
    if "curse" in maze_object.object_data["status_effects"]:
        maze_object.object_data["current_strength"] = maze_object.object_data["strength"] // 2
        maze_object.object_data["current_vitality"] = maze_object.object_data["vitality"] // 2
        maze_object.object_data["current_dexterity"] = maze_object.object_data["dexterity"] // 2
        maze_object.object_data["current_agility"] = maze_object.object_data["agility"] // 2

        maze_object.object_data["current_smartness"] = maze_object.object_data["smartness"] // 2
        maze_object.object_data["current_magic_power"] = maze_object.object_data["magic_power"] // 2
        maze_object.object_data["current_mental_strength"] = maze_object.object_data["mental_strength"] // 2
        maze_object.object_data["current_luckiness"] = maze_object.object_data["luckiness"] // 2
    
    # Objects are unable to use their skills.
    if "seal" in maze_object.object_data["status_effects"]:
        maze_object.object_data["unable_to_use_skill"] = True

    # Object cannot move and act for a certain amount of time.
    if "paralyzed" in maze_object.object_data["status_effects"]:
        maze_object.object_data["cannot_act"] = True 

    # The reduction of EP becomes more faster.
    if "starving" in maze_object.object_data["status_effects"]:
        maze_object.object_data["current_ep"] -= min(0, maze_object.object_data["current_ep"] - starving_ep_reduction_rate)

# Calculate the decay of the status effects.
def status_effect_decay(maze_object: MazeObject):
        # The count showing the effective duration of status effects.
    maze_object.object_data["poison_count"] -= 1
    maze_object.object_data["paralyze_count"] -= 1
    maze_object.object_data["curse_count"] -= 1
    maze_object.object_data["seal_count"] -= 1

# Calculate the status decay during the fight.
def status_effect_decay_in_fight(maze_object: MazeObject):
    maze_object.object_data["poison_count"] -= 10
    maze_object.object_data["paralyze_count"] -= 10
    maze_object.object_data["curse_count"] -= 10
    maze_object.object_data["seal_count"] -= 10