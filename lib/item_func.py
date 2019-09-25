# TODO: Implement temporary status changes.
# TODO: Power up the items as the level goes up...
from random import choice
from functools import reduce
# class Item(object):
#     def __init__(self, item_name,json_data = {}, level = 1):

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
    filtered_skill_data = filter(lambda x: x[list(x.keys())[0]]["level"] <= book_level, skill_data)
    return choice(filtered_skill_data)

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

    
# Equip item for player.
# All item data is different.
def equip_item(player, item_data):
    pass