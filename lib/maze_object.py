from random import choice
from random import uniform

numerical_player_strengh = ["hp", "mp", "sp", "ep"]
current_numerical_player_strength = ["current_hp", "current_mp", "current_sp", "current_ep"]
current_maximum_player_strength = ["current_max_hp", "current_max_mp", "current_max_sp", "current_max_ep"]

non_numerical_player_strength = ["strength", "agility", "vitality", "dexterity", "smartness", "magic_power", "mental_strength", "luckiness"] 
non_numerical_current_player_strength =   ["current_strength", "current_agility", "current_vitality", "current_dexterity",
                                           "current_smartness", "current_magic_power", "current_mental_strength", "current_luckiness"]

equipment_body_part_list  = ["head", "arm", "leg", "body_armor", "right_wrist", "left_wrist", "right_finger", "left_finger"]

poison_hp_reduction_rate = 0.005
starving_ep_reduction_rate = 4
status_effect_decay_rate_in_map = 1
status_effect_decay_rate_in_fight = 10
status_effect_decay_rate_in_fight_pararalyze = 1
status_effect_decay_rate_in_map_paralyze = 1


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
        
        # Pure basic value for player's status.
        # hp: Hit point
        # mp: Magic point
        # sp: Stamina point
        # ep: Energy point
        self.object_data["hp"] = return_json_value_data("hp", 100, json_data, level, is_random)
        self.object_data["mp"]  = return_json_value_data("mp", 100, json_data, level, is_random)
        self.object_data["sp"] = return_json_value_data("sp", 100, json_data, level, is_random)
        self.object_data["ep"] = return_json_value_data("ep", 100, json_data, level, is_random)

        # Define current max point for player.
        self.object_data["current_max_hp"] = json_data["current_max_hp"]\
            if json_data != {} and "current_max_hp" in json_data else self.object_data["hp"]
        self.object_data["current_max_mp"]  = json_data["current_max_mp"]\
            if json_data != {} and "current_max_mp" in json_data else self.object_data["mp"]
        self.object_data["current_max_sp"]  = json_data["current_max_sp"]\
            if json_data != {} and "current_max_sp" in json_data else self.object_data["sp"]
        self.object_data["current_max_ep"]  = json_data["current_max_ep"]\
            if json_data != {} and "current_max_ep" in json_data else self.object_data["ep"]


        self.object_data["current_hp"] = json_data["current_hp"] if json_data != {} and "current_hp" in json_data else self.object_data["hp"]
        self.object_data["current_mp"]  = json_data["current_mp"] if json_data != {} and "current_sp" in json_data else self.object_data["mp"]
        self.object_data["current_sp"]  = json_data["current_sp"] if json_data != {} and "current_mp" in json_data else self.object_data["sp"]
        self.object_data["current_ep"]  = json_data["current_ep"] if json_data != {} and "current_ep" in json_data else self.object_data["ep"]


        # Object's parameters
        self.object_data["strength"] = return_json_value_data("strength", 10, json_data, level, is_random)
        self.object_data["agility"] = return_json_value_data("agility", 10, json_data, level, is_random)
        self.object_data["vitality"] = return_json_value_data("vitality", 10, json_data, level, is_random)
        self.object_data["dexterity"] = return_json_value_data("dexterity", 10, json_data, level, is_random)

        self.object_data["smartness"] = return_json_value_data("smartness", 10, json_data, level, is_random)
        self.object_data["magic_power"] = return_json_value_data("magic_power", 10, json_data, level, is_random)
        self.object_data["mental_strength"] = return_json_value_data("mental_strength", 10, json_data, level, is_random)
        self.object_data["luckiness"]  = return_json_value_data("luckiness", 10, json_data, level, is_random)

        # Object's parameters
        self.object_data["current_strength"] = self.object_data["strength"]
        self.object_data["current_agility"] = self.object_data["agility"]
        self.object_data["current_vitality"] = self.object_data["vitality"]
        self.object_data["current_dexterity"] = self.object_data["dexterity"]

        self.object_data["current_smartness"] = self.object_data["smartness"]
        self.object_data["current_magic_power"] = self.object_data["magic_power"]
        self.object_data["current_mental_strength"] = self.object_data["mental_strength"]
        self.object_data["current_luckiness"]  = self.object_data["luckiness"]

        # The resistance of the potential status effects.
        self.object_data["poison_resist"] = json_data["poison_resist"]\
            if json_data != {} and "poison_resist" in json_data.keys() else 0
        self.object_data["paralyze_resist"] = json_data["paralyze_resist"]\
            if json_data != {} and "paralyze_resist" in json_data.keys() else 0
        self.object_data["curse_resist"] = json_data["curse_resist"]\
            if json_data != {} and "curse_resist" in json_data.keys() else 0
        self.object_data["seal_resist"] = json_data["seal_resist"]\
            if json_data != {} and "seal_resist" in json_data.keys() else 0
        self.object_data["starving_resist"] = json_data["starving_resist"]\
            if json_data != {} and "starving_resist" in json_data.keys() else 0

        # The count showing the effective duration of status effects.
        self.object_data["poison_count"] = json_data["poison_count"]\
            if json_data != {} and "poison_count" in json_data.keys() else 0
        self.object_data["paralyze_count"] = json_data["paralyze_count"]\
            if json_data != {} and "paralyze_count" in json_data.keys() else 0
        self.object_data["curse_count"] = json_data["curse_count"]\
            if json_data != {} and "curse_count" in json_data.keys() else 0
        self.object_data["seal_count"] = json_data["seal_count"]\
            if json_data != {} and "seal_count" in json_data.keys() else 0
        self.object_data["starving_count"] = json_data["starving_count"]\
            if json_data != {} and "starving_count" in json_data.keys() else 0

        self.object_data["unable_to_use_skill"] = json_data["unable_to_use_skill"]\
            if json_data != {} and "unable_to_use_skill" in json_data.keys() else False
        self.object_data["cannot_act"] = json_data["cannot_act"]\
            if json_data != {} and "cannot_act" in json_data.keys() else False

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
        self.object_data["hand"]  = json_data["hand"]\
            if json_data != {} and "hand" in json_data.keys() else []
        self.object_data["head"]  = json_data["head"]\
            if json_data != {} and "head" in json_data.keys() else []
        self.object_data["arm"]  =  json_data["arm"]\
            if json_data != {} and "arm" in json_data.keys() else []
        self.object_data["leg"]  = json_data["leg"]\
            if json_data != {} and "leg" in json_data.keys() else []
        self.object_data["body_armor"]  = json_data["body_armor"]\
            if json_data != {} and "body_armor" in json_data.keys() else []

        
        self.object_data["right_wrist"]  = json_data["right_wrist"]\
            if json_data != {} and "right_wrist" in json_data.keys() else []
        self.object_data["left_wrist"]  = json_data["left_wrist"]\
            if json_data != {} and "left_wrist" in json_data.keys() else []
        self.object_data["right_finger"]  = json_data["right_finger"]\
            if json_data != {} and "right_finger" in json_data.keys() else []
        self.object_data["left_finger"]  = json_data["left_finger"]\
            if json_data != {} and "left_finger" in json_data.keys() else []

        # Status is normal by default
        # if the status is normal, then the player is not affected.
        self.object_data["status_effects"]  = json_data["status_effects"]\
            if json_data != {} and "status_effects" in json_data.keys() else []

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
        # TODO: Implement the idea of rank.
        self.object_data["rank"]  = json_data["rank"]\
            if json_data != {} and "rank" in json_data.keys() else {}

        # The monster will drop the item
        self.object_data["drop_item"]  = json_data["drop_item"]\
            if json_data != {} and "drop_item" in json_data.keys() else {}

    
    # Update values everytime the player walks or level-up.
    # TODO: Added several features later...
    # Player added
    def update_object(self):
        
        ##################################
        # Initialization part
        ##################################
        # Initialise weight limit.
        self.object_data["weight"] = 0

        # Initialise before assigning the value...
        for j in numerical_player_strengh:
            self.object_data["current_max_" + j] = self.object_data[j]
        
        
        ##################################
        # Calculation part.
        ##################################
        # For each body part list
        for i in equipment_body_part_list:
            
            
            # if the body part is not empty, then...
            if self.object_data[i] != []:
                # Firstly, initialise the value.
                for j in numerical_player_strengh:
                    item_name = list(self.object_data[i].keys())[0]
                    self.object_data["current_max_" + j] += self.object_data[i][item_name][j + "_change"]
                
                for j in non_numerical_player_strength:
                    item_name = list(self.object_data[i].keys())[0]
                    self.object_data["current_" + j] += self.object_data[i][item_name][j + "_change"]

                
                self.object_data["weight"] +=  self.object_data[i][item_name]["weight"]


        # TODO: Add the "weight" function.
        # By default, the player has 20 base + strength unit.
        self.object_data["weight_limit"] = 10 + int(self.object_data["strength"] // (1.5 + self.object_data["strength"] // 20))

        for i in range(len(self.object_data["items"])):
            item_in_list = self.object_data["items"][i]
            item_name = list(item_in_list.keys())[0]

            self.object_data["weight"] +=  self.object_data["items"][i][item_name]["weight"]

    def move_update_object(self):
        # If exceed the limit, the hp continues to decrease until the weight losses into a certain amount.
        self.object_data["current_hp"] -= max(self.object_data["weight"] - self.object_data["weight_limit"], 0)


    # The system of the calculation of the level
    def _get_experience(self, exp_values):

        self.object_data["current_exp"] += exp_values
        self.object_data["next_exp"] -= exp_values

        # If the experience reaches another limits, then 
        # player can go up two or more levels.
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
            for _ in range(5 + 5 * (self.object_data["level"] // 10)):
                tmp_choice = choice(numerical_player_strengh + non_numerical_player_strength)
                
                if tmp_choice in numerical_player_strengh:
                    self.object_data[tmp_choice] += 10
                    print("The {} value increases by 10!".format(tmp_choice))
                else:
                    self.object_data[tmp_choice] += 1
                    print("The {} value increases by 1!".format(tmp_choice))

                
            # The formula for calculating the experice for leveling up player.
            self.object_data["next_exp"] = 50 + int(round(50 * (0.5 * (self.object_data["level"] ** (constant_next_level_exp))))) - remain

            self.update_object()

    # NOTE: This function is firstly invoked before the status is updated everytime the player walk
    # on the field. This function puts the status effects on characters or creatures on Maze.
    def affect_player_status(self):
        
        # Firstly, put all status normal before getting into the status effects.
        self.object_data["current_strength"] = self.object_data["strength"]
        self.object_data["current_vitality"] = self.object_data["vitality"]
        self.object_data["current_dexterity"] = self.object_data["dexterity"]
        self.object_data["current_agility"] = self.object_data["agility"]
        self.object_data["current_smartness"] = self.object_data["smartness"]
        self.object_data["current_magic_power"] = self.object_data["magic_power"]
        self.object_data["current_mental_strength"] = self.object_data["mental_strength"]
        self.object_data["current_luckiness"] = self.object_data["luckiness"]
        self.object_data["unable_to_use_skill"] = False
        self.object_data["cannot_act"] = False

        # This effects is effective until its development is over,
        # The status effects can be multiple.
        
        # Object hp decrases gradually
        if "poison" in self.object_data["status_effects"]:
            # HP becomes zero
            self.object_data["current_hp"] -= min(1, 
                1 + round(self.object_data["current_hp"] * poison_hp_reduction_rate, 0))
        
        # All object's status becomes half.
        if "curse" in self.object_data["status_effects"]:
            self.object_data["current_strength"] = self.object_data["strength"] // 2
            self.object_data["current_vitality"] = self.object_data["vitality"] // 2
            self.object_data["current_dexterity"] = self.object_data["dexterity"] // 2
            self.object_data["current_agility"] = self.object_data["agility"] // 2

            self.object_data["current_smartness"] = self.object_data["smartness"] // 2
            self.object_data["current_magic_power"] = self.object_data["magic_power"] // 2
            self.object_data["current_mental_strength"] = self.object_data["mental_strength"] // 2
            self.object_data["current_luckiness"] = self.object_data["luckiness"] // 2
        
        # Objects are unable to use their skills.
        if "seal" in self.object_data["status_effects"]:
            self.object_data["unable_to_use_skill"] = True

        # Object cannot move and act for a certain amount of time.
        if "paralyzed" in self.object_data["status_effects"]:
            self.object_data["cannot_act"] = True 


    def update_status_effect_in_map(self):
        self.object_data["poison_count"] = max(0, 
        self.object_data["poison_count"] - status_effect_decay_rate_in_map)
        
        self.object_data["paralyze_count"] = max(0,
        self.object_data["paralyze_count"] - status_effect_decay_rate_in_map_paralyze)
        
        self.object_data["curse_count"] = max(0, 
        self.object_data["curse_count"] - status_effect_decay_rate_in_map)

        self.object_data["seal_count"] = max(0, 
        self.object_data["seal_count"] - status_effect_decay_rate_in_map)

        self.object_data["starving_count"] = max(0, 
        self.object_data["starving_count"] - status_effect_decay_rate_in_map)

        # Object hp decrases gradually.
        if "poison" in self.object_data["status_effects"] and  self.object_data["poison_count"] == 0:
            self.object_data["status_effects"].remove("poison")

        # Object cannot move.
        if "paralyze" in self.object_data["status_effects"] and  self.object_data["paralyze_count"] == 0:
            self.object_data["status_effects"].remove("paralyze")
        
        # Object is cursed, meaning that the status is reduced to half.
        if "curse" in self.object_data["status_effects"] and  self.object_data["curse_count"] == 0:
            self.object_data["status_effects"].remove("curse")

        # Object cannot use magic & skills
        if "seal" in self.object_data["status_effects"] and  self.object_data["seal_count"] == 0:
            self.object_data["status_effects"].remove("seal")

        # Object starved & reduction of stamina gets faster!
        if "starving" in self.object_data["status_effects"] and  self.object_data["starving_count"] == 0:
            self.object_data["status_effects"].remove("starving")

        self.affect_player_status()

    def update_status_effect_in_fight(self):
        self.object_data["poison_count"] = max(0, 
        self.object_data["poison_count"] - status_effect_decay_rate_in_fight)
        
        self.object_data["paralyze_count"] = max(0,
        self.object_data["paralyze_count"] - status_effect_decay_rate_in_fight_pararalyze)
        
        self.object_data["curse_count"] = max(0, 
        self.object_data["curse_count"] - status_effect_decay_rate_in_fight)

        self.object_data["seal_count"] = max(0, 
        self.object_data["seal_count"] - status_effect_decay_rate_in_fight)

        self.object_data["starving_count"] = max(0, 
        self.object_data["starving_count"] - status_effect_decay_rate_in_fight)

        # Object hp decrases gradually
        if "poison" in self.object_data["status_effects"] and  self.object_data["poison_count"] == 0:
            self.object_data["status_effects"].remove("poison")

        # Object hp decrases gradually
        if "paralyze" in self.object_data["status_effects"] and  self.object_data["paralyze_count"] == 0:
            self.object_data["status_effects"].remove("paralyze")
        
        # Object hp decrases gradually
        if "curse" in self.object_data["status_effects"] and  self.object_data["curse_count"] == 0:
            self.object_data["status_effects"].remove("curse")

        # Object hp decrases gradually
        if "seal" in self.object_data["status_effects"] and  self.object_data["seal_count"] == 0:
            self.object_data["status_effects"].remove("seal")

        # Object hp decrases gradually
        if "starving" in self.object_data["status_effects"] and  self.object_data["starving_count"] == 0:
            self.object_data["status_effects"].remove("starving")

        self.affect_player_status()
    
    # Put all debug methods below!
    # The following is for the debugging methods for status effects:
    def _reduce_all_status_effects_counts_debug(self):
        self.object_data["poison_count"] = 1
        self.object_data["paralyze_count"] = 1
        self.object_data["curse_count"] = 1
        self.object_data["seal_count"] = 1
        self.object_data["starving_count"] = 1 

        print("All status count is set to 1!!!")
        pass
