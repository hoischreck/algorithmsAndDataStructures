from Dependencies.PygameClass2.PygameClass2Core.GameObjects import *
from Dependencies.PygameClass2.PygameClass2Core.drawingQueue import *

class Collection():
    def __init__(self, game):
        self.game = game
    def simple_Controller_WASD(self, speed, *GameObjects):
        if self.game.key.held_down(pygame.K_w):
            [i.change_y_by(-speed) for i in GameObjects]
        if self.game.key.held_down(pygame.K_s):
            [i.change_y_by(speed) for i in GameObjects]
        if self.game.key.held_down(pygame.K_d):
            [i.change_x_by(speed) for i in GameObjects]
        if self.game.key.held_down(pygame.K_a):
            [i.change_x_by(-speed) for i in GameObjects]
    #def glide_to(self, time)
    def random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))