from maze import MazeImg
from maze import Maze
import cv2 as cv
import sys, time, os

name=input("Ime slike u input folderu(sa ekstenzijom): ")

solver=input("Resavac(DFS, BFS, astar, dijkstra): ")

if not os.path.isdir("../output"):
    if not os.path.exists("../output"): 
        os.mkdir("../output")
    else:
        print("Ne mogu da napravim direktorijum ../output")

pic_path="../input/" + name 


start_time=time.time()

maze=Maze(pic_path)

try:
    solve_method=getattr(maze, solver)
except AttributeError:
    print("Nema takve funkcije")
    sys.exit(1)


pic_res=cv.imread(pic_path)

solution=solve_method(maze.img.start_string, maze.img.finish_string)
length=len(solution)
color=0

for s in range(0,length-1):
    curr=solution[s].split("_")
    nxt=solution[s+1].split("_")
    
    curr=[int(x) for x in curr]
    nxt=[int(x) for x in nxt]
    
    color_to_apply=[color, 0, 255-color]

    if curr[0]==nxt[0]:
        for x in range(min(curr[1], nxt[1]), max(curr[1], nxt[1])):
            pic_res[curr[0]][x]=color_to_apply
    elif curr[1]==nxt[1]:
        for y in range(min(curr[0], nxt[0]), max(curr[0], nxt[0])+1):
            pic_res[y][curr[1]]=color_to_apply

    color+=255/length

end_time=time.time()

print("{}".format(solver) + "\nDuzina: " + str(length) + "\nVreme: %g sekundi" % (end_time - start_time))
name_no_ext=name[0:name.find(".")]
#
#
print("Cuvanje slike: " + name_no_ext + "_res.png")
cv.imwrite("../output/" + name_no_ext + "_res.png", pic_res)





