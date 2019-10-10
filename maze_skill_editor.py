import sys
import os

import json
from lib.default_values import *
import tkinter as tk

# Maze skill editor
file_path = os.path.join(data_dir,skill_data_file_name)

# NOTE: skills also uses skills to deliver damage and alter their status.
class Application(object):
    def __init__(self):
    
        # Create main window
        self.root = tk.Tk()
        self.root.title("Maze Skill Editor")

        self.menubar = tk.Menu(self.root)
        self.menubar.add_command(label = "Quit", command = self.root.destroy)

        self.root.config(menu=self.menubar)
        # List of parameters that users would like to adjust.
        self.list_of_parameters_right = ["skill_name","hp_change", "mp_change", "sp_change", "ep_change", 
        "strength_change", "agility_change", "vitality_change", "dexterity_change", "smartness_change"]
        
        self.list_of_parameters_middle_1_1 =[
        ("fire", "fire"),
        ("water", "water"),
        ("thunder","thunder"),
        ("light", "light"),
        ("dark", "dark"),
        ("neutral", "neutral")]
            # Object hp decrases gradually
        
        self.list_of_parameters_middle_1_2 = ["poison_possiblity", "curse_possibility", "seal_possibility", "paralyze_possibility",
        "starving_possibility"]

        # Effects that cure negative status effects.
        self.list_of_parameters_middle_3_2 = ["cure_poison", "cure_curse", "cure_seal", "cure_paralyze", "cure_starving"]
        

        self.list_of_parameters_middle_2 = ["strength_multiplier", "agility_multiplier", "vitality_multiplier", "dexterity_multiplier", 
        "smartness_multiplier","magic_power_multiplier","mental_strength_multiplier", "luckiness_multiplier"]
        
        # Temporary status change during the battle.
        self.list_of_parameters_middle_3_1 = ["magic_power_change","mental_strength_change", "luckiness_change", "effective_time", "durablity_change", "weight", "level"]
        self.list_of_parameters_left_2 = ["hp_spent", "mp_spent", "sp_spent", "ep_spent"]
        self.start_window()

    # The list of parameters that users would like to adjust for creating monsters.
    def start_window(self):
        self.skill_list = {}
        try:
            with open(file_path, "r") as f:
                self.skill_list = json.loads(f.read()) 
        except:
            with open(file_path, "a") as f:
                f.close()

        self.main_group = tk.Frame(self.root)
        self.main_group.pack()

        self.main_list_frame = tk.Frame(self.main_group)
        self.main_list_frame.pack(side = tk.TOP)

        # Non-checkbox Frame
        self.main_group_left = tk.Frame(self.main_list_frame)
        self.main_group_left.grid(row = 0, column = 0, padx = 3, pady =3, sticky = tk.N)
        self.main_group_left_2 = tk.Frame(self.main_list_frame)
        self.main_group_left_2.grid(row = 1, column = 0, padx = 3, pady =3, sticky = tk.N)
        
        # Checkbox Frame
        self.main_group_radiobutton_1_1 = tk.Frame(self.main_list_frame)
        self.main_group_radiobutton_1_1.grid(row = 0, column = 1, padx = 3, pady = 3, sticky = tk.N)

        # Non_checkbox (middle part 2)
        self.main_group_status_effects_1_2 = tk.Frame(self.main_list_frame)
        self.main_group_status_effects_1_2.grid(row = 1, column = 1, padx = 3, pady = 3, sticky = tk.N)

        # Checkbox Frame
        self.main_group_radiobutton_1_3 = tk.Frame(self.main_list_frame)
        self.main_group_radiobutton_1_3.grid(row = 0, column = 1, padx = 3, pady = 3, sticky = tk.N)

        # Non-checkbox Frame (middle part 1)
        self.main_group_middle_3_1 = tk.Frame(self.main_list_frame)
        self.main_group_middle_3_1.grid(row = 0, column = 2, padx = 3, pady =3, sticky = tk.N)
        
        # Checkbox frame (middle part 2)
        self.main_group_middle_checkbox_3_2 = tk.Frame(self.main_list_frame)
        self.main_group_middle_checkbox_3_2.grid(row = 1, column = 2, padx = 3, pady = 3, sticky = tk.N)

        # Non-checkbox Frame (middle part e)
        self.main_group_entry_middle_frame_2 = tk.Frame(self.main_list_frame)
        self.main_group_entry_middle_frame_2.grid(row = 0, column = 3, padx = 3, pady =3, sticky = tk.N)

        # Listbox Frame
        self.main_group_list_box_frame = tk.Frame(self.main_list_frame)
        self.main_group_list_box_frame.grid(row = 0, column = 4, padx = 3, pady = 3, sticky = tk.NS)
        self.main_group_list_box_scroll = tk.Scrollbar(self.main_group_list_box_frame)
        
        # Listbox Frame (
        self.main_group_list_box_scroll.pack(side = tk.RIGHT, fill = tk.Y)
        self.main_group_list_box = tk.Listbox(self.main_group_list_box_frame, yscrollcommand = self.main_group_list_box_scroll.set)
        self.main_group_list_box.pack(side = tk.LEFT, fill = tk.Y)

        
        for name in list(self.skill_list.keys()):
            self.main_group_list_box.insert(tk.END, name)

        for i,parameter_list in enumerate(self.list_of_parameters_right):
            exec("""self.{0}_adjust_label = tk.Label(self.main_group_left, text = "{0}: " )""". format(parameter_list))
            exec("self.{0}_adjust_label.grid(row = i, sticky = tk.E,column = 0, padx = 3, pady =1)". format(parameter_list))
            exec("self.{0}_input_box = tk.Entry(self.main_group_left)". format(parameter_list))
            exec("self.{0}_input_box.grid(row = i, column = 1, padx = 10, pady =1)". format(parameter_list))

        for i,parameter_list in enumerate(self.list_of_parameters_middle_1_2):
            exec("""self.{0}_adjust_label = tk.Label(self.main_group_status_effects_1_2, text = "{0}: " )""". format(parameter_list))
            exec("self.{0}_adjust_label.grid(row = i, sticky = tk.E,column = 0, padx = 3, pady =1)". format(parameter_list))
            exec("self.{0}_input_box = tk.Entry(self.main_group_status_effects_1_2)". format(parameter_list))
            exec("self.{0}_input_box.grid(row = i, column = 1, padx = 10, pady =1)". format(parameter_list))

        # Spent mp displayed
        for i,parameter_list in enumerate(self.list_of_parameters_left_2):
            exec("""self.{0}_adjust_label = tk.Label(self.main_group_left_2, text = "{0}: " )""". format(parameter_list))
            exec("self.{0}_adjust_label.grid(row = i, sticky = tk.E,column = 0, padx = 3, pady =1)". format(parameter_list))
            exec("self.{0}_input_box = tk.Entry(self.main_group_left_2)". format(parameter_list))
            exec("self.{0}_input_box.grid(row = i, column = 1, padx = 10, pady =1)". format(parameter_list))

        # Set the radio button.
        self.middle_radio_button_value_1 = tk.StringVar()
        self.middle_radio_button_value_1.set("L") 

        for text, mode in self.list_of_parameters_middle_1_1:
            self.radiobutton_middle_1 = tk.Radiobutton(self.main_group_radiobutton_1_1, text=text,
                            variable=self.middle_radio_button_value_1, value=mode)
            self.radiobutton_middle_1.pack(anchor=tk.W)

        # Set if it can be used in player's menu.
        self.is_in_fight_value = tk.BooleanVar()
        self.checkbutton_if_used_in_menu = tk.Checkbutton(self.main_group_radiobutton_1_1,
        text = "is_in_fight", onvalue = True, offvalue = False, variable = self.is_in_fight_value)
        self.checkbutton_if_used_in_menu.pack(anchor=tk.W)

        for i,parameter_list in enumerate(self.list_of_parameters_middle_2):
            exec("""self.{0}_adjust_label = tk.Label(self.main_group_entry_middle_frame_2, text = "{0}: " )""". format(parameter_list))
            exec("self.{0}_adjust_label.grid(row = i, sticky = tk.E,column = 0, padx = 3, pady =1)". format(parameter_list))
            exec("self.{0}_input_box = tk.Entry(self.main_group_entry_middle_frame_2)". format(parameter_list))
            exec("self.{0}_input_box.grid(row = i, column = 1, padx = 10, pady =1)". format(parameter_list))

        for i,parameter_list in enumerate(self.list_of_parameters_middle_3_1):
            exec("""self.{0}_adjust_label = tk.Label(self.main_group_middle_3_1, text = "{0}: " )""". format(parameter_list))
            exec("self.{0}_adjust_label.grid(row = i, sticky = tk.NE,column = 0, padx = 3, pady =1)". format(parameter_list))
            exec("self.{0}_input_box = tk.Entry(self.main_group_middle_3_1)". format(parameter_list))
            exec("self.{0}_input_box.grid(row = i, column = 1, padx = 10, pady =1, sticky = tk.N)". format(parameter_list))
    
        for i,parameter_list in enumerate(self.list_of_parameters_middle_3_2):
            exec("""self.{0}_value = tk.BooleanVar()""". format(parameter_list))
            exec("""self.{0}_checkbutton = tk.Checkbutton(self.main_group_middle_checkbox_3_2,
        text = "{0}", onvalue = True, offvalue = False, variable = self.{0}_value)""".format(parameter_list))
            exec("self.{0}_checkbutton.pack(anchor=tk.W)". format(parameter_list))

        self.main_group_list_box.bind("<Double-1>", self._load_skill_data)
        self.exit_button = tk.Button(self.main_group, text = "exit", command = exit)
        self.exit_button.pack(side = tk.BOTTOM)
        self.save_button = tk.Button(self.main_group, text = "save", command = self._save_skill_data)
        self.save_button.pack(side = tk.BOTTOM)
        self.root.mainloop()
    
    # Refresh the saved skill data
    def _refresh_saved_skill_data(self):
        # 1. Check folder existence
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)

        # 2. Check file existence
        if not os.path.isfile(file_path):
            open(file_path, 'a').close()

        # Main frame for putting monster
        main_skill_data = {}

        # Get skill name
        main_skill_name = eval("self.skill_name_input_box.get()")
        tmp = {}
        

    def _save_skill_data(self):
        # 1. Check folder existence
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)

        # 2. Check file existence
        if not os.path.isfile(file_path):
            open(file_path, 'a').close()
        
        # Main frame for putting monster
        main_skill_data = {}

        # Get skill name
        main_skill_name = eval("self.skill_name_input_box.get()")
        tmp = {}

        with open(file_path, "r") as f:
            string = f.read()
            if string != "":
                main_skill_data = json.loads(string)
            else:
                main_skill_data = {}

        # Record the attribute 
        tmp["attribute"] = self.middle_radio_button_value_1.get()

        for i in self.list_of_parameters_right[1:] + self.list_of_parameters_middle_3_1 + self.list_of_parameters_left_2 +\
            self.list_of_parameters_middle_1_2:

            exec("tmp[i] = int(self.{0}_input_box.get())".format(i))
        
        for i in self.list_of_parameters_middle_2:
            exec("tmp[i] = float(self.{0}_input_box.get())".format(i))
        
        tmp["is_in_fight"] = self.is_in_fight_value.get()

        for i in self.list_of_parameters_middle_3_2:
            exec("tmp[i] = self.{0}_value.get()".format(i))

        # Put & update the data of main skill data.
        main_skill_data[main_skill_name] = tmp

        with open(file_path, "w") as f:
            f.write(json.dumps(main_skill_data, indent = 4))

        try:
            with open(file_path, "r") as f:
                self.skill_list = json.loads(f.read()) 
        except:
            print("Error when loading the file.")
        
        self.main_group_list_box.delete(0,tk.END)

        for name in self.skill_list.keys():
            self.main_group_list_box.insert(tk.END, name)
        # except :
        #     print("Please input a proper value.")
    
    # Load skill data from selection list.
    def _load_skill_data(self,evt = None, skill_name = None):
        
        w = evt.widget
        idx = int(w.curselection()[0])
        value = w.get(idx)

        self.skill_name_input_box.delete(0,tk.END)
        self.skill_name_input_box.insert(0,value)
    
        for parameter_list in self.list_of_parameters_right[1:]:
            exec("self.{0}_input_box.delete(0,tk.END)".format(parameter_list))
            try:
                exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,self.skill_list[value][parameter_list]))
            except:
                exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,0))
        
        for parameter_list in self.list_of_parameters_middle_3_1:
            exec("self.{0}_input_box.delete(0,tk.END)".format(parameter_list))
            try:
                exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,self.skill_list[value][parameter_list]))
            except:
                exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,0))

        for parameter_list in self.list_of_parameters_left_2:
            exec("self.{0}_input_box.delete(0,tk.END)".format(parameter_list))
            try:
                exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,self.skill_list[value][parameter_list]))
            except:
                exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,0))

        for parameter_list in self.list_of_parameters_middle_2:
            exec("self.{0}_input_box.delete(0,tk.END)".format(parameter_list))
            try:
                exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,self.skill_list[value][parameter_list]))
            except:
                exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,0))

        for parameter_list in self.list_of_parameters_middle_1_2:
            exec("self.{0}_input_box.delete(0,tk.END)".format(parameter_list))
            try:
                exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,self.skill_list[value][parameter_list]))
            except:
                exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,0))

        try:
            self.middle_radio_button_value_1.set(self.skill_list[value]["attribute"])
        except:
            self.middle_radio_button_value_1.set(self.list_of_parameters_middle_1_1[0][0])

        try:
            self.is_in_fight_value.set(self.skill_list[value]["is_in_fight"])
        except:
            self.is_in_fight_value.set(False)
        
        for i in self.list_of_parameters_middle_3_2:
            try:
                exec("self.{0}_value.set(self.skill_list[value][i])".format(i))
            except:
                exec("self.{0}_value.set(False)".format(i))

# Start the application
def main():
    Application()

if __name__ == '__main__':
    main()


