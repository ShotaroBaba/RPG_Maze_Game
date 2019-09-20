from random import shuffle
from random import randint

height_default = 5
width_default = 5


# This game will become Role Playing Game where a person 
# walks around the maze and fights with foes. Backtracing algorithm is used
# for generating maze.

# Initialize and create the grid
# The form of the grid is as follows:

# Set direction.
direction = {"N": (0,-1), "S":(0,1),"E":(1,0), "W":(-1,0)}
opposite_direction  = {"N":"S", "S":"N", "E":"W", "W":"E"}
# Firstly, make grid using list.
# height and width must be positive integer.


def make_maze_grid(width = height_default, height = width_default):

    grid = [[[] for _ in range(width)] for _ in range(height)]

    # Take grid as the numbers.
    def generate_maze_grid(current_x=0,current_y=0):
        
        move_directions = ["N","S","E","W"]

        shuffle(move_directions)

        for move_direction in move_directions:
            
            next_x = current_x + direction[move_direction][0]
            next_y = current_y + direction[move_direction][1]

            if 0 <= next_x < len(grid[0]) and 0 <= next_y < len(grid) and grid[next_y][next_x] == []:
                grid[current_y][current_x].append(opposite_direction[move_direction])
                grid[next_y][next_x].append(move_direction)
                generate_maze_grid(next_x, next_y)

    generate_maze_grid(randint(0, width-1), randint(0, height-1))

    return grid

# Create maze first.
def generate_maze_grid(grid):
    # Print maze based on the information on grid.
    # String used for generating maze.

    range_x = range(2 * len(grid[0]) + 1)
    range_y = range(2 * len(grid) + 1)
    max_x = len(list(range_x)) - 1
    max_y = len(list(range_y)) - 1

    maze_list = []
    tmp = []
    for y in range_y:
        tmp = []
        for x in range_x:
            if x % 2 == 1 and y % 2 == 1: 
                tmp.append(" ")
            elif x % 2 == 0 and y % 2 == 1:
                if (x == 0 or x == max_x):
                    tmp.append("#")
                else:
                    # if W --> E
                    if "W" in grid[y//2][x//2-1] and "E" in grid[y//2][x//2]:
                        tmp.append(" ")
                    # if not, the wall is retained.
                    else:
                        tmp.append("#")
            elif y % 2 == 0 and x % 2 == 1:
                if(y == 0 or y == max_y):
                    tmp.append("#")
                else:
                    # if N --> S, then the wall is removed.
                    if "N" in grid[y//2 -1][x//2] and "S" in grid[y//2][x//2]:
                        tmp.append(" ")
                    # if not, the wall is retained.
                    else:
                        tmp.append("#")
            else:
                tmp.append("#")

        maze_list.append(tmp)
    
    return maze_list

# Main function for the test purpose...
def main():

    print("Test maze generation (1)")
    grid = make_maze_grid(10,10)
    maze_str = generate_maze_grid(grid)
    print(maze_str)
    print("\n\n")

    print("Test maze generation (2)")
    grid = make_maze_grid(10,40)
    maze_str = generate_maze_grid(grid)
    print(maze_str)
    print("\n\n")

    print("Test maze generation (3)")
    grid = make_maze_grid(40,10)
    maze_str = generate_maze_grid(grid)
    print(maze_str)
    print("\n\n")

    print("Test maze generation (4)")
    grid = make_maze_grid(30,30)
    maze_str = generate_maze_grid(grid)
    print(maze_str)

if __name__ == '__main__':
    main()

