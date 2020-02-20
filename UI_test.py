import graph
import random
import maze_algorithms as mazeLib
from graph import pair
import tkinter as tk
import time
import copy
import maze_options as defaults

class Logic:
    def __init__(self):
        self.width = defaults.mazeWidth
        self.height = defaults.mazeHeight
        self.widthStr = tk.StringVar(value=str(self.width))
        self.heightStr = tk.StringVar(value=str(self.height))
        self.showGenerationProcess = tk.IntVar()
        self.showWay = tk.IntVar()
        self.maze = None
        self.wayGraph = None
        self.way = []        
        self.methodList = ["SideWinder", "Eller's Algorithm"]
        self.method = tk.StringVar(value = self.methodList[0])        
        self.startPoint = pair(0, 0)
        self.endPoint = pair(self.width - 1, self.height - 1)
        self.pointString = tk.StringVar(value = ("from {0}:{1} to {2}:{3}".format(0, 0, self.width - 1, self.height - 1)))

    def reset(self):
        self.maze = None
        self.wayGraph = None
        self.way = []
        self.startPoint = pair(0, 0)
        self.endPoint = pair(self.width - 1, self.height - 1) #bad, in case if width anf height doesn't contain actual value this pair will contain incorrect data
        self.pointString.set("from {0}:{1} to {2}:{3}".format(0, 0, self.width - 1, self.height - 1))

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master        
        self.canvas = None       
        self.mazeSettings = Logic()
        self.create_widgets()
        #self.after_id = 0

    def create_widgets(self):
        ####################  Frames creating ###############################        
        self.leftFrame = tk.Frame(self)
        self.rightFrame = tk.Frame(self)

        self.generationFrame = tk.LabelFrame(self.leftFrame, bd = 2, relief = tk.GROOVE, text = "Generation")
        self.sizeFrame = tk.Frame(self.generationFrame)
        self.sizelblFrame = tk.LabelFrame(self.sizeFrame, bd = 2, relief = tk.GROOVE, text = "Size")
        self.lbl2Frame = tk.Frame(self.generationFrame)
        self.optionList1Frame = tk.Frame(self.generationFrame)
        self.chkBox1Frame = tk.Frame(self.generationFrame)
        self.btn1Frame = tk.Frame(self.generationFrame)

        self.wayFrame = tk.LabelFrame(self.leftFrame, bd = 2, relief = tk.GROOVE, text = "Find way")
        self.pointFrame = tk.Frame(self.wayFrame)
        self.poinlblFrame = tk.LabelFrame(self.pointFrame, bd = 2, relief = tk.GROOVE, text = "Points")
        self.chkBox2Frame = tk.Frame(self.wayFrame)
        self.btn2Frame = tk.Frame(self.wayFrame)
        self.btn3Frame = tk.Frame(self.wayFrame)

        self.canvasFrame = tk.Frame(self.rightFrame, bd = 2, relief = tk.RIDGE)

        ####################  Frames packing ###############################
        self.leftFrame.pack(side = "left", padx = 10, fill = tk.BOTH)
        self.rightFrame.pack(side = "right", padx = 10, fill = tk.BOTH, expand = 1)

        self.generationFrame.pack(side = "top", fill = tk.X)
        self.sizeFrame.pack(side = "top", fill = tk.X)
        self.sizelblFrame.pack(side = "left", padx = 10)
        self.lbl2Frame.pack(side = "top", fill = tk.X)
        self.optionList1Frame.pack(side = "top", fill = tk.X)
        self.chkBox1Frame.pack(side = "top", fill = tk.X)
        self.btn1Frame.pack(side = "top", fill = tk.X)

        self.wayFrame.pack(side = "top", fill = tk.X)
        self.pointFrame.pack(side = "top", fill = tk.X)
        self.poinlblFrame.pack(side = "left", padx = 10)
        self.chkBox2Frame.pack(side = "top", fill = tk.X)
        self.btn2Frame.pack(side = "top", fill = tk.X)
        self.btn3Frame.pack(side = "top", fill = tk.X)

        self.canvasFrame.pack(side = "top", pady = 8)

        ####################  UI elements creating #########################        
        self.sizeLabel = tk.Label(self.sizelblFrame, text = " x ")
        self.wEntry = tk.Entry(self.sizelblFrame, textvariable = self.mazeSettings.widthStr, width = 3)        
        self.hEntry = tk.Entry(self.sizelblFrame, textvariable = self.mazeSettings.heightStr, width = 3)
        self.algLabel = tk.Label(self.lbl2Frame, text = "Choose algorithm:")
        self.chooseMethod = tk.OptionMenu(self.optionList1Frame, self.mazeSettings.method, *self.mazeSettings.methodList)
        self.showGenProcChkb = tk.Checkbutton(self.chkBox1Frame, text="Show generation process", variable = self.mazeSettings.showGenerationProcess, onvalue=1, offvalue=0)
        self.generateBtn = tk.Button(self.btn1Frame, text = "Generate Maze", command = self.generateMaze)

        self.pointsLbl = tk.Label(self.poinlblFrame, bd = 2, relief = tk.GROOVE, textvariable = self.mazeSettings.pointString)
        self.chooseStartPointBtn = tk.Button(self.poinlblFrame, text = "Start", command = self.chooseStartPoint)
        self.chooseEndPointBtn = tk.Button(self.poinlblFrame, text = "End ", command = self.chooseEndPoint)
        self.showWayProcChkb = tk.Checkbutton(self.chkBox2Frame, text="Show find way process", variable=self.mazeSettings.showWay, onvalue=1, offvalue=0)
        self.findWayBtn = tk.Button(self.btn2Frame, text = "Find Way", command = self.findWay)
        self.clearWayBtn = tk.Button(self.btn3Frame, text = "Clear Way", command = self.clearWay)

        self.canvas = tk.Canvas(self.canvasFrame, width = (self.mazeSettings.height+1)*15, height=(self.mazeSettings.width+1)*15)

        self.quit = tk.Button(self.leftFrame, text="QUIT", fg="red", command=self.master.destroy)

        ####################  UI elements packing ##########################        
        self.wEntry.pack(side = "left", pady = 10, padx = 10)        
        self.sizeLabel.pack(side = "left", pady = 10)        
        self.hEntry.pack(side = "left", pady = 10, padx = 10)        
        self.algLabel.pack(side = "left", padx = 10)        
        self.chooseMethod.pack(side = "left", padx = 10)        
        self.showGenProcChkb.pack(side = "left", pady = 10, padx = 10)        
        self.generateBtn.pack(side="right", pady = 10, padx = 10)
        
        self.pointsLbl.pack(side="bottom", pady = 10)        
        self.chooseStartPointBtn.pack(side="left", pady = 10, padx = 10)        
        self.chooseEndPointBtn.pack(side="left", pady = 10, padx = 10)        
        self.showWayProcChkb.pack(side = "left", pady = 10, fill = tk.X, padx = 10)        
        self.findWayBtn.pack(side="right", padx = 10)        
        self.clearWayBtn.pack(side="right", pady = 10, padx = 10)
        
        self.canvas.pack(side = "top", padx = 10, pady = 10)
        
        self.quit.pack(side="top", pady = 10)

        self.pack()

    def drawWayPoint(self, i, j):
        #self.canvas.create_oval(15+j*15, (i+1)*15, 30+j*15, 15+(i+1)*15)
        #self.canvas.create_rectangle(15+j*15, (i+1)*15, 30+j*15, 15+(i+1)*15, fill='red', outline='red')
        self.canvas.create_oval(15+j*15 + 2, (i+1)*15 + 2, 30+j*15 -2, 15+(i+1)*15 - 2, fill='red', outline='red', tag = "way")

    def clearWay(self):
        self.canvas.delete("way")

    def drawWay(self, points, showProcess = 0):
        points.reverse()
        for i in range(len(points)):
            if showProcess:
                x = points[i].i
                y = points[i].j
                #print("{0}:{1}".format(x, y))
                self.after((i+1)*100, self.drawWayPoint, x, y)
            else:
                self.drawWayPoint(points[i].i, points[i].j)

    def coordinatesToIndexes(self, x, y):
        cX = x // 15 
        cY = y // 15
        if cX == 0 or cY == 0:
            print("incorrect area; using default point")
            return pair(0,0)
        return pair(cY-1, cX-1) #why???
        
    def callbackStart(self, event):
        print("clicked at {0}:{1}".format(event.x, event.y))
        self.mazeSettings.startPoint = self.coordinatesToIndexes(event.x, event.y)
        self.mazeSettings.pointString.set("from {0}:{1} to {2}:{3}".format(self.mazeSettings.startPoint.i, self.mazeSettings.startPoint.j, self.mazeSettings.endPoint.i, self.mazeSettings.endPoint.j))

    def callbackEnd(self, event):
        print("clicked at {0}:{1}".format(event.x, event.y))
        self.mazeSettings.endPoint = self.coordinatesToIndexes(event.x, event.y)
        self.mazeSettings.pointString.set("from {0}:{1} to {2}:{3}".format(self.mazeSettings.startPoint.i, self.mazeSettings.startPoint.j, self.mazeSettings.endPoint.i, self.mazeSettings.endPoint.j))

    def chooseStartPoint(self):
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.callbackStart)

    def chooseEndPoint(self):
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.callbackEnd)        
    
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
                    
    def redrawMaze(self, m, n, matrix, showProcess=0):
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

    def findWay(self):
        self.findWayInMaze(self.mazeSettings.maze, self.mazeSettings.width, self.mazeSettings.height)
        self.drawWay(self.mazeSettings.way, self.mazeSettings.showWay.get())

    def findWayInMaze(self, maze, m, n):
        if self.mazeSettings.maze == None:
            return
        if self.mazeSettings.endPoint.isNull():
            self.mazeSettings.endPoint = pair(self.mazeSettings.width - 1, self.mazeSettings.height - 1)
        self.mazeSettings.wayGraph = graph.matrixToGraph(maze, m, n, self.mazeSettings.startPoint)
        self.mazeSettings.way = graph.BFS(self.mazeSettings.wayGraph.head, self.mazeSettings.endPoint)#pair(m-2,n-1))        

    def getMazeSize(self):
        try:
            wEntry = int(self.mazeSettings.widthStr.get()) # or ?? wEntry = int(self.wEntry.get())
            if wEntry < 0 or wEntry > 100:
                raise Exception("incorrect width value; using default value")
        except:
            wEntry = defaults.mazeWidth #default value here

        try:
            hEntry = int(self.mazeSettings.heightStr.get()) #or ?? hEntry = int(self.hEntry.get())
            if hEntry < 0 or hEntry > 100:
                raise Exception("incorrect height value; using default value")
        except:
            hEntry = defaults.mazeHeight #default value here
            
        self.mazeSettings.width = wEntry
        self.mazeSettings.height = hEntry

        print("{0}:{1}".format(self.mazeSettings.width, self.mazeSettings.height))

    def getDataFromUI(self):
        self.getMazeSize()
        print("genProc = {0}; useAlg = {1}; wayProc = {2}".format(self.mazeSettings.showGenerationProcess.get(), self.mazeSettings.method.get(), self.mazeSettings.showWay.get()))
        ##TODO: width and height vice versa?? Fix it
        self.canvas.config(width = (self.mazeSettings.height+1)*15, height = (self.mazeSettings.width+1)*15)
        self.mazeSettings.pointString.set("from {0}:{1} to {2}:{3}".format(0, 0, self.mazeSettings.width - 1, self.mazeSettings.height - 1))
                
    def generateMaze(self):        
        self.getDataFromUI()
        self.mazeSettings.reset()
        if self.mazeSettings.method.get() == "SideWinder":
            self.mazeSettings.maze = mazeLib.GenerateSidewinderMaze(self.mazeSettings.width, self.mazeSettings.height)
        elif self.mazeSettings.method.get() == "Eller's Algorithm":
            self.mazeSettings.maze = mazeLib.GenerateEllerMaze(self.mazeSettings.width, self.mazeSettings.height)
        else:
            print("Algorithm {0} is not supported!".format(self.mazeSettings.method.get()))
            return
        
        self.redrawMaze(self.mazeSettings.width, self.mazeSettings.height, self.mazeSettings.maze, self.mazeSettings.showGenerationProcess.get())
    

root = tk.Tk()
app = Application(master=root)
app.mainloop()

