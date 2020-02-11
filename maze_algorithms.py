import random
class Cell:
    #walls: 0 - right and bottom, 1 - bottom, 2 - right, 3 - none
    def __init__(self, Walls = 0, ID = 0):
        if Walls > 3 or Walls < 0:
            print("Invalid wall type!")
            self.walls = 0
        else:
            self.walls = Walls
        self.id = ID



def PrintMaze(maze, m, n):
    print("  ", end ="")
    for j in range(0, n):
        print("_ ", end ="")
    print()
    for i in range(m):
        print(" |", end ="")
        for j in range(n):
            if maze[i][j].walls == 3:
                print("  ", end ="")
            elif maze[i][j].walls == 2:
                print(" |", end ="")
            elif maze[i][j].walls == 1:
                print("_ ", end ="")
            elif maze[i][j].walls == 0:
                print("_|", end ="")
        print("")


def PrintIDMaze(maze, m, n):
    for i in range(m):
        for j in range(n):
            #print("{0}:{1} = {2} ".format(i, j, maze[i][j].id), end =" ")
            print("{0}".format(maze[i][j].id), end ="\t")
        print()
    print()

def PrintWallMaze(maze, m, n):
    for i in range(m):
        for j in range(n):
            #print("{0}:{1} = {2} ".format(i, j, maze[i][j].id), end =" ")
            print("{0} ".format(maze[i][j].walls), end =" ")
        print()
    print()
        
def CreateEmptyMaze(m, n):
    maze = [[None] * n for i in range(m)]
    print("{0}:{1}".format(len(maze), len(maze[0])))
    for i in range(len(maze)):#range(m):
        for j in range(len(maze[i])):#range(n):
            maze[i][j] = Cell()

    return maze

def InitFirstLine(maze, m, n):
    for i in range(n):
        maze[0][i].id = i+1
    return i+1

def JoinCells():
    res = random.choice([True, False])
    #print(res)
    return res
    #res = random.randint(0, 25000000)
    #if res % 3 != 0:
    #    return False
    #return True


def GetCellCount(maze, row, n, id):
    count = fcount = 0
    for j in range(n):
        if maze[row][j].id == id:
            count += 1
            if maze[row][j].walls == 2 or maze[row][j].walls == 3:
                fcount += 1
    #print("for id {0} {1}:{2}".format(id, count, fcount))
    return count, fcount

def RemoveFloor(maze, row, col):
    if maze[row][col].walls == 0:
        maze[row][col].walls = 2
        maze[row+1][col].id = maze[row][col].id
    if maze[row][col].walls == 1:
        maze[row][col].walls = 3
        maze[row+1][col].id = maze[row][col].id

def RemoveRandomFloor(maze, row, id):
    idIndx = []
    for j in range(n):
        if maze[row][j].id == id:
            idIndx.append(j)

    toRemove = random.choice(idIndx)
    RemoveFloor(maze, row, toRemove)

def GenerateEllerMaze(m,n):
    matrix = CreateEmptyMaze(m, n)
    uniqID = InitFirstLine(matrix, m, n)

    for i in range(m - 1):
        for j in range(n - 1):
            if matrix[i][j].id != matrix[i][j+1].id and JoinCells():
                matrix[i][j].walls = 1
                matrix[i][j+1].id = matrix[i][j].id

        for j in range(n):
            #add checking of wall type?
            count, fcount = GetCellCount(matrix, i, n, matrix[i][j].id)
            if count == 1:
                RemoveFloor(matrix, i, j)
            elif fcount != 0 and JoinCells():
                RemoveFloor(matrix, i, j)
            elif fcount == 0:
                RemoveRandomFloor(matrix, i, matrix[i][j].id)

        for j in range(n):
            if matrix[i+1][j].id == 0:
                matrix[i+1][j].id = uniqID
                uniqID += 1

    for j in range(n-1):
        if matrix[m-1][j].id != matrix[m-1][j+1].id:
            matrix[m-1][j].id = matrix[m-1][j+1].id
            matrix[m-1][j].walls = 1

    #PrintMaze(matrix, m ,n)
    #PrintIDMaze(matrix, m, n)
    return matrix
            

def GenerateSidewinderMaze(m, n):
    matrix = CreateEmptyMaze(m, n)
    run = []    
    #current = matrix[0][0]

    for i in range(m-1):
        run.clear()
        current = matrix[i][0]
        for j in range(n-1):
            run.append(current)
            if JoinCells():
                matrix[i][j].walls = 1
                current = matrix[i][j+1]
            else:
                cell = random.choice(run)
                if cell.walls == 0:
                    cell.walls = 2
                if cell.walls == 1:
                    cell.walls = 3
                run.clear()
                current = matrix[i][j+1]
            if j+1 == n-1:
                matrix[i][j+1].walls = 2
                continue
            
        for j in range(n-1):
            matrix[m-1][j].walls = 1
            

    #PrintMaze(matrix, m ,n)
    return matrix

def CopyMaze(m, n, matrix):
    pass
