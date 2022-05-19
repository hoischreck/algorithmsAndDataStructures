from Dependencies.PygameClass2.PygameClass2 import *
from random import randint, choice

from collections import namedtuple

NeighbourVertex = namedtuple("NeighbourVertex", "neighbour cost")

class PygameRandomWeightedGraph:
    def __init__(self, vertexAmount, edgeMax=3, edgeMin=1, weightMax=10, weightMin=1):
        self.game = Game()
        self.game.name = "Random Graph"
        self.game.windowSize = (1920, 1080)
        self.game.tickrate = 20
        self.game.init()
        self.__main = self.game.loop(self._main)
        self.edgeColor = (0, 0, 0)

        self.vertexAmount = vertexAmount

        self.adjacencyList = self.createRandomAdjacencyList(vertexAmount, edgeMax, edgeMin, weightMax, weightMin)

        self.vertices = self.__getAllVertices()

    def __getAllVertices(self):
        return set(self.adjacencyList.keys())

    def getNeighbours(self, vertex):
        return self.adjacencyList[vertex]

    def show(self):
        while self.game.running:
            self.__main()

    def _main(self):
        for v in self.adjacencyList:
            x1, y1 = self.adjacencyList[v][0].x_y_position()
            for n in self.adjacencyList[v][1]:
                x2, y2 = self.adjacencyList[n.neighbour][0].x_y_position()
                self.game.draw_line((x1, y1), (x2, y2), self.edgeColor, 4)

    def createRandomAdjacencyList(self, vertexAmount, edgeMax, edgeMin, weightMax, weightMin):
        vertexObjects = self.createVertices(vertexAmount, radius_range=(23, 23))
        adjacencyList = {}
        for c, v in enumerate(vertexObjects):
            adjacencyList[c] = [v, set()]
        verticesWithWeights = {v: randint(weightMin, weightMax) for v in adjacencyList}
        for v in adjacencyList:
            for i in range(randint(edgeMin, edgeMax)+1):
                choices = []
                for j in adjacencyList:
                    if j not in adjacencyList[v][1] and j != v and not self.hasNeighbourTuple(v, adjacencyList[j][1]):
                        choices.append(NeighbourVertex(j, verticesWithWeights[j]))
                if len(choices) > 0:
                    adjacencyList[v][1].add(choice(choices))
        for v in adjacencyList:
            self.game.add.Text2D(adjacencyList[v][0].x_y_position_center(), 25, str(v), bold=True)
        checkedEdges = {v: set() for v in adjacencyList}
        for v in adjacencyList:
            for n in adjacencyList[v][1]:
                if n.neighbour not in checkedEdges[v] and v not in checkedEdges[n.neighbour]:
                    x1, y1 = adjacencyList[v][0].x_y_position()
                    x2, y2 = adjacencyList[n.neighbour][0].x_y_position()
                    #print(x1, x2, y1, y2, v, n.neighbour)
                    if x1 < x2:
                        m = (y1-y2)/(x1-x2)
                        xLabel = int(abs(x1 - x2)/2) + x1
                        yLabel = (xLabel-x1) * m + y1
                    elif x1 > x2:
                        m = (y1-y2)/(x2-x1)
                        xLabel = int(abs(x1 - x2)/2) + x2
                        yLabel = (xLabel-x2) * m + y1
                    else:
                        xLabel = x1
                        yLabel = abs(int(y2-y1))
                    self.game.add.Text2D((xLabel, yLabel), 30, str(n.cost), bold=True, color=(0, 0, 255))
        return adjacencyList

    #Ineffiziente Funktion, durch falsche Datenstruktur <-- Faulheit
    def hasNeighbourTuple(self, v, iterable):
        for i in iterable:
            if v == i.neighbour:
                return True
        return False

    def createVertices(self, amount, radius_range=(10, 25)):
        if amount % 2 != 0:
            raise ValueError("amount must be dividable by 2")
        circles = []
        placement_ratio = self.game.windowSize[0] / self.game.windowSize[1]
        positions = self.CalculatePositionsWithEqualSpreading(amount, placement_ratio)
        for i in range(amount):
            pos = positions[i]
            radius = random.randint(*radius_range)
            color = self.game.collection.random_color()
            circles.append(self.game.add.Circle2D(pos, radius, color))
        return circles

    def CalculatePositionsWithEqualSpreading(self, amount, ratio):
        possible, pos = {}, []
        for f1 in range(1, amount + 1):
            for f2 in range(1, amount + 1):
                if f2 * f1 == amount:
                    possible[(f2, f1)] = f2 / f1
        r = min(possible.items(), key=lambda x: abs(x[1] - ratio))[0]
        fx, fy = int(self.game.windowSize[0] / r[0]), int(self.game.windowSize[1] / r[1])
        for row in range(1, r[1] + 1):
            for column in range(1, r[0] + 1):
                x = fx * column - int(fx / 2) + randint(-200, 200) # Should not be fixed value
                y = fy * row - int(fy / 2) + randint(-200, 200)
                pos.append((x, y))
        return pos

    def drawPath(self, path, color = (255, 0, 0)):
        # Soll einen ausgewählten Path dauerhaft im loop nachmalen
        pass

rg = PygameRandomWeightedGraph(8)
rg.show()