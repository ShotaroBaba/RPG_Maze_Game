# TODO: Implement temporary status changes.
# TODO: Power up the items as the level goes up...

# class Item(object):
#     def __init__(self, item_name,json_data = {}, level = 1):

def update_item(item_data):
    item_data["effective_time"] -= 1

# Use item for player.
def use_item(player,item_name,item_data):

    # TODO: Do not use item when a current value is the same as a maximum value.
    hp_changed = mp_changed = sp_changed = ep_changed = False
     
    if player.object_data["current_hp"] != player.object_data["hp"] and item_data[item_name]["hp_change"] != 0:
        player.object_data["current_hp"]  = \
            min(player.object_data["current_hp"]  + item_data[item_name]["hp_change"], player.object_data["hp"])
        hp_changed = True
    
    if player.object_data["current_mp"] != player.object_data["mp"] and item_data[item_name]["mp_change"] != 0:
        player.object_data["current_mp"]  = \
            min(player.object_data["current_mp"]  + item_data[item_name]["mp_change"], player.object_data["mp"])
        mp_changed = True

    if player.object_data["current_sp"] != player.object_data["sp"] and item_data[item_name]["sp_change"] != 0:
        player.object_data["current_sp"]  = \
            min(player.object_data["current_sp"]  + item_data[item_name]["sp_change"], player.object_data["sp"])
        sp_changed = True
    
    if player.object_data["current_ep"] != player.object_data["ep"] and item_data[item_name]["ep_change"] != 0:
        player.object_data["current_ep"]  = \
            min(player.object_data["current_ep"]  + item_data[item_name]["ep_change"], player.object_data["ep"])
        ep_changed = True

    return hp_changed or mp_changed or sp_changed or ep_changed

    
    # Equip item for player.
    # All item data is different.
    # Equip the 
    def equip_item(player, item_data):
        pass