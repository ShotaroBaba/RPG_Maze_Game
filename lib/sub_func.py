# TODO: Implement temporary status changes.
# TODO: Power up the items as the level goes up...
from random import choice
from random import uniform
from functools import reduce
from getch import _Getch
from maze_object import MazeObject


poison_hp_reduction_rate = 200
getch = _Getch()

starving_ep_reduction_rate = 4
status_effect_decay_rate_in_map = 1
status_effect_decay_rate_in_fight = 10
status_effect_decay_rate_in_fight_pararalyze = 1
status_effect_decay_rate_in_map_paralyze = 1

# class Item(object):
#     def __init__(self, item_name,json_data = {}, level = 1):
strength_parameters =["strength", "agility", "vitality", "dexterity",
                      "smartness", "magic_power", "mental_strength", "luckiness"]

item_change_parameters = ["strength_change","agility_change",
                          "vitality_change","dexterity_change",
                          "smartness_change","magic_power_change",
                          "mental_strength_change","luckiness_change",
                          "hp_change", "mp_change",
                          "ep_change","sp_change"]

# Take level into consideration when creating item
def extract_item_names(item_data):
    if item_data != []:
        return list(map(lambda x: list(x.keys())[0],item_data))
    else:
        return []


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


# Change the effects of items (equipment and expendable)

def alter_item_effects_by_level(tmp_key, tmp_item_json, level = 1):

    tmp = {}
    # All item parameters are changed based on the floor level
    # Generally, it is often to be positive!
    for i in item_change_parameters:
        tmp_item_json[i] = tmp_item_json[i] * (uniform(1,1 + 0.1*level))

    # The item is followed by level.
    tmp_key += f"_{level}"
    tmp[tmp_key] = tmp_item_json

    return tmp

# The skill book gives player to create the 
# Randomly select the skills from skill list.
# Skills are randomly selected based on the book level.
# When a skill book is used, he/she can obtain one skill randomly.
# Player cannot choose his/her skills as he/she wishes from skill books.
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
    hp_changed = mp_changed = sp_changed = ep_changed =\
    poison_changed = curse_changed = seal_changed = paralyze_changed = starving_changed = False
     
    if player.object_data["current_hp"] != player.object_data["current_max_hp"] and item_data[item_name]["hp_change"] != 0:
        player.object_data["current_hp"]  = \
            min(player.object_data["current_hp"]  + item_data[item_name]["hp_change"], player.object_data["current_max_hp"])
        print("hp is recovered by {}".format(item_data[item_name]["hp_change"]))
        hp_changed = True
    
    if player.object_data["current_mp"] != player.object_data["current_max_mp"] and item_data[item_name]["mp_change"] != 0:
        player.object_data["current_mp"]  = \
            min(player.object_data["current_mp"]  + item_data[item_name]["mp_change"], player.object_data["current_max_mp"])
        print("mp is recovered by {}".format(item_data[item_name]["mp_change"]))
        mp_changed = True

    if player.object_data["current_sp"] != player.object_data["current_max_sp"] and item_data[item_name]["sp_change"] != 0:
        player.object_data["current_sp"]  = \
            min(player.object_data["current_sp"]  + item_data[item_name]["sp_change"], player.object_data["current_max_sp"])
        print("sp is recovered by {}".format(item_data[item_name]["sp_change"]))
        sp_changed = True
    
    if player.object_data["current_ep"] != player.object_data["current_max_ep"] and item_data[item_name]["ep_change"] != 0:
        player.object_data["current_ep"]  = \
            min(player.object_data["current_ep"]  + item_data[item_name]["ep_change"], player.object_data["current_max_ep"])
        print("ep is recovered by {}".format(item_data[item_name]["ep_change"]))
        ep_changed = True

    if "poison" in player.object_data["status_effects"] and item_data[item_name]["cure_poison"]:
        player.object_data["status_effects"].remove("poison")
        player.object_data["poison_count"] = 0
        print("Cured poison!")
        poison_changed = True

    if "curse" in player.object_data["status_effects"] and item_data[item_name]["cure_curse"]:
        player.object_data["status_effects"].remove("curse")
        player.object_data["curse_count"] = 0
        print("Cured curse!")
        curse_changed = True

    if "seal" in player.object_data["status_effects"] and item_data[item_name]["cure_seal"]:
        player.object_data["status_effects"].remove("seal")
        player.object_data["seal_count"] = 0
        print("Cured seal!")
        seal_changed = True

    if "paralyze" in player.object_data["status_effects"] and item_data[item_name]["cure_paralyze"]:
        player.object_data["status_effects"].remove("paralyze")
        player.object_data["paralyze_count"] = 0
        print("Cured paralyze!")
        paralyze_changed = True

    if "starving" in player.object_data["status_effects"] and item_data[item_name]["cure_starving"]:
        player.object_data["status_effects"].remove("starving")
        player.object_data["starving_count"] = 0
        print("Cured starving!")
        starving_changed = True

    return hp_changed or mp_changed or sp_changed or ep_changed or\
        poison_changed or curse_changed or seal_changed or paralyze_changed or\
            starving_changed

def remove_status_effects(user:MazeObject, data, name):

    is_removed_status_effect = False
    cured_list = []

    if "poison" in user.object_data["status_effects"] and data[name]["cure_poison"]:
        user.object_data["status_effects"].remove("poison")
        is_removed_status_effect = True
        cured_list.append("poison")
        user.object_data["poison_count"] = 0

    if "curse" in user.object_data["status_effects"] and data[name]["cure_curse"]:
        user.object_data["status_effects"].remove("curse")
        is_removed_status_effect = True
        cured_list.append("curse")
        user.object_data["curse_count"] = 0

    if "seal" in user.object_data["status_effects"] and data[name]["cure_seal"]:
        user.object_data["status_effects"].remove("seal")
        is_removed_status_effect = True
        cured_list.append("seal")
        user.object_data["seal_count"] = 0

    if "paralyze" in user.object_data["status_effects"] and data[name]["cure_paralyze"]:
        user.object_data["status_effects"].remove("paralyze")
        is_removed_status_effect = True
        cured_list.append("paralyze")
        user.object_data["paralyze_count"] = 0

    if "starving" in user.object_data["status_effects"] and data[name]["cure_starving"]:
        user.object_data["status_effects"].remove("starving")
        is_removed_status_effect = True
        cured_list.append("starving")
        user.object_data["starving_count"] = 0

    return is_removed_status_effect, cured_list

# The infliction of status effects on either player or enemy.
def add_target_status_effect(target:MazeObject, skill_data, skill_name):
    
    # TODO: Calculate the possibility of status infliction.

    if skill_data[skill_name]["poison_possibility"] > uniform(0, 1.0):
        if not "poison" in target.object_data["status_effects"]:
            target.object_data["status_effects"].append("poison")
        target.object_data["poison_count"] = 100

    if skill_data[skill_name]["curse_possibility"] > uniform(0, 1.0):
        if not "curse" in target.object_data["status_effects"]:
            target.object_data["status_effects"].append("curse")
        target.object_data["curse_count"] = 100
    
    if skill_data[skill_name]["seal_possibility"] > uniform(0, 1.0):
        if not "seal" in target.object_data["status_effects"]:
            target.object_data["status_effects"].append("seal")
        target.object_data["seal_count"] = 200
    
    if skill_data[skill_name]["paralyze_possibility"] > uniform(0, 1.0):
        if not "paralyze" in target.object_data["status_effects"]:
            target.object_data["status_effects"].append("paralyze")
        target.object_data["paralyze_count"] = 5

    if skill_data[skill_name]["starving_possibility"] > uniform(0, 1.0):
        if not "starving" in target.object_data["status_effects"]:
            target.object_data["status_effects"].append("starving")
        target.object_data["starving_count"] = 200

def use_skill(skill_user, skill_data, target = None, is_in_menu = True):
    
    # TODO: Do not use item when a current value is the same as a maximum value
    skill_name = list(skill_data.keys())[0]

    # If "seal" effect is active, then the 
    if "seal" in skill_user.object_data["status_effects"]:
        print("Cannot use skill in seal condition!")
        getch()
        return False

    if is_in_menu and skill_data[skill_name]["is_in_fight"]:
        print("This skill cannot be used in the player's menu.")
        getch()
        return False

    # Heal or alter player's status.
    # When enemy us`ing the skill, whether skill is used in main menu must be considered
    # Status change is applied to
    elif not skill_data[skill_name]["is_in_fight"]:
        if not is_in_menu or (skill_user.object_data["current_hp"] - skill_data[skill_name]["hp_spent"] >= 0 
        or skill_data[skill_name]["hp_spent"] == 0)\
        and (skill_user.object_data["current_mp"] - skill_data[skill_name]["mp_spent"] >= 0 
        or skill_data[skill_name]["mp_spent"] == 0)\
        and (skill_user.object_data["current_sp"] - skill_data[skill_name]["sp_spent"] >= 0 
        or skill_data[skill_name]["sp_spent"] == 0)\
        and (skill_user.object_data["current_ep"] - skill_data[skill_name]["ep_spent"] >= 0 
        or skill_data[skill_name]["ep_spent"] == 0):

            is_status_removed, removed_list = remove_status_effects(skill_user, skill_data, skill_name)

            if not is_in_menu or (skill_user.object_data["current_hp"] != skill_user.object_data["current_max_hp"] 
            and skill_data[skill_name]["hp_change"] != 0)\
            or (skill_user.object_data["current_mp"] != skill_user.object_data["current_max_mp"] 
            and skill_data[skill_name]["mp_change"] != 0)\
            or (skill_user.object_data["current_sp"] != skill_user.object_data["current_max_sp"] 
            and skill_data[skill_name]["sp_change"] != 0)\
            or (skill_user.object_data["current_ep"] != skill_user.object_data["current_max_ep"] 
            and skill_data[skill_name]["ep_change"] != 0)\
            or is_status_removed:

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

                if removed_list != []:
                    print("Cured {0}!".format(", ".join(removed_list)))

                return hp_change, mp_change, sp_change, ep_change, True
    
    # Player can be the person who receive the damage from enemy.
    # TODO: Add the status effects on the enemy.
    # If player is in fight, then it will perform the attack against enemy.
    elif skill_data[skill_name]["is_in_fight"] and target != None:
        if not is_in_menu or (skill_user.object_data["current_hp"] - skill_data[skill_name]["hp_spent"] >= 0 
        or skill_data[skill_name]["hp_spent"] == 0)\
        and (skill_user.object_data["current_mp"] - skill_data[skill_name]["mp_spent"] >= 0 
        or skill_data[skill_name]["mp_spent"] == 0)\
        and (skill_user.object_data["current_sp"] - skill_data[skill_name]["sp_spent"] >= 0 
        or skill_data[skill_name]["sp_spent"] == 0)\
        and (skill_user.object_data["current_ep"] - skill_data[skill_name]["ep_spent"] >= 0 
        or skill_data[skill_name]["ep_spent"] == 0):
            
            hp_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["hp_change"])
            target.object_data["current_hp"] = min(target.object_data["current_hp"] + 
            hp_change,
            target.object_data["current_max_hp"])

            mp_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["mp_change"])
            target.object_data["current_mp"] = min(target.object_data["current_mp"] + 
            mp_change,
            target.object_data["current_max_mp"])
            
            sp_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["sp_change"])
            target.object_data["current_sp"] = min(target.object_data["current_sp"] + 
            sp_change,
            target.object_data["current_max_sp"])

            ep_change = _use_skill_sub(skill_user, skill_data, skill_data[skill_name]["ep_change"])
            target.object_data["current_ep"] = min(target.object_data["current_ep"] + 
            ep_change,
            target.object_data["current_max_ep"])
            
            skill_user.object_data["current_hp"]  -= skill_data[skill_name]["hp_spent"]
            skill_user.object_data["current_mp"]  -= skill_data[skill_name]["mp_spent"]
            skill_user.object_data["current_sp"]  -= skill_data[skill_name]["sp_spent"]
            skill_user.object_data["current_ep"]  -= skill_data[skill_name]["ep_spent"] 
            
            # Remove status effects from users.
            remove_status_effects(skill_user, skill_data, skill_name)
            
            # Inflict status effects on player or enemy.
            add_target_status_effect(target, skill_data,skill_name)

            # Inflict the status effect on user.
            return hp_change, mp_change, sp_change, ep_change, False

    

# Return the value in accordance with the changes of the values.
# TODO: Add the multiplier to the skills.
def _use_skill_sub(player,skill_data,changed_value):

    # Initialise the values
    tmp = 0
    tmp_name = list(skill_data.keys())[0]
    for i in strength_parameters:
        tmp += changed_value * (uniform(0.8, 1.0) * (player.object_data["current_" + i] * skill_data[tmp_name][i + "_multiplier"]))
    
    return int(round(tmp,0))

# NOTE: The following methods are only for debugging purposes.
# Shows all the contents of data...
def display_debug_status(obj):
    # Print all json-formatted player's data:
    print(obj.object_data)