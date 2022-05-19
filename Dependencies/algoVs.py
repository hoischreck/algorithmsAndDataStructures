from Dependencies.PygameClass2.PygameClass2 import *
from Dependencies.Utilities import timeFunction

class AlgoSortingVs():
    signalColor = (255, 0, 0)
    def __init__(self, algorithm, mutableIterable, colorFunction = None, **algorithmArguments):
        self.game = Game()
        self.game.name = "AlgoVs"
        self.game.windowCaption = "AlgoVs"
        self.game.backgroundColor = (255, 255, 255)
        self.game.set_Background_Image("testImg1.jpg")
        #schlechte Lösung
        self.game.rotateScreenY = False
        self.game.windowSize = (1920, 1080)
        self.game.tickrate = 0
        self.game.runtime_display = True
        self.game.tps_display = True
        self.game.init()
        self.__main = self.game.loop(self._main)

        if colorFunction is None:
            self.colorFunction = self.game.collection.random_color
        else:
            self.colorFunction = colorFunction
        self.list = AlgoSortingVs._VisualArray(mutableIterable, self)
        self.bars = list()
        self.tmp = None

        if len(algorithmArguments) != 0:
            self.algorithm = algorithm(self.list, algorithmArguments)
        else:
            self.algorithm = algorithm(self.list)

        #not implemented yet
        self.reverse = True

        self.finished = False


    def visualize(self):
        self.__createBars()
        timer = self.game.add.Timer()
        while self.game.running:
            if self.__main():
                self.finished = True
                print(f"Die Sortierung dauerte {timer.runtime()}s")
                del timer


    def _main(self):
        if not self.finished:
            a = self.__next()
            if a == None:
                self.bars[self.tmp[0]].set_color(self.tmp[1])
                return True #array is sorted
            else:
                if self.tmp != None:
                    self.bars[self.tmp[0]].set_color(self.tmp[1])
                b = self.bars[a]
                self.tmp = [a, b.color]
                b.set_color(AlgoSortingVs.signalColor)

    def __next(self):
        try:
            return next(self.algorithm)
        except StopIteration:
            return None

    def __createBars(self):
        barAmount = len(self.list)
        barWidth = self.game.windowSize[0] / barAmount
        greatesElement = max(self.list)

        for i in range(len(self.list)):
            pos = (i*barWidth, 0)
            barHeight = self.game.windowSize[1] * (self.list[i]/greatesElement * 1)
            color = self.colorFunction()
            self.bars.append(self.game.add.Rectangle2D(pos, (int(barWidth)+1, barHeight), color))

    def _swapBars(self, index1, index2):
        if self.tmp != None:
            if index1 == self.tmp[0]:
                self.tmp[0] = index2
            elif index2 == self.tmp[0]:
                self.tmp[0] = index1

        bar1, bar2 = self.bars[index1], self.bars[index2]
        self.bars[index1], self.bars[index2] = self.bars[index2], self.bars[index1]
        bar1tmpX = bar1.x_position()
        bar1.set_x(bar2.x_position())
        bar2.set_x(bar1tmpX)



    class _VisualArray(list):
        def __init__(self, numericList, algoVsObj):
            super().__init__(numericList)
            self.avs = algoVsObj

        def swap(self, index1, index2):
            self.avs._swapBars(index1, index2)
            self[index1], self[index2] = self[index2], self[index1]

def swap(mutableIterable, index1, index2):
    mutableIterable[index1], mutableIterable[index2] = mutableIterable[index2], mutableIterable[index1]

def swapAvs(mutableIterable, index1, index2):
    mutableIterable.swap(index1, index2)