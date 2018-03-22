from daedalus import Maze
import cv2, os, sys

args=sys.argv[1:]

h=int(args[0])
w=int(args[1])
name=args[2]
maze_type=args[3]

maze=Maze(h,w)


try:
    maze_type_method=getattr(maze, "create_" + maze_type)
except AttributeError:        
    sys.exit("Method not found")


maze_type_method()
maze.save_bitmap(name)

img=cv2.imread(name) #load image
img=(255-img) #convert white to black and vice-versa
img=img[0:img.shape[0]-1, 0:img.shape[1]-1] #clip unwanted part of image(vreated by daedalus)

#
#for i in range(0, img.shape[0]):
#    for j in range(0,img.shape[1]):
#        if all(img[i][j]) == 0:
#            img[i][j]=[255,0,0]

cv2.imwrite(name, img)

os.rename(name, "../input/" + name)
