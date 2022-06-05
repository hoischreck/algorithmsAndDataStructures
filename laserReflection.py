import numpy as np
import pygame, numpy

pygame.init()

class LaserReflection:
	def __init__(self, size, reflectionDepth, lineStrength=4, tps=60):
		self.size = size
		self.w, self.h = size
		self.backgroundColor = (255, 255, 255)
		self.tps = tps
		assert reflectionDepth > 1, "Reflection-depth must be greater than 1"
		self.reflectionDepth = reflectionDepth
		self.lineStrength = lineStrength

		self.running = False
		self.start = None

	def run(self):
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()
		self.running = True
		lines = []  # list of tuples, with represent a start and an endpoint

		while self.running:
			self.screen.fill(self.backgroundColor)
			keys = pygame.key.get_pressed()

			if keys[pygame.K_UP]:
				self.reflectionDepth += 1
				print("reflection depth:", self.reflectionDepth)
				lines = self._calcIntersections()
			elif keys[pygame.K_DOWN]:
				if self.reflectionDepth > 2:
					self.reflectionDepth -= 1
					print("reflection depth:", self.reflectionDepth)
					lines = self._calcIntersections()


			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					self.running = False

				if e.type == pygame.MOUSEBUTTONUP:
					self.start = LaserStart(pygame.mouse.get_pos(), self.screen)

				if e.type == pygame.MOUSEMOTION:
					if self.start is None:
						break

					lines = self._calcIntersections()

			#red = (255, 0, 0)
			if len(lines) > 0:
				q  = 255 / len(lines)
				for c, l in enumerate(lines[::-1]):
					fade = 255 - int(c*q)
					color = (255, fade, fade) #fix this
					pygame.draw.line(self.screen, color, *l, 4)

			if self.start is not None:
				self.start.draw()


			self.clock.tick(self.tps)
			pygame.display.flip()

	def _calcIntersections(self):
		m, s = numpy.array(pygame.mouse.get_pos()), numpy.array(self.start.pos)
		v = m - s
		# g: x = s + rv

		lines = []
		for i in range(self.reflectionDepth):
			if v[0] == 0:
				# hacky?
				lines.append((s, numpy.array([s[0], 0])))
				lines.append((s, numpy.array([s[0], self.h])))
				break
			elif v[1] == 0:
				lines.append((numpy.array([0, s[1]]), s))
				lines.append((numpy.array([self.h, s[1]]), s))
				break

			if v[0] < 0:
				r = -s[0] / v[0]
			else:
				r = (self.w - s[0]) / v[0]
			if v[1] < 0:
				w = -s[1] / v[1]
			else:
				w = (self.h - s[1]) / v[1]

			intersection = None
			if abs(r) < abs(w):
				intersection = s + r * v
				v[0] = -v[0]
			elif abs(r) > abs(w):
				intersection = s + w * v
				v[1] = -v[1]
			lines.append((s, intersection))
			s = intersection
		return lines

class LaserStart:
	def __init__(self, pos, screen, color=(0, 220, 0), radius=15):
		self.pos = pos

		self.screen = screen
		self.color = color
		self.radius = radius

	def draw(self):
		pygame.draw.circle(self.screen, self.color, self.pos, self.radius)

if __name__ == "__main__":
	lr = LaserReflection(size=(2000, 1000), reflectionDepth=2, lineStrength=2, tps=60)
	lr.run()