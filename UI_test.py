import graph
import random
import maze_algorithms as mazeLib
from graph import pair
import tkinter as tk
import time
import copy
m = 50
n = 50

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.canvas = tk.Canvas(master)
        self.create_widgets()
        #self.after_id = 0

    def drawWayPoint(self, i, j):
        #self.canvas.create_oval(15+j*15, (i+1)*15, 30+j*15, 15+(i+1)*15)
        #self.canvas.create_rectangle(15+j*15, (i+1)*15, 30+j*15, 15+(i+1)*15, fill='red', outline='red')
        self.canvas.create_oval(15+j*15 + 2, (i+1)*15 + 2, 30+j*15 -2, 15+(i+1)*15 - 2, fill='red', outline='red')

    def drawWay(self, points, showProcess = False):
        for i in range(len(points)):
            if showProcess:
                x = points[i].i
                y = points[i].j
                #print("{0}:{1}".format(x, y))
                self.after((i+1)*100, self.drawWayPoint, x, y)
            else:
                self.drawWayPoint(points[i].i, points[i].j)
    
    def draw_horizontal_line(self, i, j):
        self.canvas.create_line(15+j*15, 15+(i+1)*15, 30+j*15, 15+(i+1)*15, tag="{0}:{1}".format(i,j))

    def draw_vertical_line(self, i, j):
        self.canvas.create_line(15+(j+1)*15, 15+i*15, 15+(j+1)*15, 30+i*15, tag="{0}:{1}".format(i,j))

    def drawMaze(self, m, n, maze):
        for j in range(0, n):
            self.draw_horizontal_line(-1, j)
        for i in range(m):
            self.draw_vertical_line(i, -1)
            for j in range(n):
                if maze[i][j].walls == 3:
                    pass
                elif maze[i][j].walls == 2:
                    self.draw_vertical_line(i, j)
                elif maze[i][j].walls == 1:
                    self.draw_horizontal_line(i, j)
                elif maze[i][j].walls == 0:
                    self.draw_vertical_line(i, j)
                    self.draw_horizontal_line(i, j)
                    
    def redrawMazeProcess(self, m, n, matrix):
        self.drawInitMaze(m, n)
        for i in range(m):
            for j in range (n):
                self.after((i*n+j)*50, self.redrawCell, matrix, m, n, i, j)

    def drawInitMaze(self, m , n):
        for j in range(0, n):
            self.draw_horizontal_line(-1, j)
        for i in range(m):
            self.draw_vertical_line(i, -1)
            for j in range(n):
                self.draw_vertical_line(i, j)
                self.draw_horizontal_line(i, j)

    def redrawCell(self, maze, m, n, i, j):
        #print("Delete {0}:{1} cell and draw {2} instead".format(i, j, maze[i][j]))
        self.canvas.delete("{0}:{1}".format(i,j))
        if maze[i][j].walls == 3:
            pass
        elif maze[i][j].walls == 2:
            self.draw_vertical_line(i, j)
        elif maze[i][j].walls == 1:
            self.draw_horizontal_line(i, j)
        elif maze[i][j].walls == 0:
            self.draw_vertical_line(i, j)
            self.draw_horizontal_line(i, j)
                    
    def create_widgets(self):
        ###########################
        self.canvas.pack(expand=1)
        self.canvas.config(width=1000, height=1000)
        ###########################
        self.generate = tk.Button(self)
        self.generate["text"] = "Generate Maze"
        self.generate["command"] = self.generateMaze
        self.generate.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def redrawMaze(self, m, n, matrix, showProcess=False):
        #PrintWallMaze(matrix, m, n)
        #print("0 ")
        #self.after_cancel(self.after_id)
        self.canvas.delete("all")
        if showProcess:
            self.redrawMazeProcess(m, n, matrix)
        else:
            self.drawMaze(m, n, matrix)    

    def GenerateSidewinderMaze(self, m, n, showProcess = False):
        matrix = mazeLib.CreateEmptyMaze(m, n)
        run = []

        for i in range(m-1):
            run.clear()
            for j in range(n):
                run.append(matrix[i][j])
                if mazeLib.JoinCells() and j != n-1:
                    matrix[i][j].walls = 1
                else:
                    cell = random.choice(run)
                    if cell.walls == 0:
                        cell.walls = 2
                    if cell.walls == 1:
                        cell.walls = 3
                    run.clear()
                #if j+1 == n-1:
                #    matrix[i][j+1].walls = 2
                #    #continue
                if showProcess:
                    self.after((i*n+j)*100, lambda matrix=copy.deepcopy(matrix): self.redrawMaze(m, n, matrix))

        for j in range(n-1):
            matrix[m-1][j].walls = 1
            if showProcess:
                    self.after(((m-1)*n+j)*100, lambda matrix=copy.deepcopy(matrix): self.redrawMaze(m, n, matrix))

        #PrintMaze(matrix, m ,n)
        #self.drawMaze(m, n, matrix)
        return matrix

    def findWay(self, maze, m, n):
        graf = graph.matrixToGraph(maze, m, n)
        way = graph.BFS(graf.head, pair(m-2,n-1))
        self.drawWay(way, True)
        
    def generateMaze(self):
        maze = mazeLib.GenerateSidewinderMaze(m, n)
        #maze = mazeLib.GenerateEllerMaze(m,n)
        #maze = CreateEmptyMaze(m, n)
        #PrintMaze(maze, m ,n)
        self.redrawMaze(m, n, maze, True)
        #self.redrawMazeProcess(m, n, maze)
        #self.findWay(maze, m, n)
        #print("hi there, everyone!")

    

root = tk.Tk()
app = Application(master=root)
app.mainloop()


#matrix = CreateEmptyMaze(m, n)
#GenerateEllerMaze(m,n)
#GenerateSidewinderMaze(m, n)
#GenerateSidewinderMazeInt(m,n)
