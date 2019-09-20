class Skills(object):

    # The way to initialise the object is to use the JSON object files.    
    def __init__(self, json_data = {}):

        # The spend mp and hp for using skills
        # They are often fixed or random value
        self.hp_change = json_data["hp_change"] if json_data != {} else 100
        self.mp_change = json_data["mp_change"] if json_data != {} else 100
        self.sp_change = json_data["sp_change"] if json_data != {} else 100
        self.ep_change = json_data["ep_change"] if json_data != {} else 100
        self.is_random = None
        
        # Random is FALSE by default
        self.is_random_point_change = False
        self.is_random_skill_points = False

        # Set the skill levels to adjust their effectiveness
        self.skill_level = 0

        # Ignore the effects caused by the values when the skills
        # are activated. It is False by default.
        self.is_skill_points_ignored = False
        self.item_weight = False

        self.random_range = 1.05

        # TODO: Create a part of skills describing upgrade
    # Target can be the persons, or enemies
    def activate_skills(self, target):
        if self.is_random:
            pass
        else:
            pass

# This is an item class, this includes weapon, shields and potions.
# Item might also have the skills in some cases.