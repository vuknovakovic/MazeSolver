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



#os.system("python2 ./maze_generator.py 2000 2000 " + name + " perfect")
#print("Generated image: " + name)

pic_path="../input/" + name 



print("Generating graph")
maze=Maze(pic_path)
print("Graph generated\nNumber of nodes: %d" % len(maze.adj_list))

try:
    solve_method=getattr(maze, solver)
except AttributeError:
    sys.exit("Method not found")


pic_res=maze.img.img
pic_res = cv.cvtColor(pic_res, cv.COLOR_GRAY2BGR)

print("Starting solver: " + solver)
start_time=time.time()

solution=solve_method(maze.img.start_string, maze.img.finish_string)

length=len(solution)
color=0

print("Generetaing result image")

for s in range(0,length-1):
    curr=solution[s].split("_")
    nxt=solution[s+1].split("_")
    
    curr=[int(x) for x in curr]
    nxt=[int(x) for x in nxt]
    
    color_to_apply=[0, 0 , 255-color] #set any color you like

    if curr[0]==nxt[0]:
        for x in range(min(curr[1], nxt[1]), max(curr[1], nxt[1])):
            pic_res[curr[0]][x]=color_to_apply
    elif curr[1]==nxt[1]:
        for y in range(min(curr[0], nxt[0]), max(curr[0], nxt[0])+1):
            pic_res[y][curr[1]]=color_to_apply

    color+=255/length

end_time=time.time()

print("Path length: " + str(length) + "\nRuntime: %g s" % (end_time - start_time))
name_no_ext=name[0:name.find(".")]


res_path=name_no_ext + "_" + solver + "_res.png"
print("Saving image: " + res_path)
cv.imwrite("../output/" + res_path, pic_res)





