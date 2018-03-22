from maze import MazeImg
from maze import Maze
import cv2 as cv
import sys, time, os

args=sys.argv[1:]

if len(args) < 2:
    sys.exit("Proslediti argumente: ime_fajla.png i resavac(DFS, BFS, dijkstra, astar)")

name=args[0]
solver=args[1]


if not os.path.isdir("../output"):
    if not os.path.exists("../output"): 
        os.mkdir("../output")
    else:
        print("Ne mogu da napravim direktorijum ../output")



os.system("python2 ./maze_generator.py 300 500 " + name + " spiral")

pic_path="../input/" + name 


start_time=time.time()

maze=Maze(pic_path)

try:
    solve_method=getattr(maze, solver)
except AttributeError:
    print("Nema takve funkcije")
    sys.exit(1)


pic_res=maze.img.img
pic_res = cv.cvtColor(pic_res, cv.COLOR_GRAY2BGR)

solution=solve_method(maze.img.start_string, maze.img.finish_string)
length=len(solution)
color=0
tmp=length

for s in range(0,length-1):
    curr=solution[s].split("_")
    nxt=solution[s+1].split("_")
    
    curr=[int(x) for x in curr]
    nxt=[int(x) for x in nxt]
    
    color_to_apply=[color, (255-color)/2 , 255-color] #postavite koju boju zelite

    if curr[0]==nxt[0]:
        for x in range(min(curr[1], nxt[1]), max(curr[1], nxt[1])):
            pic_res[curr[0]][x]=color_to_apply
            tmp+=1
    elif curr[1]==nxt[1]:
        for y in range(min(curr[0], nxt[0]), max(curr[0], nxt[0])+1):
            pic_res[y][curr[1]]=color_to_apply
            tmp+=1

    color+=255/length

end_time=time.time()

print("{}".format(solver) + "\nDuzina: " + str(tmp) + "\nVreme: %g sekundi" % (end_time - start_time))
name_no_ext=name[0:name.find(".")]


res_path=name_no_ext + "_" + solver + "_res.png"
print("Cuvanje slike: " + res_path)
cv.imwrite("../output/" + res_path, pic_res)





