from collections import deque
import cv2 as cv
from time import time
import heapq as hp
import sys, json, os

class MazeImg:
    def load(self):

        gray = cv.cvtColor(cv.imread(self.path), cv.COLOR_BGR2GRAY)
        ret,thresh = cv.threshold(gray,100,255,cv.THRESH_BINARY)

        return thresh

    def start_finish(self):
        i=0
        start=0
        finish=0

        while self.img[0][i] == 0:
            i+=1
        start=i

        i=0
        while self.img[self.height-1][i] == 0:
            i+=1

        finish=i

        return (start, finish)

    def __init__(self, path):
        self.path=path

        self.img=self.load()

        self.width=self.img.shape[1]
        self.height=self.img.shape[0]

        (self.start, self.finish)=self.start_finish()

        self.start_string="0_{}".format(self.start)
        self.finish_string="{}_{}".format(self.height-1, self.finish)


    def show(self):
        cv.imshow("maze",self.img)
        cv.waitKey(0)

class Maze:

    def stringit(self,x, y):
        return "{}_{}".format(y,x)

    def old_adj_list(self, img):#Old adj_list, here for testing purposes only
        #img that is sent via arg is class MazeImg, real image is img field of that class

        mat=img.img
        start_x=img.start #start coords
        finish_x=img.finish #finish coords

        adj_list={}
        adj_list[self.stringit(start_x, 0)]=[]

        i=1
        j=1
        n=img.height
        m=img.width

        while i < n:
            while j < m:
                if mat[i][j] == 255:
                    adj_list["%d_%d" % (i,j)]=[]
                    if mat[i-1][j] == 255:
                        adj_list["%d_%d" % (i,j)].append(("%d_%d" % (i-1,j),1))
                        adj_list["%d_%d" % (i-1,j)].append(("%d_%d" % (i,j),1))
                    if mat[i][j-1] == 255:
                        adj_list["%d_%d" % (i,j)].append(("%d_%d" % (i,j-1),1))
                        adj_list["%d_%d" % (i,j-1)].append(("%d_%d" % (i,j),1))

                j+=1
            j=1
            i+=1
        return adj_list

    def calculate_edge_weight(self, u, v):
        u = u.split("_")
        v = v.split("_")

        u=[int(x) for x in u]
        v=[int(x) for x in v]

        return abs(u[0]-v[0]) + abs(u[1] - v[1])

    def make_adj_list(self, img, name_json):
        #img that is sent via arg is class MazeImg, real image is img field of that class

        mat=img.img
        start_x=img.start #start coords
        finish_x=img.finish #finish coords

        adj_list={}
        adj_list[self.stringit(start_x, 0)]=[]

        w=img.width
        h=img.height

        x=1
        y=1
        top_nodes=[None]*w #Used for North-South edges
        top_nodes[start_x]=self.stringit(start_x, 0)

        for y in range(1,h-1):
            prev=False
            curr=False
            nxt=(mat[y][1])>0 #0 means we hit wall, so we check for >0(path)

            left_node=None

            for x in range(1,w-1):
                prev=curr
                curr=nxt
                nxt=(mat[y][x+1])>0

                n=None

                if curr == False:#Hit wall
                    continue

                adj_list[self.stringit(x,y)]=[]

                if prev == True:

                    if nxt == True:
                        #PATH PATH PATH
                        if mat[y-1][x] > 0 or mat[y+1][x] > 0:#if path above or below exists
                            n=self.stringit(x,y)

                            edge_weight=self.calculate_edge_weight(n, left_node)

                            adj_list[n].append((left_node, edge_weight))#this branch won't be executed until we are on path, so this is safe
                            adj_list[left_node].append((n, edge_weight))

                            left_node=n

                    else:
                        #PATH PATH WALL
                        n=self.stringit(x,y)

                        edge_weight=self.calculate_edge_weight(n, left_node)

                        adj_list[left_node].append((n,edge_weight))
                        adj_list[n].append((left_node,edge_weight))

                        left_node=None

                else:

                    if nxt == True:
                        #WALL PATH PATH
                        n=self.stringit(x,y)
                        left_node=n
                    else:
                        #WALL PATH WALL
                        #create node only if there is wall above or bellow us, otherwise no need to create
                        if mat[y+1][x] == 0 or mat[y-1][x] == 0:
                            n=self.stringit(x,y)

                if n != None:#if node is created, check for Notrh-South edges
                    if mat[y-1][x] > 0:#above is clear
                        tmp=top_nodes[x]

                        edge_weight=self.calculate_edge_weight(tmp, n)

                        adj_list[tmp].append((n,edge_weight))
                        adj_list[n].append((tmp, edge_weight))

                        top_nodes[x]=n
                    elif mat[y+1][x] > 0:#path bellow, set this node as top node for next time
                        top_nodes[x]=n
                    else:
                        top_nodes[x]=None

        finish_str=img.finish_string
        tmp=top_nodes[finish_x]

        edge_weight=self.calculate_edge_weight(finish_str, tmp)

        adj_list[tmp].append((finish_str, edge_weight))
        adj_list[finish_str]=[(tmp, edge_weight)]


#        for k,v in adj_list.items():
#            print("{}:{}".format(k, v))

        with open (name_json, "w") as f:
            print("Saving graph to: " + name_json)
            json.dump(adj_list, f)
        return adj_list


    def __init__(self, path):
        self.img=MazeImg(path)
        name_no_ext=path[0:path.rfind(".")]
        name_json=name_no_ext + ".json"
        if name_json[name_json.rfind("/")+1:] not in os.listdir("../input"):
            self.adj_list=self.make_adj_list(self.img, name_json)
        else:
            print("loading from json")
            with open(name_json, "r") as f:
                self.adj_list=json.load(f)
#        self.adj_list=self.old_adj_list(self.img) #uncomment if you want realy slow algorithm


        self.h={}

    #chebyshev heuristic
    def chebyshev(self, stop):
        start_time = time()
        tmp=stop.split("_")
        stop_x=int(tmp[0])
        stop_y=int(tmp[1])


        for v in self.adj_list:
            tmp=v.split("_")
            v_x=int(tmp[0])
            v_y=int(tmp[1])
            self.h[v]=max(abs(stop_x-v_x), abs(stop_y-v_y))

        end_time=time()
        print("Chebyshev: {}s".format(end_time - start_time))

    #manhattan heuristic
    def manhattan(self, stop):
        start_time = time()
        tmp=stop.split("_")
        stop_x=int(tmp[0])
        stop_y=int(tmp[1])


        for v in self.adj_list:
            tmp=v.split("_")
            v_x=int(tmp[0])
            v_y=int(tmp[1])
            self.h[v]=abs(stop_x-v_x) + abs(stop_y-v_y)

        end_time=time()
        print("Manhattan: {}s".format(end_time - start_time))

#euclid heuristic
    def euclid(self, stop):
        start_time=time()
        tmp=stop.split("_")

        stop_x=int(tmp[0])
        stop_y=int(tmp[1])

        for v in self.adj_list:
            tmp=v.split("_")
            v_x=int(tmp[0])
            v_y=int(tmp[1])
            self.h[v]=int(((stop_x-v_x)**2 + (stop_y-v_y)**2)**(0.3))

        end_time=time()
        print("Euclid: {}s".format(end_time - start_time))

    def astar(self, start, stop):
        #TODO implement open_list using heap

        open_list={}
        #closed_list={}

        dist=dict([(v, float('inf')) for v in self.adj_list])
        dist[start]=0

        self.manhattan(stop)
#        self.euclid(stop)
#        self.chebyshev(stop)
        open_list[start]=dist[start]+self.h[start]

        parents=dict([(v,None) for v in self.adj_list])

        marked={}
        marked[start]=True
        while open_list:
            (tmp,val)=min(open_list.items(), key=lambda x: x[1])#take current minimum in open_list, add it to closed list and remove it from open_list

            #closed_list[tmp]=val
            del open_list[tmp]

            #if we found exit
            if tmp == stop:
                path=deque([])

                while parents[tmp]:
                    path.appendleft(tmp)
                    tmp=parents[tmp]

                path.appendleft(start)
                return list(path)

            for v,w in self.adj_list[tmp]:
                if v not in marked:
                    marked[v]=True

                    dist[v]=dist[tmp]+w
                    open_list[v]=dist[v]+self.h[v]

                    parents[v]=tmp

                elif v in open_list:
                    if dist[v] > dist[tmp]+w:#better path exists
                        dist[v]=dist[tmp]+w
                        parents[v]=tmp
                        open_list[v]=dist[v]#update value in open_list


        #while loop ended, that means no path
        print("Path not found")
        return []

    def DFS(self, start, stop):

        marked={}
        marked[start] = True
        path = [start]

        while len(path) > 0:

            v = path[-1]

            if v == stop:
                return path

            has_unvisited = False

            for (w, weight) in self.adj_list[v]:
                if w not in marked:
                    path.append(w)
                    marked[w] = True
                    has_unvisited = True
                    break

            if has_unvisited == False:
                path.pop()

    def BFS(self, start, stop):#NOTE coloring won't work here and in DFS every time
        marked={}
        marked[start]=True
        path=deque()
        path.append(start)
        res=[]
        while len(path)>0:
            v=path.popleft()
            res.append(v)

            if v == stop:
                return res

            for (w, _) in self.adj_list[v]:
                if w not in marked:
                    marked[w]=True
                    path.append(w)

    def dijkstra(self, start, stop):
        marked={}
        open_list={}
        parents=dict([(v,None) for v in self.adj_list])

        marked[start]=True

        dist=dict([(v, float('inf')) for v in self.adj_list])
        dist[start]=0


        open_list[start]=dist[start]
        while open_list:
            (tmp,val)=min(open_list.items(), key=lambda x: x[1])
            del open_list[tmp]
            if tmp == stop:
                path=deque([])
                while parents[tmp]:
                    path.appendleft(tmp)
                    tmp=parents[tmp]
                path.appendleft(start)
                return list(path)

            for v,w in self.adj_list[tmp]:
                if v not in marked:
                    marked[v]=True
                    dist[v]=dist[tmp]+w
                    open_list[v]=dist[v]
                    parents[v]=tmp
                elif v in open_list:
                    if dist[v] > dist[tmp]+w:
                        dist[v]=dist[tmp]+w
                        parents[v]=tmp
                        open_list[v]=dist[v]
