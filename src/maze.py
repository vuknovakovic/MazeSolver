import cv2 as cv

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
#ovo radi, ali za svaki beli piksel pravi cvor, hocu da izbegnem to
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
        for (k,v) in self.adj_list.items():
            print(str(k) + ":" + str(v))


    
