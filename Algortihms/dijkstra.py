from collections import namedtuple

nVertex = namedtuple("nVertex", "neighbour cost")
VertexEntry = namedtuple("VertexEntry", "vertex cost previous")

class Graph:
    def __init__(self, adjacencyList):
        self.adjacencyList = adjacencyList
        self.vertices = self.__allVertices()
        self.dDictionary = {}

    def __allVertices(self):
        return set(self.adjacencyList.keys())

    def getNeighbours(self, vertex):
        return self.adjacencyList[vertex]

    def createDijkstraList(self, startVertex):
        unchecked = self.vertices
        vertexCost = {v: float("inf") if v != startVertex else 0 for v in self.vertices}
        prevVertex = {v: None for v in self.vertices}
        v = startVertex
        while True:
            unchecked.remove(v)
            vertexNeighbours = self.getNeighbours(v)
            for i in [n for n in vertexNeighbours if n.neighbour in unchecked]:
                n, cost = i.neighbour, i.cost
                if vertexCost[n] == float("inf") or vertexCost[n] > vertexCost[v] + cost:
                    vertexCost[n] = vertexCost[v] + cost
                    prevVertex[n] = v
            if len(unchecked) > 0:
                v = sorted([(i, vertexCost[i]) for i in unchecked], key=lambda x : x[1])[0][0]
            else:
                break
        self.dDictionary[startVertex] = {v:VertexEntry(v, vertexCost[v], prevVertex[v]) for v in vertexCost}

    def shortestPath(self, start, end):
        if start not in self.dDictionary:
            self.createDijkstraList(start)
        path = []
        current = self.dDictionary[start][end]
        while True:
            path.append(current.vertex)
            if current.previous is not None:
                current = self.dDictionary[start][current.previous]
            else:
                return (path[::-1], self.dDictionary[start][end].cost)

if __name__ == "__main__":
    # exampleData: graph1.png
    g = Graph({
        'a': {nVertex('c', 4), nVertex('b', 1), nVertex('e', 9)},
        'b': {nVertex('a', 1), nVertex('f', 6), nVertex('e', 7)},
        'c': {nVertex('f', 7), nVertex('d', 2), nVertex('a', 4)},
        'd': {nVertex('c', 2)},
        'e': {nVertex('a', 9), nVertex('b', 7), nVertex('f', 4)},
        'f': {nVertex('c', 7), nVertex('e', 4), nVertex('b', 6)}
    })
    shortest = g.shortestPath('f', 'a')
    print(shortest)

