# TODO: Implement temporary status changes.
# TODO: Power up the items as the level goes up...
from random import choice
from random import uniform
from functools import reduce
from getch import _Getch

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

def filter_monster(monster_data, floor_level = 1):
    filtered_monster_data = list(filter(lambda x: x[list(x.keys())[0]]["level"] <= floor_level, monster_data))
    return dict(choice(filtered_monster_data))

def filter_item_data(item_data, floor_level = 1):
    filtered_item_data = list(filter(lambda x: x[1]["level"] <= floor_level, item_data.items()))
    return dict((choice(filtered_item_data),))

# Use item for player.
def use_item(player,item_name,item_data):

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

    return hp_changed or mp_changed or sp_changed or ep_changed

def use_skill(player, skill_data, target_object = None, is_in_menu = True):
    
    # TODO: Do not use item when a current value is the same as a maximum value
    skill_name = list(skill_data.keys())[0]

    if is_in_menu and skill_data[skill_name]["is_in_fight"]:
        print("This skill cannot be used in the player's menu.")
        getch()
        return False
    
    # TODO: Add the status effects on the player.
    # Heal or alter player's status.
    elif not skill_data[skill_name]["is_in_fight"]:
        if (player.object_data["current_hp"] - skill_data[skill_name]["hp_spent"] >= 0 
        or skill_data[skill_name]["hp_spent"] == 0)\
        and (player.object_data["current_mp"] - skill_data[skill_name]["mp_spent"] >= 0 
        or skill_data[skill_name]["mp_spent"] == 0)\
        and (player.object_data["current_sp"] - skill_data[skill_name]["sp_spent"] >= 0 
        or skill_data[skill_name]["sp_spent"] == 0)\
        and (player.object_data["current_ep"] - skill_data[skill_name]["ep_spent"] >= 0 
        or skill_data[skill_name]["ep_spent"] == 0):
        
            if (player.object_data["current_hp"] != player.object_data["current_max_hp"] 
            and skill_data[skill_name]["hp_change"] != 0)\
            or (player.object_data["current_mp"] != player.object_data["current_max_mp"] 
            and skill_data[skill_name]["mp_change"] != 0)\
            or (player.object_data["current_sp"] != player.object_data["current_max_sp"] 
            and skill_data[skill_name]["sp_change"] != 0)\
            or (player.object_data["current_ep"] != player.object_data["current_max_ep"] 
            and skill_data[skill_name]["ep_change"] != 0):


                hp_change = use_skill_sub(player, skill_data, skill_data[skill_name]["hp_change"])
                player.object_data["current_hp"] = min(player.object_data["current_hp"] + 
                hp_change,
                player.object_data["current_max_hp"])

                mp_change = use_skill_sub(player, skill_data, skill_data[skill_name]["mp_change"])
                player.object_data["current_mp"] = min(player.object_data["current_mp"] + 
                mp_change,
                player.object_data["current_max_mp"])
                
                sp_change = use_skill_sub(player, skill_data, skill_data[skill_name]["sp_change"])
                player.object_data["current_sp"] = min(player.object_data["current_sp"] + 
                sp_change,
                player.object_data["current_max_sp"])

                ep_change = use_skill_sub(player, skill_data, skill_data[skill_name]["ep_change"])
                player.object_data["current_ep"] = min(player.object_data["current_ep"] + 
                ep_change,
                player.object_data["current_max_ep"])

            
                return hp_change, mp_change, sp_change, ep_change, True
    
    # Player can be the person who receive the damage from enemy.
    # TODO: Add the status effects on the enemy.
    # If player is in fight, then it will perform the attack against enemy.
    elif skill_data[skill_name]["is_in_fight"] and target_object != None:
        if (player.object_data["current_hp"] - skill_data[skill_name]["hp_spent"] >= 0 
        or skill_data[skill_name]["hp_spent"] == 0)\
        and (player.object_data["current_mp"] - skill_data[skill_name]["mp_spent"] >= 0 
        or skill_data[skill_name]["mp_spent"] == 0)\
        and (player.object_data["current_sp"] - skill_data[skill_name]["sp_spent"] >= 0 
        or skill_data[skill_name]["sp_spent"] == 0)\
        and (player.object_data["current_ep"] - skill_data[skill_name]["ep_spent"] >= 0 
        or skill_data[skill_name]["ep_spent"] == 0):
            
            hp_change = use_skill_sub(player, skill_data, skill_data[skill_name]["hp_change"])
            target_object.object_data["current_hp"] = min(target_object.object_data["current_hp"] + 
            hp_change,
            target_object.object_data["current_max_hp"])

            mp_change = use_skill_sub(player, skill_data, skill_data[skill_name]["mp_change"])
            target_object.object_data["current_mp"] = min(target_object.object_data["current_mp"] + 
            mp_change,
            target_object.object_data["current_max_mp"])
            
            sp_change = use_skill_sub(player, skill_data, skill_data[skill_name]["sp_change"])
            target_object.object_data["current_sp"] = min(target_object.object_data["current_sp"] + 
            sp_change,
            target_object.object_data["current_max_sp"])

            ep_change = use_skill_sub(player, skill_data, skill_data[skill_name]["ep_change"])
            target_object.object_data["current_ep"] = min(target_object.object_data["current_ep"] + 
            ep_change,
            target_object.object_data["current_max_ep"])
            
            player.object_data["current_hp"]  -= skill_data[skill_name]["hp_spent"]
            player.object_data["current_mp"]  -= skill_data[skill_name]["mp_spent"]
            player.object_data["current_sp"]  -= skill_data[skill_name]["sp_spent"]
            player.object_data["current_ep"]  -= skill_data[skill_name]["ep_spent"] 
                
            return hp_change, mp_change, sp_change, ep_change, False


# Return the value in accordance with the changes of the values.
# TODO: Add the multiplier to the skills.
def use_skill_sub(player,skill_data,changed_value):

    tmp = changed_value
    tmp_name = list(skill_data.keys())[0]
    for i in strength_parameters:
        tmp += changed_value * (uniform(1.0, 1.5) * (player.object_data["current_" + i] * skill_data[tmp_name][i + "_multiplier"]))
    
    return int(round(tmp,0))

# Equip item for player.
# All item data is different.
def equip_item(player, item_data):
    pass