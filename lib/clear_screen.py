# import system 
from os import system, name 

# define clear function 
def clear(): 
    # for windows 
    if name == 'nt': 
        system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        system('clear') 
  