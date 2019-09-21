from random import choice
from random import uniform

numerical_player_strengh = ["hp", "mp", "sp", "ep"]
current_numerical_player_strength = ["current_hp", "current_mp", "current_sp", "current_ep"]
non_numerical_player_strength = ["strength", "agility", "vitality", "dexterity", "smartness", "magic_power", "mental_strength"]   
equipment_body_part_list  = ["head", "arm", "leg", "body_armor", "right_wrist", "left_wrist", "right_finger", "left_finger"]

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
        
        # Save all player data as an json object.
        self.object_data = {}
        
        # The enemy and player level, which is an important value.
        self.object_data["level"] = json_data["level"] if json_data != {} else 1
        self.object_data["bonus"]  = json_data["bonus"] if json_data !={} and "bonus" in json_data.keys() else 0
        
        #Note: maximum points available
        # hp: Hit point
        # mp: Magic point
        # sp: Stamina point
        # ep: Energy point
        self.object_data["hp"] = return_json_value_data("hp", 100, json_data, level, is_random)
        self.object_data["mp"]  = return_json_value_data("mp", 100, json_data, level, is_random)
        self.object_data["sp"] = return_json_value_data("sp", 100, json_data, level, is_random)
        self.object_data["ep"] = return_json_value_data("ep", 100, json_data, level, is_random)

        self.object_data["current_hp"] = json_data["current_hp"] if json_data != {} and "current_hp" in json_data else self.object_data["hp"]
        self.object_data["current_mp"]  = json_data["current_mp"] if json_data != {} and "current_hp" in json_data else self.object_data["mp"]
        self.object_data["current_sp"]  = json_data["current_sp"] if json_data != {} and "current_hp" in json_data else self.object_data["sp"]
        self.object_data["current_ep"]  = json_data["current_ep"] if json_data != {} and "current_hp" in json_data else self.object_data["ep"]


        # Object's parameters
        self.object_data["strength"] = return_json_value_data("strength", 10, json_data, level, is_random)
        self.object_data["agility"] = return_json_value_data("agility", 10, json_data, level, is_random)
        self.object_data["vitality"] = return_json_value_data("vitality", 10, json_data, level, is_random)
        self.object_data["dexterity"] = return_json_value_data("dexterity", 10, json_data, level, is_random)

        self.object_data["smartness"] = return_json_value_data("smartness", 10, json_data, level, is_random)
        self.object_data["magic_power"] = return_json_value_data("magic_power", 10, json_data, level, is_random)
        self.object_data["mental_strength"] = return_json_value_data("mental_strength", 10, json_data, level, is_random)

        # TODO: Implement luckiness effects
        self.object_data["luckiness"]  = return_json_value_data("luckiness", 10, json_data, level, is_random)

        # Object's parameters
        self.object_data["current_strength"] = self.object_data["strength"]
        self.object_data["current_agility"] = self.object_data["agility"]
        self.object_data["current_vitality"] = self.object_data["vitality"]
        self.object_data["current_dexterity"] = self.object_data["dexterity"]

        self.object_data["current_smartness"] = self.object_data["smartness"]
        self.object_data["current_magic_power"] = self.object_data["magic_power"]
        self.object_data["current_mental_strength"] = self.object_data["mental_strength"]

        # TODO: Implement luckiness effects
        self.object_data["current_luckiness"]  = self.object_data["luckiness"]


        # Check whether it is a player, an enemy or just an object
        self.object_data["player_name"]  = json_data["player_name"]\
            if json_data != {} and "player_name" in json_data.keys() else "None"
        self.object_data["is_living"]  = json_data["is_living"]\
            if json_data != {} and "is_living" in json_data.keys( ) else True
        self.object_data["is_player"]  = json_data["is_player"]\
            if json_data != {} and "is_player" in json_data.keys() else True
        self.object_data["is_enemy"]  = json_data["is_enemy"]\
            if json_data != {} and "is_enemy" in json_data.keys() else  False
        

        # Show the objects that player equips.
        self.object_data["head"]  = json_data["head"]\
            if json_data != {} and "head" in json_data.keys() else {}
        self.object_data["arm"]  =  json_data["arm"]\
            if json_data != {} and "arm" in json_data.keys() else {}
        self.object_data["leg"]  = json_data["leg"]\
            if json_data != {} and "leg" in json_data.keys() else {}
        self.object_data["body_armor"]  = json_data["body_armor"]\
            if json_data != {} and "body_armor" in json_data.keys() else {}

        
        self.object_data["right_wrist"]  = json_data["right_wrist"]\
            if json_data != {} and "right_wrist" in json_data.keys() else {}
        self.object_data["left_wrist"]  = json_data["left_wrist"]\
            if json_data != {} and "left_wrist" in json_data.keys() else {}
        self.object_data["right_finger"]  = json_data["right_finger"]\
            if json_data != {} and "right_finger" in json_data.keys() else {}
        self.object_data["left_finger"]  = json_data["left_finger"]\
            if json_data != {} and "left_finger" in json_data.keys() else {}

        # Initialise paramteres based on player's equipment.
        self._init_parameters_equipment()

        # Status is normal by default
        # if the status is normal, then the player is not affected.
        self.object_data["status"]  = json_data["status"]\
            if json_data != {} and "status" in json_data.keys() else "Normal"

        # By default, the Objects's position is unknown.
        # It is only applied to the player.
        self.object_data["object_pos"]  = json_data["object_pos"]\
            if json_data != {} and "object_pos" in json_data.keys() else None

        # Check how the character is displayed.
        self.object_data["displayed_character"]  = json_data["displayed_character"]\
            if json_data != {} and "displayed_character" in json_data.keys() else "\033[91m" + "@" + "\033[0m"

        # The maximum number of items that Objects can hold
        # It can be increased by the level up.
        self.object_data["max_item_hold"]  = json_data["max_item_hold"]\
            if json_data != {} and "max_item_hold" in json_data.keys() else 10
        
        # Objects's experience point when gaining the points
        self.object_data["exp"]  = int(round(json_data["exp"] * uniform(level-0.2, level+0.2),0))\
            if json_data != {} and "exp" in json_data.keys() else 0

        # Object's current expereince points if available
        # This is only for the player...
        self.object_data["current_exp"]  = json_data["current_exp"]\
            if json_data != {} and "current_exp" in json_data.keys() else 0

        # This is only for the player...
        self.object_data["bonus_point"]  = json_data["bonus_point"]\
            if json_data != {} and "bonus_point" in json_data.keys() else 0

        # Objects's necessary experience points.
        self.object_data["next_exp"]  = json_data["next_exp"]\
            if json_data != {} and "next_exp" in json_data.keys() else 50

        # Item numbers is recorded in the dictionary type
        self.object_data["items"]  = json_data["items"]\
            if json_data != {} and "items" in json_data.keys() else []

        # Item weight limit
        self.object_data["weight_limit"]  = json_data["weight_limit"]\
            if json_data != {} and "weight_limit" in json_data.keys() else\
                10 + int(self.object_data["strength"] // (1.5 + self.object_data["strength"] // 20))
        
        # TODO Create the skill classes for users
        self.object_data["skills"]  = json_data["skills"]\
            if json_data != {} and "skills" in json_data.keys() else []

        # Rank that can be used for adjusting the random encounter in dungeon.
        self.object_data["rank"]  = json_data["rank"]\
            if json_data != {} and "rank" in json_data.keys() else {}

        # The monster will drop the item
        self.object_data["drop_item"]  = json_data["drop_item"]\
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
    # Player added
    def update_object(self):
        # TODO: Add the "weight" function.
        self.object_data["weight_limit"] = 10 + int(self.object_data["strength"] // (1.5 + self.object_data["strength"] // 20))
        for i in equipment_body_part_list:
            if self.object_data != {}:
                pass
            else:
                pass


    # The system of the calculation of the level
    def _get_experience(self, exp_values):

        self.object_data["current_exp"] += exp_values
        self.object_data["next_exp"] -= exp_values

        while self.object_data["next_exp"] < 1:
            remain = self.object_data["next_exp"]
            self.object_data["bonus_point"] += 5 + self.object_data["level"] // 5
            self.object_data["level"] += 1
            
            # Bonus point is added for allowing users to select the ability to improve based on
            # their preference.
            print("Player level up!")
            print("You gained {} bonus points.".format( self.object_data["bonus_point"]))
            print("Player reached to level {}".format(self.object_data["level"]))
            
            # Randomly allocate the values once the level is up
            for _ in range(3 + (self.object_data["level"] // 10)):
                tmp_choice = choice(numerical_player_strengh + non_numerical_player_strength)
                
                if tmp_choice in numerical_player_strengh:
                    self.object_data[tmp_choice] += 5
                    print("The {} value increases by 5!".format(tmp_choice))
                else:
                    self.object_data[tmp_choice] += 1
                    print("The {} value increases by 1!".format(tmp_choice))

                
            # The formula for calculating the experice for leveling up player.
            self.object_data["next_exp"] = 50 + int(round(50 * (0.5 * (self.object_data["level"] ** (constant_next_level_exp))))) - remain