from kivy.uix.gesturesurface import Line
from kivy.uix.behaviors.touchripple import Color
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.effectwidget import Rectangle
from kivy.core.window import Window
from kivy.uix.popup import Popup
import random

gridWidth = 16
gridHeight = 25

objectList = [[[int(gridWidth/2),gridHeight-1],[int(gridWidth/2),gridHeight-2],[int(gridWidth/2),gridHeight-3],[int(gridWidth/2),gridHeight-4]], # straight line
[[int(gridWidth/2),gridHeight-1],[int(gridWidth/2),gridHeight-2],[int(gridWidth/2),gridHeight-3],[int(gridWidth/2)-1,gridHeight-3]], # L left
[[int(gridWidth/2),gridHeight-1],[int(gridWidth/2),gridHeight-2],[int(gridWidth/2)-1,gridHeight-2],[int(gridWidth/2)-1,gridHeight-1]], # square
[[int(gridWidth/2),gridHeight-1],[int(gridWidth/2),gridHeight-2],[int(gridWidth/2)+1,gridHeight-2],[int(gridWidth/2)+1,gridHeight-3]], # rotated z
[[int(gridWidth/2),gridHeight-1],[int(gridWidth/2),gridHeight-2],[int(gridWidth/2)+1,gridHeight-2],[int(gridWidth/2)+1,gridHeight-3]], # rotated s
[[int(gridWidth/2),gridHeight-1],[int(gridWidth/2),gridHeight-2],[int(gridWidth/2)+1,gridHeight-3],[int(gridWidth/2),gridHeight-3]], # L right
[[int(gridWidth/2),gridHeight-1],[int(gridWidth/2),gridHeight-2],[int(gridWidth/2),gridHeight-3],[int(gridWidth/2)-1,gridHeight-2]]] # T

# class of the settings popup
class SettingsPopup(Popup):
    pass

# the class of the main grid
class MainGrid(GridLayout):
    def __init__(self):
        super(MainGrid, self).__init__()
        Window.bind(on_key_down=self.keyAction)
    def keyAction(self, instance, keyboard, keycode, text, modifiers):
        #print(text)
        if text == "a":
            self.moveObject("left")
        elif text == "d":
            self.moveObject("right")
        elif text == "s":
            self.moveObject("down")
        elif text == "w":
            self.moveObject("rotate")
        elif text == "r":
            self.restart()
    def restart(self):
        self.clockEvent.cancel()
        self.ids.scoreLabel.text = "Score: 0"
        self.setup()
    def moveObject(self, direction):
        #print(self.moveTiles)
        tilesToRemove = []
        tilesToAppend = []
        if direction == "left" and self.lastMove != "left":
            for tile in self.moveTiles:
                if tile[1] <= 0 or [tile[0], tile[1]-1] in self.staticTiles:
                    return
            orderedTiles = sorted(self.moveTiles, key=lambda x: x[1])
            for tile in orderedTiles:
                self.gameGrid[tile[0]][tile[1]] = 0
                self.gameGrid[tile[0]][tile[1]-1] = 1
                tilesToRemove.append([tile[0], tile[1]]) # tiles have to be removed outside of this loop since otherwise it will start skipping tiles
                tilesToAppend.append([tile[0], tile[1]-1])
            self.lastMove = "left"
            #print(self.moveTiles, "changed to left")
        elif direction == "right" and self.lastMove != "right":
            for tile in self.moveTiles:
                if tile[1] >= gridWidth-1 or [tile[0], tile[1]+1] in self.staticTiles:
                    return
            orderedTiles = sorted(self.moveTiles, key=lambda x: x[1], reverse=True)
            for tile in orderedTiles:
                self.gameGrid[tile[0]][tile[1]] = 0
                self.gameGrid[tile[0]][tile[1]+1] = 1
                tilesToRemove.append([tile[0], tile[1]])
                tilesToAppend.append([tile[0], tile[1]+1])
            self.lastMove = "right"
        elif direction == "down" and self.lastMove != "down":
            for tile in self.moveTiles:
                if tile[0] <= 0 or [tile[0]-1, tile[1]] in self.staticTiles:
                    return
            orderedTiles = sorted(self.moveTiles, key=lambda x: x[0])
            for tile in orderedTiles:
                self.gameGrid[tile[0]][tile[1]] = 0
                self.gameGrid[tile[0]-1][tile[1]] = 1
                tilesToRemove.append([tile[0], tile[1]])
                tilesToAppend.append([tile[0]-1, tile[1]])
            self.lastMove = "down"
        elif direction == "rotate" and self.lastMove != "rotate":
            # flipping the tiles, this is complicated, but it should work
            print("rotating")
            pieceTiles = self.moveTiles
            mostLeftTile = None
            mostTopTile = None
            MatrixSize = 0
            # finding the most left and top tiles, this will be the top left corner of the matrix used in the rotating
            for tile in pieceTiles:
                if mostLeftTile == None or tile[1] < mostLeftTile[1]:
                    mostLeftTile = tile
                if mostTopTile == None or tile[0] > mostTopTile[0]:
                    mostTopTile = tile
            # finding the size of the matrix, this is the longest distance from side to side of the object/matrix
            print(mostTopTile, mostLeftTile, "most top and left tile")
            for tile in pieceTiles:
                print(tile, "tile")
                if abs(tile[0]-mostTopTile[0]) > MatrixSize - 1:
                    print(tile[0],mostTopTile[0], "tile[0], mostTopTile[0]")
                    MatrixSize = abs(tile[0]-mostTopTile[0]) + 1
                    print(MatrixSize, "MatrixSize changed to by first if")
                if abs(tile[1]-mostLeftTile[1]) > MatrixSize - 1:
                    MatrixSize = abs(tile[1]-mostLeftTile[1]) + 1
                    print(MatrixSize, "MatrixSize changed to by second if")
            print(MatrixSize, "MatrixSize")
            MatrixGrid = []
            for i in range(MatrixSize):
                MatrixGrid.append([])
                for j in range(MatrixSize):
                    if [mostTopTile[0]-i, mostLeftTile[1]+j] in pieceTiles:
                        MatrixGrid[i].append(1)
                    else:
                        MatrixGrid[i].append(0)
            #print(pieceTiles)
            #for i in range(MatrixSize):
            #    print(MatrixGrid[i])
            resGrid = self.rotateMatrixClockwise(MatrixGrid)
            #print("-----------------")
            #for i in range(MatrixSize):
                #print(resGrid[i])
            #print(mostTopTile[0],mostLeftTile[1])
            # now moving the tiles back to the original position, for this I will use the top left corner as a reference point
            for i in self.moveTiles:
                tilesToRemove.append(i)
            for i in range(MatrixSize):
                for j in range(MatrixSize):
                    if resGrid[i][j] == 1:
                        tilesToAppend.append([mostTopTile[0]-i, mostLeftTile[1]+j])
                        self.gameGrid[mostTopTile[0]-i][mostLeftTile[1]+j] = 1
                        #print("tile at ", mostTopTile[0]-i, mostLeftTile[1]+j, "changed to 1")
                    else:
                        self.gameGrid[mostTopTile[0]-i][mostLeftTile[1]+j] = 0
            #print(self.moveTiles, "move tiles")
            self.lastMove = "rotate"
        #print(tilesToRemove, "tiles to remove")
        for tile in tilesToRemove:
            self.moveTiles.remove(tile)
        #print(tilesToAppend, "tiles to append")
        for tile in tilesToAppend:
            self.moveTiles.append(tile)
        #print(self.moveTiles, "move tiles")
    def rotateMatrixClockwise(self, matrix):
        return [list(reversed(col)) for col in zip(*matrix)]
    def setup(self):
        self.gameGrid = []
        self.moveTiles = []
        self.staticTiles = []
        self.score = 0
        self.lastMove = ""
        for i in range(gridHeight):
            self.gameGrid.append([])
            for j in range(gridWidth):
                self.gameGrid[i].append(0)
        self.changeSize()
        # just for testing of the line check thing
        #for i in range(gridWidth):
        #    self.gameGrid[0][i] = 1
        #    self.gameGrid[1][i] = 1
        self.spawnObject()
        self.clockEvent = Clock.schedule_interval(self.update, 1)
    def changeSize(self):
        self.sizeTile = self.size[1] / (gridHeight + gridHeight/5)
    def draw(self):
        self.ids.tetrisCanvas.canvas.clear()
        for i in range(gridHeight - 1):
            # drawing the horizontal grid lines
            self.ids.tetrisCanvas.canvas.add(Color(rgba=(0, 0, 0, 1)))
            self.ids.tetrisCanvas.canvas.add(Line(points=[self.size[0]/2-gridWidth*self.sizeTile/2, i*self.sizeTile+self.sizeTile*3, self.size[0]/2+gridWidth*self.sizeTile/2, i*self.sizeTile+self.sizeTile*3]))
            for j in range(gridWidth):
                # drawing the tiles
                if self.gameGrid[i][j] == 0:
                    self.ids.tetrisCanvas.canvas.add(Color(rgba=(1, 1, 1, 1)))
                    self.ids.tetrisCanvas.canvas.add(Rectangle(pos=(j*self.sizeTile+self.size[0]/2-self.sizeTile*gridWidth/2, i*self.sizeTile+self.sizeTile*3), size = (self.sizeTile, self.sizeTile)))
                else:
                    self.ids.tetrisCanvas.canvas.add(Color(rgba=(1, 0, 0, 1)))
                    self.ids.tetrisCanvas.canvas.add(Rectangle(pos=(j*self.sizeTile+self.size[0]/2-self.sizeTile*gridWidth/2, i*self.sizeTile+self.sizeTile*3), size =(self.sizeTile, self.sizeTile)))
        # drawing the vertical grid lines
        for i in range(gridWidth):
            self.ids.tetrisCanvas.canvas.add(Color(rgba=(0, 0, 0, 1)))
            self.ids.tetrisCanvas.canvas.add(Line(points=[i*self.sizeTile+self.size[0]/2-gridWidth*self.sizeTile/2, self.sizeTile*3, i*self.sizeTile+self.size[0]/2-gridWidth*self.sizeTile/2, self.sizeTile*gridHeight+self.sizeTile*2]))
        # drawing the next tiles rectangle
        self.ids.tetrisCanvas.canvas.add(Color(rgba=(1, 1, 1, 1)))
        self.ids.tetrisCanvas.canvas.add(Rectangle(pos=(self.size[0]/2+gridWidth*self.sizeTile/2+self.sizeTile, self.sizeTile*6), size=(self.size[0]/2-gridWidth*self.sizeTile/2-self.sizeTile*2, self.size[1]-self.sizeTile*17)))
        # reseting the last move, this ensures that the player can only move once during a game tick
        self.lastMove = ""
    def spawnObject(self):
        if len(self.moveTiles) == 0:
            self.choice = random.choice(objectList)
            for tile in self.choice:
                if self.gameGrid[tile[1]][tile[0]] == 1:
                    self.gameOver()
                    break
            for tile in self.choice:
                self.moveTiles.append([tile[1], tile[0]]) # I somehow managed to the tiles in reverse order, however it should still work
                self.gameGrid[tile[1]][tile[0]] = 1
    def gameOver(self):
        self.clockEvent.cancel()
        print("game over")
    def update(self, dt):
        self.move()
        self.draw()
        self.spawnObject()
        self.checkLines()
    def move(self):
        for i in range(gridHeight):
            for j in range(gridWidth):
                if self.gameGrid[i][j] == 1 and [i, j] in self.moveTiles:
                    if i <= 0 or [i-1, j] in self.staticTiles:
                        for tile in self.moveTiles:
                            self.staticTiles.append(tile)
                            #print(self.staticTiles)
                        self.moveTiles = []
        for i in range(gridHeight):
            for j in range(gridWidth):
                if self.gameGrid[i][j] == 1 and [i, j] in self.moveTiles:
                    if [i-1, j] not in self.staticTiles:
                        self.gameGrid[i][j] = 0
                        self.gameGrid[i-1][j] = 1
                        self.moveTiles.remove([i, j])
                        self.moveTiles.append([i-1, j])
    def checkLines(self):
        linesCleared = 0
        for i in range(gridHeight):
            if 0 not in self.gameGrid[i]:
                self.gameGrid.pop(i)
                print("cleared line at", i)
                self.gameGrid.insert(0, [0 for i in range(gridWidth)])
                linesCleared += 1
        self.score += linesCleared * 100 # this may not be the actual way to calculate the score, however I dont think it matters anyway
        self.ids.scoreLabel.text = "Score: " + str(self.score)
    def settings(self):
        popup = SettingsPopup()
        popup.open()

# the app class
class TetrisApp(App):
    def build(self):
        return MainGrid()
    
# running the app
def main():
    TetrisApp().run()