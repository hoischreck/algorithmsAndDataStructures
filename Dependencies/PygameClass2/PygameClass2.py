from Dependencies.PygameClass2.PygameClass2Core.GameObjects import *
from Dependencies.PygameClass2.PygameClass2Core.drawingQueue import *
from Dependencies.PygameClass2.PygameClass2Collection import Collection

class Game():
    def __init__(self, name="NoName"):
        self.name = name
        self.windowSize = (1920, 1080)
        self.windowCaption = "Window"
        self.backgroundColor = (255, 255, 255)
        self.__backgroundImage = None
        self.running = False
        self.tickrate = 10
        self.processtime = 0
        self.tps = 0
        self.tick_count = 0
        self.info_color = [0, 0, 0]
        self.events = []

        self.runtime_display = False
        self.tps_display = False
        self.rotateScreenY = False

        self.gameObjects = []
        self.drawingQueue = DrawerQueue()

        self.key = Keys(pygame.key.get_pressed(), self.events)
        self.mouse = Mouse(pygame.mouse.get_pressed(), self.events)
        self.add = Objects(self)
        self.collection = Collection(self)
        self.time = Time()

    def loop(self, func):
        def Gameloop(*args, **kwargs):
            processStart, tickStart = time.time(), time.time()
            self.__mainOpen()
            r = func(*args, **kwargs)
            self.processtime = time.time() - processStart
            self.__mainClose()
            self.tps = 1 / (time.time() - tickStart)
            return r
        return Gameloop

    def init(self):
        self.screen = pygame.display.set_mode(self.windowSize)
        pygame.display.set_caption(self.windowCaption)
        if self.__backgroundImage != None:
            self.__backgroundImage = pygame.image.load(self.__backgroundImage).convert()
        self.running = True

    def __mainOpen(self):
        self.fill_Background()
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                sys.exit()
        self.key = Keys(pygame.key.get_pressed(), self.events)
        self.mouse = Mouse(pygame.mouse.get_pressed(), self.events)
        self.drawingQueue._draw()


    def __mainClose(self):
        if self.tps_display == True:
            self.drawingQueue.drawOnce((self.add.Text2D((self.windowSize[0]-380, 0), 50, draw=False, text=f"runtime: {secondsToFormat(int(self.time.runtime()))}s", color=self.info_color), 0))
        if self.runtime_display == True:
            self.drawingQueue.drawOnce((self.add.Text2D((10, 0), 50, bold=True, draw=False, text=f"ticks/second: {int(self.tps)}", color=self.info_color), 0))
        self.tick_count += 1
        #may be slow
        if self.rotateScreenY:
            self.screen.blit(pygame.transform.rotate(self.screen, 180), (0, 0))
        pygame.display.flip()
        pygame.time.wait(self.tickrate)

    def delete_Form(self, object):
        self.drawingQueue.removeObjects(object)
        del object

    def fill_Background(self):
        if type(self.__backgroundImage) == pygame.Surface:
            self.load_Background_Image()
        else:
            self.fill_Background_with_Color()

    def fill_Background_with_Color(self, color=None):
        if color == None:
            self.screen.fill(self.backgroundColor)
        else:
            self.screen.fill(color)

    def set_Background_Image(self, ImagePath):
        if ImagePath == None:
            self.__backgroundImage = None
        elif self.running == False:
            self.__backgroundImage = ImagePath
        else:
            self.__backgroundImage = pygame.image.load(ImagePath).convert()

    def load_Background_Image(self, Img=None):
        if Img == None:
            self.screen.blit(self.__backgroundImage, (0,0))
        else:
            self.screen.blit(pygame.image.load(Img).convert(), (0, 0))

    def take_screenshot(self, path, subsurface=None):
        if subsurface != None:
            if len(subsurface) > 2:
                n = 2
                subsurface = [subsurface[i:i + n] for i in range(0, len(subsurface), n)]
            else:
                subsurface = [list(i) for i in subsurface]
            if subsurface[1][0] + subsurface[0][0] > self.game.windowSize[0]:
                subsurface[1][0] = self.game.windowSize[0] - subsurface[0][0]
            if subsurface[1][1] + subsurface[0][1] > self.game.windowSize[1]:
                subsurface[1][1] = self.game.windowSize[1] - subsurface[0][1]
            sub = self.game.screen.subsurface(pygame.Rect(*subsurface))
        else:
            self.game.screen.subsurface(pygame.Rect((0,0), self.game.windowSize))
        pygame.image.save(sub, path)

    def draw_line(self, start_pos, end_pos, color=(255, 0, 0), width=10):
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)

class Objects(Game):
    def __init__(self, game):
        self.game = game
    def __addToQueue(self, obj):
        self.game.drawingQueue.addObjects((obj[0].drawAtt, obj[1]))
    def Rectangle2D(self, position, size, color, name="Rectangle2D", draw=True, drawPriority=-1):
        form = Rectangle2D(self.game.screen, position, size, color, name)
        self.game.gameObjects.append(form)
        if draw == True: self.__addToQueue((form, drawPriority))
        return form
    def Circle2D(self, position, radius, color, name="Circle2D", draw=True, drawPriority=-1):
        form = Circle2D(self.game.screen, position, radius, color, name)
        self.game.gameObjects.append(form)
        if draw == True: self.__addToQueue((form, drawPriority))
        return form
    def Text2D(self, position, size, text="Insert Text Here", color=(0, 0, 0), name="Text2D", fonts = ["arial", "bahnschrift", "calibri"], bold = True, draw=True, drawPriority=-1):
        form = Text2D(self.game.screen, position, size, name, color, text, fonts, bold)
        self.game.gameObjects.append(form)
        if draw == True: self.__addToQueue((form, drawPriority))
        return form
    def Pen(self, gameObject=None, drawPriority=0):
        pen = Pen(self.game, gameObject)
        self.game.gameObjects.append(pen)
        self.__addToQueue((pen, drawPriority))
        return pen
    def Timer(self):
        return Time()

class Keys():
    def __init__(self, pygameKeys, pygameEvents):
        self.keys = pygameKeys
        self.events = pygameEvents
    def held_down(self, pygameKey):
        if self.keys[pygameKey]:
            return True
    def clicked(self, pygameKey):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygameKey:
                    return 1


class Mouse():
    def __init__(self, pygamePressed, pygameEvents):
        self.mouseButtons = pygamePressed
        self.events = pygameEvents
    def held_down(self, mouseButton=None):
        if mouseButton != None:
            if self.mouseButtons[0] == 1 and mouseButton == 1:
                return True
            if self.mouseButtons[1] == 1 and mouseButton == 2:
                return True
            if self.mouseButtons[2] == 1 and mouseButton == 3:
                return True
        else:
            if 1 in self.mouseButtons:
                return True
    def position(self):
        return pygame.mouse.get_pos()
    def set_position(self, pos):
        return pygame.mouse.set_pos(pos)
    def clicked(self, mouseButton=None):
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouseButton != None:
                    if self.mouseButtons[0] == 1 and mouseButton == 1:
                        return True
                    if self.mouseButtons[1] == 1 and mouseButton == 2:
                        return True
                    if self.mouseButtons[2] == 1 and mouseButton == 3:
                        return True
                else:
                    return True

class Time():
    def __init__(self):
        self.startTime = time.time()
    def runtime(self):
        return time.time() - self.startTime

class Pen():
    def __init__(self, game, gameObject=None, color=(0, 0, 0)):
        self.game = game
        self.color = color
        self.gameObj = gameObject
        self.drawObj = []
        self.drawQueue = DrawerQueue()
        self.drawAtt = self.__drawObject
        self.originalImg = None

    def draw(self):
        if self.gameObj == None:
            self.drawObj.append(Rectangle2D(self.game.screen, pygame.mouse.get_pos(), (20, 20), self.color, ""))
        else:
            if type(self.gameObj) == Circle2D:
                x, y = self.gameObj.x_position(), self.gameObj.y_position()
            else:
                x, y = self.gameObj.x_position() + self.gameObj.size[0]/2, self.gameObj.y_position() + self.gameObj.size[1]/2
            self.drawObj.append(Rectangle2D(self.game.screen, (x, y), (20, 20), self.color, ""))

    def erase_all(self):
        self.drawObj = []

    def __drawObject(self):
        self.drawQueue = DrawerQueue([i.drawAtt for i in self.drawObj])
        self.drawQueue._draw()