from maze import MazeImg
from maze import Maze
import cv2 as cv
import sys, time, os

args=sys.argv[1:]

if len(args) < 2:
    sys.exit("Call with args: image_name.png astar|dijkstra|BFS|DFS")

name=args[0]
solver=args[1]


if not os.path.isdir("../output"):
    if not os.path.exists("../output"): 
        os.mkdir("../output")
    else:
        sys.exit("Unable to create directory: ../output")


choice=""

def generate_image(name):
    w=input("Enter width: ")
    h=input("Enter height: ")
    maze_type = input("Type of maze(braid|perfect|spiral|unicursal|diagonal|braid_eller): ")
    os.system("python2 ./maze_generator.py " + str(w) + " " + str(h) + " " + name + " " + maze_type)
    print("\nGenerated image: " + name + "\n")

if name in os.listdir("../input"):
    print("Image with that name exists\nErase it and generate again?(y/N)",)
    choice=input()

    if choice.lower() == 'y':
        os.system("rm ../input/" + name)
        os.system("rm ../input/" + name[0:name.find(".")] + ".json")
        generate_image(name)
else:
    generate_image(name)

pic_path="../input/" + name 

print("\nGenerating graph")
maze=Maze(pic_path)
print("Graph generated\nNumber of nodes: %d\n\n" % len(maze.adj_list))

try:
    solve_method=getattr(maze, solver)
except AttributeError:
    sys.exit("Method not found")


pic_res=maze.img.img
pic_res = cv.cvtColor(pic_res, cv.COLOR_GRAY2BGR)

print("Starting solver: " + solver)
start_time=time.time()

solution=solve_method(maze.img.start_string, maze.img.finish_string)

end_time=time.time()
length=len(solution)

print("Path length: " + str(length) + "\nRuntime: %g s" % (end_time - start_time))

color=0

print("Generetaing result image\n")

for s in range(0,length-1):
    curr=solution[s].split("_")
    nxt=solution[s+1].split("_")
    
    curr=[int(x) for x in curr]
    nxt=[int(x) for x in nxt]
    
    color_to_apply=[100*(1-color) + 30*color, 200*(1-color) + 20*color, 255*(1-color) + 40*color] #set any color you like

    if curr[0]==nxt[0]:
        for x in range(min(curr[1], nxt[1]), max(curr[1], nxt[1])):
            pic_res[curr[0]][x]=color_to_apply
    elif curr[1]==nxt[1]:
        for y in range(min(curr[0], nxt[0]), max(curr[0], nxt[0])+1):
            pic_res[y][curr[1]]=color_to_apply

    color+=1/length


name_no_ext=name[0:name.find(".")]

res_path=name_no_ext + "_" + solver + "_res.png"
print("Saving image: " + res_path)
cv.imwrite("../output/" + res_path, pic_res)





