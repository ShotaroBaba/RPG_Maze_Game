import sys
import os

import json
from lib.default_values import *
import tkinter as tk

file_path = os.path.join(data_dir,creature_data_file_name)

skill_file_path = os.path.join(data_dir, skill_data_file_name)
class Application(object):

    def __init__(self):
    
        # Create main window
        self.root = tk.Tk()
        self.root.title("Maze Creature Editor")

        self.menubar = tk.Menu(self.root)
        self.menubar.add_command(label = "Quit", command = self.root.destroy)

        self.root.config(menu=self.menubar)
        # List of parameters that users would like to adjust.
        self.list_of_parameters_right = ["creature_name", "hp", "mp", "sp", "ep", "strength", 
        "agility", "vitality", "dexterity", "smartness", "magic_power", "mental_strength", "luckiness", "level"]

        self.list_of_parameters_left = ["exp", "drop_item"]

        self.start_window()
    # The list of parameters that users would like to adjust for creating monsters.

    def start_window(self):
        self.raw_skill_data = []
        self.monster_list = []
        self.creature_skill_data = []
        try:
            with open(file_path, "r") as f:
                self.monster_list = json.loads(f.read()) 
        except:
            print("Error when loading the file.")
        
        try:
            with open(skill_file_path, "r") as f:
                self.raw_skill_data = json.loads(f.read())
        except:
            print("Error when loading the skill file")
        
        self.main_group = tk.Frame(self.root)
        self.main_group.pack()

        self.main_list_frame = tk.Frame(self.main_group)
        self.main_list_frame.pack(side = tk.TOP)

        # Left-hand side
        self.main_group_left = tk.Frame(self.main_list_frame)
        self.main_group_left.grid(row = 0, column = 0, padx = 3, pady =3, sticky = tk.N)

        for i,parameter_list in enumerate(self.list_of_parameters_right):
            exec("""self.{0}_adjust_label = tk.Label(self.main_group_left, text = "{0}: " )""". format(parameter_list))
            exec("self.{0}_adjust_label.grid(row = i, sticky = tk.E,column = 0, padx = 3, pady =1)". format(parameter_list))
            exec("self.{0}_input_box = tk.Entry(self.main_group_left)". format(parameter_list))
            exec("self.{0}_input_box.grid(row = i, column = 1, padx = 10, pady =1)". format(parameter_list))

        # Right hand side: parameter 
        self.main_group_middle_1 = tk.Frame(self.main_list_frame)
        self.main_group_middle_1.grid(row = 0, column = 1, padx = 3, pady =3, sticky = tk.N)
        
        for i,parameter_list in enumerate(self.list_of_parameters_left):
            exec("""self.{0}_adjust_label = tk.Label(self.main_group_middle_1, text = "{0}: " )""". format(parameter_list))
            exec("self.{0}_adjust_label.grid(row = i, sticky = tk.NE,column = 0, padx = 3, pady =1)". format(parameter_list))
            exec("self.{0}_input_box = tk.Entry(self.main_group_middle_1)". format(parameter_list))
            exec("self.{0}_input_box.grid(row = i, column = 1, padx = 10, pady =1, sticky = tk.N)". format(parameter_list))

        self.main_group_middle_2 = tk.Frame(self.main_list_frame)
        self.main_group_middle_2.grid(row = 0, column = 2, padx = 3, pady = 3, sticky = tk.N)

        # Middle of the line
        # Right hand side: parameter 
        self.main_group_middle_2_1 = tk.Frame(self.main_group_middle_2)
        self.main_group_middle_2_1.grid(row = 0, column = 0, padx = 3, pady =3, sticky = tk.N)
        
        # Creature skill data.
        self.main_group_list_box_scroll_creature_skill_creature_data_label = tk.Label(self.main_group_middle_2_1, text = "Creature skills")
        self.main_group_list_box_scroll_creature_skill_creature_data_label.pack(anchor = tk.CENTER)
        self.main_group_list_box_scroll_creature_skill_data = tk.Scrollbar(self.main_group_middle_2_1)
        self.main_group_list_box_scroll_creature_skill_data.pack(side = tk.RIGHT, fill = tk.Y)
        self.main_group_list_box_creature_skill_data = tk.Listbox(self.main_group_middle_2_1, yscrollcommand = self.main_group_list_box_scroll_creature_skill_data.set)
        self.main_group_list_box_creature_skill_data.pack(side = tk.LEFT, fill = tk.Y)
        
        self.main_group_list_box_creature_skill_data.bind("<Double-1>", self._delete_creature_skill)

        # Right hand side: parameter 
        self.main_group_middle_2_2 = tk.Frame(self.main_group_middle_2)
        self.main_group_middle_2_2.grid(row = 1, column = 0, padx = 3, pady =3, sticky = tk.N)

        # Skill list to input creature.
        self.main_group_list_box_scroll_raw_skill_label = tk.Label(self.main_group_middle_2_2, text = "Skill list to put")
        self.main_group_list_box_scroll_raw_skill_label.pack(anchor = tk.CENTER)
        self.main_group_list_box_scroll_raw_skill_list = tk.Scrollbar(self.main_group_middle_2_2)
        self.main_group_list_box_scroll_raw_skill_list.pack(side = tk.RIGHT, fill = tk.Y)
        self.main_group_list_box_raw_skill_list = tk.Listbox(self.main_group_middle_2_2, yscrollcommand = self.main_group_list_box_scroll_raw_skill_list.set)
        self.main_group_list_box_raw_skill_list.pack(side = tk.LEFT, fill = tk.Y)

        # By double clicking, the skill data will be inserted into the creature.
        self.main_group_list_box_raw_skill_list.bind("<Double-1>", self._insert_creature_skill)

        # Most right hand side: Listbox
        self.main_group_right = tk.Frame(self.main_list_frame)
        self.main_group_right.grid(row = 0, column = 3, padx = 3, pady = 3, sticky = tk.NS)

        # Creature data list.
        self.main_group_list_box_scroll_creature_data = tk.Scrollbar(self.main_group_right)
        self.main_group_list_box_scroll_creature_data.pack(side = tk.RIGHT, fill = tk.Y)
        self.main_group_list_box_creature_data = tk.Listbox(self.main_group_right, yscrollcommand = self.main_group_list_box_scroll_creature_data.set)
        self.main_group_list_box_creature_data.pack(side = tk.LEFT, fill = tk.Y)
        
        # Double click will load the creature's data.
        self.main_group_list_box_creature_data.bind("<Double-1>", self._load_creature_data)

        for name in list(self.monster_list.keys()):
            self.main_group_list_box_creature_data.insert(tk.END, name)


        self.exit_button = tk.Button(self.main_group, text = "exit", command = exit)
        self.exit_button.pack(side = tk.BOTTOM)

        self.save_button = tk.Button(self.main_group, text = "save", command = self._save_creature_data)
        self.save_button.pack(side = tk.BOTTOM)
        
        # Put all skill data from the start.
        for i in self.raw_skill_data.keys():
            self.main_group_list_box_raw_skill_list.insert(tk.END, i)

        self.root.mainloop()
    
    # Insert creature skills by double clicking it.
    def _insert_creature_skill(self,evt):

        w = evt.widget
        idx = int(w.curselection()[0])
        value = w.get(idx)
        
        # If there is a skill already, then it will remove the file.
        if value in self.main_group_list_box_creature_skill_data.get(0, tk.END):
            return

        self.main_group_list_box_creature_skill_data.insert(tk.END, value)
        tmp = {}
        tmp[value] = self.raw_skill_data[value]


    def _delete_creature_skill(self,evt):

        # Delete creature skill data.
        self.main_group_list_box_creature_skill_data.delete(tk.ANCHOR)


    def _save_creature_data(self):
        # 1. Check folder existence
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)

        # 2. Check file existence
        if not os.path.isfile(file_path):
            open(file_path, 'a').close()
        
        # Main frame for putting monster
        main_creature_data = {}

        # Get creature name
        main_creature_name = eval("self.creature_name_input_box.get()")
        tmp = {}

        with open(file_path, "r") as f:
            string = f.read()
            if string != "":
                main_creature_data = json.loads(string)
            else:
                main_creature_data = {}

        # try:
            # Check whether the game data exist...

        for i in self.list_of_parameters_right[1:]:
            exec("tmp[i] = int(self.{0}_input_box.get())".format(i))

        exec("""tmp["{0}"] = self.{0}_input_box.get()""".format("drop_item"))
        exec("""tmp["{0}"] = int(self.{0}_input_box.get())""".format("exp"))
        
        # Initialise skills
        tmp["skills"] = []

        for i in self.main_group_list_box_creature_skill_data.get(0, tk.END):
            tmp_skill = {}
            tmp_skill[i] = self.raw_skill_data[i]
            tmp["skills"].append(tmp_skill)
     
        # Put & update the data of main creature data.
        main_creature_data[main_creature_name] = tmp

        with open(file_path, "w") as f:
            f.write(json.dumps(main_creature_data, indent = 4))
            
        # Reload the list after saving creature data.
        
        try:
            with open(file_path, "r") as f:
                self.monster_list = json.loads(f.read()) 
        except:
            print("Error when loading the file.")
        
        # Refresh the creature's data and load the name of the creature.
        self.main_group_list_box_creature_data.delete(0,tk.END)

        for name in self.monster_list.keys():
            self.main_group_list_box_creature_data.insert(tk.END, name)

    # Load creature data from selection list.
    def _load_creature_data(self,evt):
        
        w = evt.widget
        idx = int(w.curselection()[0])
        value = w.get(idx)

        self.creature_name_input_box.delete(0,tk.END)
        self.creature_name_input_box.insert(0,value)
    
        for parameter_list in self.list_of_parameters_right[1:]:
            exec("self.{0}_input_box.delete(0,tk.END)".format(parameter_list))
            exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,self.monster_list[value][parameter_list]))
        
        for parameter_list in self.list_of_parameters_left[:-1]:
            exec("self.{0}_input_box.delete(0,tk.END)".format(parameter_list))
            exec("self.{0}_input_box.insert(0,{1})".format(parameter_list,self.monster_list[value][parameter_list]))
        
        exec("""self.{0}_input_box.delete(0, tk.END)""".format("drop_item"))
        exec("""self.{0}_input_box.insert(0,"{1}")""".format("drop_item", self.monster_list[value]["drop_item"]))
        
        exec("""self.{0}_input_box.delete(0, tk.END)""".format("exp"))
        exec("""self.{0}_input_box.insert(0,"{1}")""".format("exp", self.monster_list[value]["exp"]))
        
        
        try:
            for i in self.monster_list[value]["skills"]:
                self.main_group_list_box_creature_skill_data.insert(tk.END, list(i.keys())[0])
        except:
            self.main_group_list_box_creature_skill_data.delete(0,tk.END)

        

# Start the application
def main():
    Application()

if __name__ == '__main__':
    main()


