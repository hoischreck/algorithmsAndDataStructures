class DrawerQueue():
    def __init__(self, drawFunctionsWithPriority=[]):
        self.functions = []
        self.addObjects(drawFunctionsWithPriority)
        self.__drawOnceList = []
    def __initQueue(self):
        self.objects = {}
        self.__getObjectQueue()
        self.objects = self.__objsToList()
    def __getObjectQueue(self):
        for func in self.functions:
            if type(func) != tuple:
                self.objects[func] = -1
            else:
                self.objects[func[0]] = func[1]
    def __objsToList(self):
        last = [func for func in self.objects if self.objects[func] == -1]
        queue = sorted([(func, self.objects[func]) for func in self.objects if self.objects[func] != -1], key=lambda x: x[1])
        queue = [i[0] for i in queue]
        final = queue + last[::-1]
        return final[::-1]
    def addObjects(self, objects):
        if type(objects) != list:
            objects = [objects]
        [self.functions.append(i) for i in objects]
        self.__initQueue()
    def removeObjects(self, objects):
        if type(objects) != list:
            objects = [objects]
        for i in objects:
            for indx, func in enumerate(self.functions):
                if type(func) == tuple and func[0] == i.drawAtt:
                    self.functions.pop(indx)
                elif type(func) != tuple and func == i.drawAtt:
                    self.functions.pop(indx)
        self.__initQueue()
    def changePriority(self, object, priority):
        indx = [i[0] for i in self.functions].index(object.drawAtt)
        self.functions[indx] = self.functions[indx][0], priority
        self.__initQueue()
    def drawOnce(self, objects):
        if type(objects) != list:
            objects = [objects]
        try:
            self.addObjects(list([(i[0].drawAtt, i[1]) for i in objects]))
        except TypeError:
            raise SyntaxError("no drawpriority givin")
        self.__drawOnceList += list(map(lambda x: x[0], objects))
    def _draw(self):
        for func in self.objects:
            func()
        self.removeObjects(self.__drawOnceList)
        self.__drawOnceList = []