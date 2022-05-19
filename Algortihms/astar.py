import pygame, sys, random, math

pygame.init()

# setup

size = (1000, 1000) # screen size
vertexDensity = 1/100 # vertices per px
radius = 10

backgroundColor = (255, 255, 255)
visitedColor = (0, 200, 0)

screen = pygame.display.set_mode(size)

class AStarVisualization:
	def __init__(self, size=(1000, 1000), vertexDensity=1/100, vertexRadius=15, tps=10, eraseRadius=15):
		self.size = size
		self.vertexDensity = vertexDensity
		self.vertexRadius = vertexRadius
		self.tps = tps
		self.backgroundColor = (255, 255, 255)
		self.baseColor = (150, 150, 150)
		self.startColor = (0, 220, 0)
		self.endColor = (220, 0, 0)
		self.eraseColor = (36, 36, 36)
		self.pathColor = (0, 0, 220)
		self.eraseRadius = eraseRadius

		self.adjacencyList = None
		self.vertexMatrix = None
		self.allVertices = None

		self.startVertex = None
		self.endVertex = None

		self.started = False
		self.finished = False
		self.solutionFound = False

	def run(self):
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

		if self.vertexMatrix is None:
			self._buildVertexMatrix()

		algorithm = None
		drag = False

		print("Select a start and end Vertex")

		while True:
			self.screen.fill(self.backgroundColor)

			# check events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.MOUSEBUTTONUP:
					drag = False
					pos = pygame.mouse.get_pos()
					for v in self.allVertices:
						distance = math.sqrt((pos[0]-v.pos[0])**2 + (pos[1]-v.pos[1])**2)
						if distance - self.vertexRadius <= 0:
							# v was clicked
							if event.button == 1:
								if self.startVertex is None:
									self.startVertex = v
									v.gameObj.color = self.startColor
									print("You selected a start vertex at the position:", "{}x {}y".format(*v.pos))
								elif self.endVertex is None:
									self.endVertex = v
									v.gameObj.color = self.endColor
									print("You selected an end vertex at the position:", "{}x {}y".format(*v.pos))
									print("If you want to start the algorithm press 'ENTER'")
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 3:
						drag = True
				if event.type == pygame.MOUSEMOTION:
					if drag:
						if self.startVertex is None and self.endVertex is None:
							pos = pygame.mouse.get_pos()
							for x, column in enumerate(self.vertexMatrix):
								for y, v in enumerate(column):

									distance = math.sqrt((pos[0] - v.pos[0]) ** 2 + (pos[1] - v.pos[1]) ** 2)
									if distance - self.vertexRadius - self.eraseRadius <= 0:
										v.gameObj.color = self.eraseColor
										v.checkable = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						if self.startVertex is not None and self.endVertex is not None and self.started == False:
							self.started = True
							for v in self.allVertices:
								if v not in (self.startVertex, self.endVertex) and v.checkable:
									v.gameObj.hide = True
							algorithm = self._astar()

							print("Starting!")

			# logic

			if self.started and not self.finished:
				try:
					active = next(algorithm)
					active.gameObj.hide = False
				except StopIteration:
					print(">>The algorithm has finished!")
					print(">>{} path was found".format("A" if self.solutionFound else "No"))
					self.finished = True

			for x in self.vertexMatrix:
				for y in x:
					y.draw()
			# handle screen
			self.clock.tick(self.tps)
			pygame.display.flip()

	def _drawPath(self, previous):
		if not self.solutionFound:
			return

		before = previous[self.endVertex]
		while True:
			before = previous[before]
			if before is None:
				break
			before.gameObj.color = self.pathColor


	def _astar(self):
		# algorithm initialization
		# 1. cost of all vertices
		# 2. predecessors of all vertices
		# 3. unchecked set
		self._buildAdjacencyList()
		verticeCosts = {v: float("inf") if v != self.startVertex else 0 for v in self.adjacencyList}
		heuristicCosts = {v: self._heuristic(v, self.endVertex) for v in self.adjacencyList}
		previous = {v: None for v in self.adjacencyList}
		unchecked = {i for i in self.adjacencyList if i.checkable}

		current = self.startVertex
		while True:
			unchecked.remove(current)
			neighbours = self.adjacencyList[current]
			for nw in [i for i in neighbours if i[0] in unchecked]:
				n, w = nw
				if verticeCosts[n] > verticeCosts[current] + w:

					verticeCosts[n] = verticeCosts[current] + w
					previous[n] = current

			yield current

			if len(unchecked) < 1:
				break

			tmpCosts = {v: verticeCosts[v] + heuristicCosts[v] for v in verticeCosts}
			current = self._cheapestVertex(tmpCosts, unchecked)
			if verticeCosts[current] == float("inf"):
				break #no solution was found
			#current = self._cheapestVertex(verticeCosts, unchecked) # dijkstra
			if current == self.endVertex:
				self.solutionFound = True
				self._drawPath(previous)
				break

		# add heuristic

	def _cheapestVertex(self, costDict, unchecked):
		return sorted([(i, costDict[i]) for i in unchecked], key=lambda x: x[1])[0][0]

	def _heuristic(self, v1, v2):
		return math.sqrt((v1.pos[0]-v2.pos[0])**2 + (v1.pos[1]-v2.pos[1])**2)

	def _buildVertexMatrix(self):
		self.allVertices = set()
		self.xAmount = int(self.size[0] * self.vertexDensity)
		self.yAmount = int(self.size[1] * self.vertexDensity)

		self.vertexMatrix = [[] for _ in range(self.xAmount)]

		for x in range(self.xAmount):
			for y in range(self.yAmount):
				pos = (
					x / self.vertexDensity + self.size[0] / (2 * self.xAmount),
					y / self.vertexDensity + self.size[1] / (2 * self.yAmount)
				)
				v = Vertex(
						pos,
						Circle(self.screen, pos, self.vertexRadius, self.baseColor)
					)
				self.vertexMatrix[x].append(v)
				self.allVertices.add(v)

	def _buildAdjacencyList(self):
		self.adjacencyList = {}

		weight = 1

		for x, column in enumerate(self.vertexMatrix):
			for y, rowElement in enumerate(column):
				self.adjacencyList[rowElement] = set()
				# add neighbours
				if x > 0:
					self.adjacencyList[rowElement].add((self.vertexMatrix[x - 1][y], weight))
				if x < self.xAmount - 1:
					self.adjacencyList[rowElement].add((self.vertexMatrix[x + 1][y], weight))
				if y > 0:
					self.adjacencyList[rowElement].add((self.vertexMatrix[x][y - 1], weight))
				if y < self.yAmount - 1:
					self.adjacencyList[rowElement].add((self.vertexMatrix[x][y+1], weight))

def randomRGB():
	return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

class Vertex:
	def __init__(self, position, gameObj, checkable=True):
		self.pos = position
		self.gameObj = gameObj
		self.checkable = checkable

	def draw(self):
		self.gameObj.draw()

class Circle:
	def __init__(self, screen, pos, radius, color):
		self.screen = screen
		self.pos = pos
		self.radius = radius
		self.color = color
		self.hide = False

	def draw(self):
		if not self.hide:
			pygame.draw.circle(self.screen, self.color, self.pos, self.radius)

if __name__ == "__main__":
	aStarV = AStarVisualization(vertexDensity=10/100, vertexRadius=6, tps=1000, eraseRadius=10)
	aStarV.run()

