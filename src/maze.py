from collections import deque
import cv2 as cv
import heapq as hp

class MazeImg:
    def load(self):
        #TODO
        #za sada se ucitavaju samo crno beli, ali kada se budu ubacile boje
        #moracu da radim filter da bih dobio ovakvu sliku
        #samo sto ce ona vratiti 0 ili 1 vrv pa cu to da konvertujem
        #na 0 i 255 ili da svaku obradim pa da imam 0 i 1, vudecu

       
        return cv.imread(self.path, cv.IMREAD_GRAYSCALE)

    def start_finish(self):
        i=0
        start=0
        finish=0
        
        #TODO bolje?
        #TODO moze jedna petlja?
        while self.img[0][i] == 0 and i < self.width:
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
        self.width=self.img.shape[0]
        self.height=self.img.shape[0]
        (self.start, self.finish)=self.start_finish()
        self.start_string="0_{}".format(self.start)
        self.finish_string="{}_{}".format(self.height-1, self.finish)


    def __str__(self):
        return str(self.img)
    
    def show(self):
        cv.imshow("maze",self.img)
        cv.waitKey(0)
    
class Maze:
    def make_adj_list(self, img):
        #img koji saljemo je klasa i ona ima polje img koje je bas slika(matrica)

        mat=img.img

        adj_list={}
        adj_list["%d_%d" % (0,img.start)]=[]
        
        n=img.width
        m=img.height

        i=1
        j=1
        #posto idem na dole i na desno, uvek proveravam samo 
        #svor sa leve strane i cvbor iznad, tj povezujem unazad
        while i < n:
            while j < m:
#TODO ovo radi, ali za svaki beli piksel pravi cvor, hocu da izbegnem to, smisljam efikasniji nacin
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


    def __init__(self, path):
        self.img=MazeImg(path)
        self.adj_list=self.make_adj_list(self.img)
        self.h={}


    #menhetn rastojanje za heuristiku
    def manhattan(self, stop):
        tmp=stop.split("_")
        stop_x=int(tmp[0])
        stop_y=int(tmp[1])
        

        for v in self.adj_list:
            tmp=v.split("_") #tmp[0] je x tmp[1] je y
            v_x=int(tmp[0])
            v_y=int(tmp[1])
            self.h[v]=abs(stop_x-v_x) + abs(stop_y-v_y)

    def astar(self, start, stop):
        #TODO ostaje da se preko heap-a implementira otvorena lista

        open_list={}
        
        closed_list={}
        
        dist=dict([(v, float('inf')) for v in self.adj_list])
        dist[start]=0
        
        self.manhattan(stop) #heuristika je konzistentna pa dole necemo proveravati zatvorenu listu
        open_list[start]=dist[start]+self.h[start]
        
        parents=dict([(v,None) for v in self.adj_list])

        marked=[]
        marked.append(start)


        while open_list:
            (tmp,val)=min(open_list.items(), key=lambda x: x[1])#uzimamo minimalni element iz otvorene liste
            closed_list[tmp]=val #dodajemo cvor u zatvorenu listu(zavrsili smo sa njim)
            del open_list[tmp] #izbacujemo ga iz otvorene liste TODO proveri ovo mozda mora posle
            if tmp == stop:
                path=deque([])
                while parents[tmp]:
                    path.appendleft(tmp)
                    tmp=parents[tmp]
                path.appendleft(start)
                return list(path)

            for v,w in self.adj_list[tmp]:
                if v not in marked:
                    marked.append(v)
                    dist[v]=dist[tmp]+w
                    open_list[v]=dist[v]+self.h[v]
                    parents[v]=tmp
                elif v in open_list:#cvor je posecen vec i u otvorenoj je listi, gledamo da li moze bolje preko ovog cvora
                    if dist[v] > dist[tmp]+w:#imamo bolji put
                        dist[v]=dist[tmp]+w
                        parents[v]=tmp
                        open_list[v]=dist[v]#azuriramo vrednost u otvorenoj listi
        #izasli smo iz while petlje i nismo izasli, znacio nema puta
        print("Path not found")
        return []
