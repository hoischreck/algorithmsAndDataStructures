from Dependencies.PygameClass2.PygameClass2Core.functions import *


class GameObject():
    def __init__(self, screen, pos, size, color, name):
        self.screen = screen
        self.name = name
        self.size = size
        self.color = color
        self.__x, self.__y = pos
        self.__direction = 0
        self.bounced = 0

    def change_x_by(self, x):
        self.__x += x
    def change_y_by(self, y):
        self.__y += y
    def follow_Direction_by(self, pixels):
        self.__x += math.cos(dirToRad(self.__direction)) * pixels
        self.__y += math.sin(dirToRad(self.__direction)) * pixels
    def set_x_y(self, pos):
        self.__x, self.__y = pos
    def set_x(self, x):
        self.__x = x
    def set_y(self, y):
        self.__y = y
    def __controlDirection(self):
        self.__direction = self.__direction-(self.__direction//360)*360
    def set_direction(self, angle):
        self.__direction = angle
        self.__controlDirection()
    def change_dircetion_by(self, angle):
        self.__direction += angle
        self.__controlDirection()
    def set_color(self, color):
        self.color = color
    def draw_line_into_direction(self, direction_in_degree, length, width=10, color=(0, 0, 0)):
        direction_in_degree = direction_in_degree-(direction_in_degree//360)*360
        form1 = lambda len, angle: math.cos(dirToRad(angle))*len
        form2 = lambda len, angle: math.sin(dirToRad(angle))*len
        if direction_in_degree >= 0 and direction_in_degree < 90:
            x, y = form1(length, direction_in_degree), form2(length, direction_in_degree)
        elif direction_in_degree >= 90 and direction_in_degree < 180:
            direction_in_degree -= 90
            x, y = -form2(length, direction_in_degree), form1(length, direction_in_degree)
        elif direction_in_degree >= 180 and direction_in_degree < 270:
            direction_in_degree -= 180
            x, y = -form1(length, direction_in_degree), -form2(length, direction_in_degree)
        elif direction_in_degree >= 270:
            direction_in_degree -= 270
            x, y = form2(length, direction_in_degree), -form1(length, direction_in_degree)
        if type(self) == Circle2D:
            pygame.draw.line(self.screen, color, self.x_y_position(), (x+self.x_position(), y+self.y_position()),width)
        else:
            pygame.draw.line(self.screen, color, self.x_y_position_center(), (x+self.x_position_center(), y+self.y_position_center()), width)

    def x_position(self):
        return self.__x
    def y_position(self):
        return self.__y
    def x_y_position(self):
        return self.__x, self.__y
    def x_position_center(self):
        return self.__x + (self.size[0]/2)
    def y_position_center(self):
        return self.__y + (self.size[1]/2)
    def x_y_position_center(self):
        return self.__x + (self.size[0]/2), self.__y + (self.size[1]/2)
    def directionAsAngle(self):
        self.__controlDirection()
        return self.__direction

    def direction_relativ_to(self, gameObject_or_pos):
        if type(gameObject_or_pos) == type(self):
            x, y = gameObject_or_pos.x_position_center()-self.x_position_center(), gameObject_or_pos.y_position_center()-self.y_position_center()
        else:
            x, y = gameObject_or_pos
        if x == 0 and y < 0:
            return 270
        elif  x == 0 and y > 0:
            return 90
        elif  y == 0 and x < 0:
            return 180
        elif  (y == 0 and x > 0) or (y == 0 and x == 0):
            return 0
        elif x > 0 and y > 0:
            return radToDir(math.atan(y/x))
        elif x < 0 and y > 0:
            return 90 + radToDir(math.atan(abs(x)/y))
        elif x < 0 and y < 0:
            return 180 + radToDir(math.atan(abs(y)/abs(x)))
        elif x > 0 and y < 0:
            return 270 + radToDir(math.atan(x/abs(y)))
    def distance_to_center_of(self, gameObject):
        return math.sqrt((self.x_position_center() - gameObject.x_position_center())**2+(self.y_position_center() - gameObject.y_position_center())**2)
    def collides_With(self, gameObject):
        width1, height1, width2, height2 = self.size[0], self.size[1], gameObject.size[0], gameObject.size[1]
        if self.__x <= gameObject.__x and self.__y <= gameObject.__y:
            xWidth, yHeight = gameObject.__x + width2 - self.__x, gameObject.__y + height2 - self.__y
        elif self.__x >= gameObject.__x and self.__y <= gameObject.__y:
            xWidth, yHeight = self.__x + width1 - gameObject.__x, gameObject.__y + height2 - self.__y
        elif self.__x <= gameObject.__x and self.__y >= gameObject.__y:
            xWidth, yHeight = gameObject.__x + width2 - self.__x, self.__y + height1 - gameObject.__y
        elif self.__x >= gameObject.__x and self.__y >= gameObject.__y:
            xWidth, yHeight = self.__x + width1 - gameObject.__x, self.__y + height1 - gameObject.__y
        if (width1+width2) > xWidth and (height1+height2) > yHeight:
            return True
        return False
    def leaves_fully(self, gameObject):
        return False if self.collide_With(gameObject) else True
    def touches_Windowborder(self):
        x, y = self.screen.get_size()
        w, h = self.size
        if self.__x + w > x or self.__y + h > y or self.__x < 0 or self.__y < 0:
            return True
        self.bounced = 0
        return False

    def touches_which_Windowborder(self):
        x, y = self.screen.get_size()
        w, h = self.size
        if self.__x + w > x:
            return RightSide
        elif self.__y + h > y:
            return BottomSide
        elif self.__x < 0:
            return LeftSide
        elif self.__y < 0:
            return UpperSide

    def bounce(self):
        if self.bounced == 0:
            self.bounced = 1
            direction = self.directionAsAngle()
            side = self.touches_which_Windowborder()
            if direction in [0, 90, 180, 270]:
                self.set_direction(direction+180)
            else:
                if side in [LeftSide, RightSide]:
                    if direction > 0 and direction < 180:
                        self.set_direction(180-direction)
                    else:
                        self.set_direction(direction-180)
                else:
                    if direction > 0 and direction < 180:
                        self.set_direction(360-direction)
                    else:
                        self.set_direction(direction-360)
            self.follow_Direction_by(1)


    def gotoMouse(self):
        x, y = pygame.mouse.get_pos()
        self.set_x_y((x - self.size[0]/2, y - self.size[1]/2))
    def draw_line_to(self, target_object, color=(0, 0, 0), width=10):
        pygame.draw.line(self.screen, color, self.x_y_position_center(), target_object.x_y_position_center(), width)

class Rectangle2D(GameObject):
    def __init__(self, screen, pos, size, color, name):
        super().__init__(screen, pos, size, color, name)
        self.form = pygame.Rect((self.x_position(), self.y_position()), self.size)
        self.drawAtt = self.__draw
    def __draw(self):
        self.form = pygame.Rect((self.x_position(), self.y_position()), self.size)
        pygame.draw.rect(self.screen, self.color, self.form)

class UnionRectangle2D(GameObject):
    def __init__(self, screen, RectangleUnion, color):
        self.color = color
        self.screen = screen
        self.form = RectangleUnion
        self.drawAtt = self.__draw
    def __draw(self):
        pygame.draw.rect(self.screen, self.color, self.form)

class Circle2D(GameObject):
    def __init__(self, screen, pos, size, color, name):
        super().__init__(screen, pos, size, color, name)
        self.size = (size, size)
        self.drawAtt = self.__draw
    def __draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x_position()), int(self.y_position())), self.size[0])

class Text2D(GameObject):
    def __init__(self, screen, pos, size, name, color, text, fonts, bold):
        super().__init__(screen, pos, size, name, color)
        self.font = self.__getFont(size, fonts)
        self.bold = bold
        self.__text = text
        self.pos = pos
        self.color = color
        self.fontDisplay = self.font.render(self.__text, True, self.color)
        self.drawAtt = self.__draw
    def __draw(self):
        self.fontDisplay = self.font.render(self.__text, True, self.color)
        self.screen.blit(self.fontDisplay, self.pos)
    def set_Text(self, text):
        self.__text = text
    def get_Text(self):
        return self.__text
    def change_Bold(self):
        if self.bold == True:
            self.bold = False
        else:
            self.bold = True
    def __getFont(self, size, fonts):
        choosen = map(lambda x: x.lower().replace(" ","") ,list(fonts))
        availableFonts = pygame.font.get_fonts()
        for c in choosen:
            if c in availableFonts:
                return pygame.font.SysFont(c, size)
        return pygame.font.Font(None, size)
    def __fontSetup(self):
        if self.bold == True:
            self.font.set_bold(True)
        else:
            self.font.set_bold(False)

class Side():
    def __init__(self):
        self.side = None
class LeftSide(Side):
    def __init__(self):
        self.side = "left"
class RightSide(Side):
    def __init__(self):
        self.side = "right"
class UpperSide(Side):
    def __init__(self):
        self.side = "upper"
class BottomSide(Side):
    def __init__(self):
        self.side = "bottom"