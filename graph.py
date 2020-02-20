#import UI_test 

class pair:
    def __init__(self, f = -1, s = -1):
        self.i = f
        self.j = s

    def eqal(self, id):
        if self.i == id.i and self.j == id.j:
            return True
        return False

    def isNull(self):
        if self.i == 0 and self.j == 0:
            return True
        return False

    def printPair(self):
        print("{0}:{1}".format(self.i, self.j))
        
class item:
    def __init__(self, id=None):
        self.child = []
        self.id = id
        self.parent = None
        self.visited = False
        self.fired = False

    def add(self, children):
        self.child += children

    def printItem(self):
        self.id.printPair()

class graph:
    def __init__(self, h):
        self.head = h

def createGraph():
    head = item(0)
    a2 = item(2)
    a3 = item(3)
    a4 = item(4)
    a5 = item(5)
    a6 = item(6)
    a7 = item(7)
    a8 = item(8)
    a9 = item(9)

    head.add([a2, a3])
    a2.add([head, a5])
    a3.add([head, a4, a5])
    a4.add([a3, a6])
    a5.add([a2, a3, a6])
    a6.add([a4, a5, a9])
    a7.add([a8])
    a8.add([a5, a7, a9])
    a9.add([a6, a8])

    return graph(head)

def printWay(it):
    curr = it
    while curr != None:
        #print("{0} -> ".format(curr.id), end="")
        curr.printItem()
        curr = curr.parent
    print()

def createWay(it):
    list=[]
    curr = it
    while curr != None:
        #print("{0} -> ".format(curr.id), end="")
        #curr.printItem()
        list.append(curr.id)
        curr = curr.parent

    return list

def BFS(root, findID = None):
    queue = [root]
    while len(queue) > 0:
        current = queue.pop(0)
        #print('id={0}'.format(current.id))
        #current.printItem()
        for child in current.child:
            if child.visited != True and child.fired != True:
                queue.append(child)
                child.parent = current
                child.fired = True
            if findID!= None and child.id.eqal(findID):
                print("found!")
                #printWay(child)
                return createWay(child)
                
        current.visited = True

def CreateEmptyItemMatrix(m, n):
    matr = [[None] * n for i in range(m)]
    #print("{0}:{1}".format(len(maze), len(maze[0])))
    for i in range(len(matr)):#range(m):
        for j in range(len(matr[i])):#range(n):
            matr[i][j] = item(pair(i,j))

    return matr

def matrixToGraph(matrix, m, n, fromPoint = pair(0,0)):
    #head = item(pair(0,0))
    im = CreateEmptyItemMatrix(m,n)
    #res = graph(im[0][0])
    res = graph(im[fromPoint.i][fromPoint.j])
    for i in range(m):
        for j in range(n):
            #curr = item(pair(0,0))
            if matrix[i][j].walls == 1:
                #print("add [{0}][{1}] to [{2}][{3}]".format(i, j+1, i, j))
                im[i][j].add([im[i][j+1]])
                im[i][j+1].add([im[i][j]])
            elif matrix[i][j].walls == 2:
                #print("add [{0}][{1}] to [{2}][{3}]".format(i+1, j, i, j))
                im[i][j].add([im[i+1][j]])
                im[i+1][j].add([im[i][j]])
            elif matrix[i][j].walls == 3:
                #print("add [{0}][{1}] to [{2}][{3}]".format(i+1, j, i, j))
                im[i][j].add([im[i+1][j]])
                im[i+1][j].add([im[i][j]])
                #print("add [{0}][{1}] to [{2}][{3}]".format(i, j+1, i, j))
                im[i][j].add([im[i][j+1]])
                im[i][j+1].add([im[i][j]])

    return res
               
            
#m = 10
#n = 10

#maze = UI_test.GenerateSidewinderMaze(m, n)
#UI_test.PrintMaze(maze, m ,n)
#graf = matrixToGraph(maze, m, n)

#graph = createGraph()
#BFS(graf.head, pair(8,9))

        



