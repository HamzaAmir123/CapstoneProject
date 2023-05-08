from random import randint
import sys

__author__ = "Hamza Amir and Benjamin Chiddy"
__email__ = "amrham001@myuct.ac.za"
__date__ = "28 August 2022"


def randomP(numR, length):
    startPos = [0, 0, 0, 0]
    h = numR*5
    mid = h/2
    with open('positions.txt', 'w') as f:
        line = str(0) + " " + str(0) + " 0"
        f.write(line + '\n')
        for i in range(1, numR):
            x = randint(-mid, mid-40)
            y = randint(-mid, mid-40)
            line = str(x) + " " + str(y) + " 0"
            f.write(line + '\n')
    f.close()

    with open('config.txt', 'w') as g:
        g.write(str(h) + '\n')
        g.write(str(h) + '\n')
        g.write(str(numR))
    g.close()


def gridP(endP, step, amount):
    m = endP
    l = step
    with open(f'positions{amount}.txt', 'w') as f:
        for i in range(-m, m, l):
            for j in range(-m, m, l):
                line = str(i) + " " + str(j) + " 0"
                f.write(line + '\n')

    f.close()
    with open(f'config{amount}.txt', 'w') as g:
        h = m*2 + 100
        g.write(str(h) + '\n')
        g.write(str(h) + '\n')
        g.write(f'{amount}')
    g.close()


def main(args):
    l = 60
    numRobots = 100
    # l * 0.5 * sqrt(n)
    gridP(l*1, l, 4)  # Generate test of 4 robots
    gridP(l*5, l, 100)  # Generate test of 100 robots
    gridP(l*15, l, 900)  # Generate test of 900 robots
    gridP(l*50, l, 10000)  # Generate test of 10000 robots
    gridP(l*150, l, 90000)  # Generate test of 90000 robots
    gridP(l*1000, l, 100000)  # Generate test of 1000000 robots


if __name__ == "__main__":
    main(sys.argv)
