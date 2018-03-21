from maze import MazeImg
from maze import Maze
import time
import cv2 as cv

name=input("Ime slike u input folderu(sa ekstenzijom): ")


pic_path="../input/" + name 

start_time=time.time()

maze=Maze(pic_path)
solution=maze.astar(maze.img.start_string, maze.img.finish_string)

pic_res=cv.imread(pic_path)
for s in solution:
    tmp=s.split("_")
    x=int(tmp[0])
    y=int(tmp[1])
    pic_res[x][y]=[0,0,255]


name_no_ext=name[0:name.find(".")]
#
#
cv.imwrite("../output/" + name_no_ext + "_res.png", pic_res)

end_time=time.time()

print(end_time-start_time)



