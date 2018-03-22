from daedalus import Maze
import cv2, os, sys

args=sys.argv[1:]
print args

h=int(args[0])
w=int(args[1])
name=args[2]
maze_type=args[3]

maze=Maze(h,w)


try:
    maze_type_method=getattr(maze, "create_" + maze_type)
except AttributeError:        
    sys.exit("Nema takve funkcije")


maze_type_method()
maze.save_bitmap(name)

img=cv2.imread(name) #ucitavanje slike
img=(255-img) #konvertovanje bele u crnu
img=img[0:img.shape[0]-1, 0:img.shape[1]-1] #odesecanje dela slike koji smeta (generisan od strane pydaedalus)

#
#for i in range(0, img.shape[0]):
#    for j in range(0,img.shape[1]):
#        if all(img[i][j]) == 0:
#            img[i][j]=[255,0,0]

cv2.imwrite(name, img)

os.rename(name, "../input/" + name)
