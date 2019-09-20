
# Item has a number of effects.

# TODO: Implement temporary status changes.

# TODO: Power up the items as the level goes up...

class Item(object):
    def __init__(self, item_name,json_data = {}, level = 1):
        
        # The values of changes of the status values
        self.status_change = ""

        # Item name
        self.item_name = item_name

        # When used, the item will creates the following effects if they have...
        self.hp_change = json_data["hp_change"] if json_data != {} else 0
        self.mp_change = json_data["mp_change"] if json_data != {} else 0
        self.sp_change = json_data["sp_change"] if json_data != {} else 0
        self.ep_change = json_data["ep_change"] if json_data != {} else 0

        self.strength_change = json_data["strength_change"] if json_data != {} else 0
        self.agility_change  = json_data["agility_change"] if json_data != {} else 0
        self.vitality_change  = json_data["vitality_change"] if json_data != {} else 0
        self.dexterity_change  = json_data["dexterity_change"] if json_data != {} else 0

        self.smartness_change  = json_data["smartness_change"] if json_data != {} else 0
        self.magic_power_change  = json_data["magic_power_change"] if json_data != {} else 0
        self.mental_strength_change  = json_data["mental_strength_change"] if json_data != {} else 0
        

        # Luckiness effect changes the possibility of dropping items from enemy.
        self.luckiness = json_data["luckiness_change"] if json_data != {} else 0
        
        # Note: These will be implemented later on.
        self.effective_time = json_data["effective_time"] if json_data != {} and "effective_time" in json_data.keys() else 0
        self.is_cure_all_status = json_data["is_cure_all_status"] if json_data != {} and "is_cure_all_status" in json_data.keys() else False

        self.is_body = json_data["is_body_armor"] if json_data != {} and "is_body_armor" in json_data.keys() else False
        self.is_arm = json_data["is_arm"] if json_data != {} and "is_arm" in json_data.keys() else False 
        self.is_leg = json_data["is_leg"] if json_data != {} and "is_leg" in json_data.keys() else False
        self.is_head = json_data["is_head"] if json_data != {} and "is_head" in json_data.keys() else False

        self.is_wrist = json_data["is_wrist"] if json_data != {} and "is_wrist" in json_data.keys() else False
        self.is_ring = json_data["is_ring"] if json_data != {} and "is_ring" in json_data.keys() else False

        self.durablity_change = json_data["durablity_change"] if json_data != {} and "durability_change" in json_data.keys() else 0

        self.weight = json_data["weight"] if json_data != {} and "weight" in json_data.keys() else 10

    def update_item(self):
        self.effective_time -= 1
    
    # Use item for player.
    def use_item(self, player):
        # TODO: Do not use item when a current value is the same as a maximum value.
        hp_changed = False
        mp_changed = False
        sp_changed = False
        ep_changed = False

        if player.current_hp != player.hp and self.hp_change != 0:
            player.current_hp = min(player.current_hp + self.hp_change, player.hp)
            hp_changed = True
        
        if player.current_mp != player.mp and self.mp_change != 0:
            player.current_mp = min(player.current_mp + self.mp_change,player.mp)
            mp_changed = True
        
        if player.current_sp != player.sp and self.sp_change != 0:
            player.current_sp = min(player.current_sp + self.sp_change,player.sp)
            sp_changed = True
        
        if player.current_ep != player.ep and self.ep_change != 0:
            player.current_ep = min(player.current_ep + self.ep_change,player.ep)
            ep_changed = True
        
        return hp_changed or mp_changed or sp_changed or ep_changed

    # Equip item for player.
    def equip_item(self, player):
        pass