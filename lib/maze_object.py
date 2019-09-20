from random import choice
from random import uniform

numerical_player_strengh = ["hp", "mp", "sp", "ep"]
non_numerical_player_strength = ["strength", "agility", "vitality", "dexterity", "smartness", "magic_power", "mental_strength"]   

# Used for returning a certain value for a certain situation.
# The enemy strength is decided randomly.
def return_json_value_data(key_value, default_value, json_data, level  = 1, is_random = "no"):
    if json_data != {}:
        if is_random == "yes":
            return int(round(json_data[key_value] * uniform(level-0.2, level + 0.2), 0))
        else:
            return json_data[key_value]
    else:
        return default_value

constant_next_level_exp = 1.4

class MazeObject(object):

    # Read the json object to initalise the data, 
    def __init__(self, json_data = {}, level = 1, is_random = "no"):
        
        # The enemy and player level, which is an important value.
        self.level = json_data["level"] if json_data != {} else 1

        self.bonus_point = json_data["bonus"] if json_data !={} and "bonus" in json_data.keys() else 0
        
        #Note: maximum points available
        # hp: Hit point
        # mp: Magic point
        # sp: Stamina point
        # ep: Energy point
        self.hp = return_json_value_data("hp", 100, json_data, level, is_random)
        self.mp = return_json_value_data("mp", 100, json_data, level, is_random)
        self.sp = return_json_value_data("sp", 100, json_data, level, is_random)
        self.ep = return_json_value_data("ep", 100, json_data, level, is_random)

        self.current_hp = json_data["current_hp"] if json_data != {} and "current_hp" in json_data else self.hp
        self.current_mp = json_data["current_mp"] if json_data != {} and "current_hp" in json_data else self.mp
        self.current_sp = json_data["current_sp"] if json_data != {} and "current_hp" in json_data else self.sp
        self.current_ep = json_data["current_ep"] if json_data != {} and "current_hp" in json_data else self.ep


        # Object's parameters
        self.strength = return_json_value_data("strength", 10, json_data, level, is_random)
        self.agility = return_json_value_data("agility", 10, json_data, level, is_random)
        self.vitality = return_json_value_data("vitality", 10, json_data, level, is_random)
        self.dexterity = return_json_value_data("dexterity", 10, json_data, level, is_random)

        self.smartness = return_json_value_data("smartness", 10, json_data, level, is_random)
        self.magic_power = return_json_value_data("magic_power", 10, json_data, level, is_random)
        self.mental_strength = return_json_value_data("mental_strength", 10, json_data, level, is_random)

        # TODO: Implement luckiness effects
        self.luckiness = return_json_value_data("luckiness", 10, json_data, level, is_random)


        # Check whether it is a player, an enemy or just an object
        self.player_name = json_data["player_name"]\
            if json_data != {} and "player_name" in json_data.keys() else "None"
        self.is_living = json_data["is_living"]\
            if json_data != {} and "is_living" in json_data.keys( ) else True
        self.is_player = json_data["is_player"]\
            if json_data != {} and "is_player" in json_data.keys() else True
        self.is_enemy = json_data["is_enemy"]\
            if json_data != {} and "is_enemy" in json_data.keys() else  False
        

        # Show the objects that player wields
        self.head = json_data["head"]\
            if json_data != {} and "head" in json_data.keys() else "Empty"
        self.arm =  json_data["arm"]\
            if json_data != {} and "arm" in json_data.keys() else "Empty"
        self.leg = json_data["leg"]\
            if json_data != {} and "leg" in json_data.keys() else "Empty"
        self.body_armor = json_data["body_armor"]\
            if json_data != {} and "body_armor" in json_data.keys() else "Empty"

        
        self.right_wrist = json_data["right_wrist"]\
            if json_data != {} and "right_wrist" in json_data.keys() else "Empty"
        self.left_wrist = json_data["left_wrist"]\
            if json_data != {} and "left_wrist" in json_data.keys() else "Empty"
        self.right_finger = json_data["right_finger"]\
            if json_data != {} and "right_finger" in json_data.keys() else "Empty"
        self.left_finger = json_data["left_finger"]\
            if json_data != {} and "left_finger" in json_data.keys() else "Empty"

        # Initialise paramteres based on player's equipment.
        self._init_parameters_equipment()

        # Status is normal by default
        # if the status is normal, then the player is not affected.
        self.status = json_data["status"]\
            if json_data != {} and "status" in json_data.keys() else "Normal"

        # By default, the Objects's position is unknown.
        # It is only applied to the player.
        self.object_pos = json_data["object_pos"]\
            if json_data != {} and "object_pos" in json_data.keys() else None

        # Check how the character is displayed.
        self.displayed_character = json_data["displayed_character"]\
            if json_data != {} and "displayed_character" in json_data.keys() else "\033[91m" + "@" + "\033[0m"

        # The maximum number of items that Objects can hold
        # It can be increased by the level up.
        self.max_item_hold = json_data["max_item_hold"]\
            if json_data != {} and "max_item_hold" in json_data.keys() else 10

        # Objects's experience point when gaining the points
        self.exp = int(round(json_data["exp"] * uniform(level-0.2, level+0.2),0))\
            if json_data != {} and "exp" in json_data.keys() else 0

        # Object's current expereince points if available
        # This is only for the player...
        self.current_exp = json_data["current_exp"]\
            if json_data != {} and "current_exp" in json_data.keys() else 0

        # This is only for the player...
        self.bonus_point = json_data["bonus_point"]\
            if json_data != {} and "bonus_point" in json_data.keys() else 0

        # Objects's necessary experience points.
        self.next_exp = json_data["next_exp"]\
            if json_data != {} and "next_exp" in json_data.keys() else 50

        # Item numbers is recorded in the dictionary type
        self.items = json_data["items"]\
            if json_data != {} and "items" in json_data.keys() else []

        # Item weight limit
        self.weight_limit = json_data["weight_limit"]\
            if json_data != {} and "weight_limit" in json_data.keys() else 10 + int(self.strength // (1.5 + self.strength // 20))
        
        # TODO Create the skill classes for users
        self.skills = json_data["skills"]\
            if json_data != {} and "skills" in json_data.keys() else []

        # Rank that can be used for adjusting the random encounter in dungeon.
        self.rank = json_data["rank"]\
            if json_data != {} and "rank" in json_data.keys() else {}

        # The monster will drop the item
        self.drop_item = json_data["drop_item"]\
            if json_data != {} and "drop_item" in json_data.keys() else {}

    # Apply skills to a certain person, enemy or items
    # NOTE: Skills will be a set of json data.
    def use_skills(self, skill_name, target):
        self.skills[skill_name].activate_skills(target)
        pass

    # Adjust parameters based on the equipment
    def _init_parameters_equipment(self):
        pass

    # Player can wear his or her own weapon, accessory or armor
    def attach_item(self, item):
        pass

    # Player can remove his or her own weapon, accessory or armor
    def detach_item(self, item):
        pass

    def _initialise_json(self):
        pass

    # Initialise player when the game is started.
    def initialise_player(self):
        pass

    # Used for generating json data for saving character's data.
    def return_character_data_json(self):
        pass

    # Move characters when the enemy
    def move_object_up(self, key_event):
        pass

    def move_object_down(self, key_event):
        pass

    def move_object_left(self, key_event):
        pass
    
    def move_object_right(self, key_event):
        pass
    
    # Update values everytime the player walks or level-up.
    # TODO: Added several features later...
    def update_object(self):
        self.weight_limit = 10 + int(self.strength // (1.5 + self.strength // 20))
    
    # The system of the calculation of the level
    def _get_experience(self, exp_values):

        self.current_exp += exp_values
        self.next_exp -= exp_values

        while self.next_exp < 1:
            remain = self.next_exp
            self.bonus_point += 5 + self.level // 5
            self.level += 1
            
            # Bonus point is added for allowing users to select the ability to improve based on
            # their preference.
            print("Player level up!")
            print("You gained {} bonus points.".format(self.bonus_point))
            print("Player reached to level {}".format(self.level))
            
            # Randomly allocate the values once the level is up
            for _ in range(3 + (self.level // 10)):
                tmp_choice = choice(numerical_player_strengh + non_numerical_player_strength)
                
                if tmp_choice in numerical_player_strengh:
                    exec("""self.{} += 5""".format(tmp_choice))
                    print("The {} value increases by 5!".format(tmp_choice))
                else:
                    exec("""self.{} += 1""".format(tmp_choice))
                    print("The {} value increases by 1!".format(tmp_choice))

                
            # The formula for calculating the next level.
            self.next_exp = 50 + int(round(50 * (0.5 * (self.level ** (constant_next_level_exp))))) - remain