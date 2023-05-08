from random import randint
import sys

__author__ = "Hamza Amir"
__email__ = "amrham001@myuct.ac.za"
__date__ = "28 August 2022"



def randomP(numR,length):
    startPos = [0,0,0,0]
    h = numR*5
    mid =  h/2
    with open('positions.txt','w') as f:
        line = str(0) + " " + str(0) + " 0"
        f.write(line +'\n')
        for i in range(1,numR):
            x= randint(-mid,mid-40)
            y= randint(-mid,mid-40)
            line = str(x) + " " + str(y) + " 0"
            f.write(line +'\n')
    f.close()

    with open('config.txt','w') as g:
        g.write(str(h) + '\n')
        g.write(str(h) + '\n')
        g.write(str(numR))
    g.close()


def gridP(endP,step):
    m = endP
    l = step
    with open('positions.txt','w') as f:
        for i in range(-m,m,l):
            for j in range(-m,m,l):
                line = str(i) + " " + str(j) + " 0"
                f.write(line + '\n')

    f.close()
    with open('config.txt','w') as g:
        h=m*2 + 100
        g.write(str(h) + '\n')
        g.write(str(h) + '\n')
        g.write('100')
    g.close()

def main(args) :
    l=40
    numRows = 2
    m=l*numRows
    numRobots= 60
    #gridP(m,l)
    randomP(numRobots,l)
   
if __name__ == "__main__":
    main(sys.argv)
