from Dependencies.Utilities import timeFunction, splitEveryNth, randomUnorderedSampleList

class BTree:
    def __init__(self, numericalList=None):
        if numericalList is None or len(numericalList) < 1:
            self.root = None
            self.dictRep = None
            self.nodeAmount = None
            self.degree = None
            self.levels = None
        else:
            self.treeByList(numericalList)

    def treeByList(self, numericalList):
        self.nodeAmount = 0
        self.degree = 2
        self.root = self.__createNodes(sorted(numericalList))
        self.dictRep = self.__breadthTraverse()
        self.levels = list(self.dictRep)[-1]+1

    def __createNodes(self, nextValues):
        if len(nextValues) == 0:
            return None
        else:
            self.nodeAmount += 1
            middleIndex = len(nextValues) // 2
            left = nextValues[:middleIndex]
            right = nextValues[middleIndex+1:]
            return BTree.Node(self.__createNodes(left), self.__createNodes(right), nextValues[middleIndex])

    def __breadthTraverse(self):
        next = [self.root]
        found = {}
        level = 0
        while len(next) > 0:
            new = []
            found[level] = []
            for i in next:
                found[level].append(i.value)
                if i.left is not None:
                    new.append(i.left)
                if i.right is not None:
                    new.append(i.right)
            next = new
            level += 1
        for lvl in found:
            found[lvl] = splitEveryNth(found[lvl], 2)
        return found

    def find(self, value):
        other = self.root
        while 1:
            if other == None:
                return False
            elif other.value == value:
                return True
            elif other.value > value:
                other = other.left
            else:
                other = other.right

    def __str__(self):
        string = ""
        baseLength = len(str(self.dictRep[self.levels-1]))
        for lvl in self.dictRep:
            nString = f"{self.dictRep[lvl]}\n"
            string += (baseLength-len(nString))//2 * " " + nString
        return string

    class Node:
        def __init__(self, left, right, value):
            self.left = left
            self.right = right
            self.value = value
        def __str__(self):
            return str(self.value)

@timeFunction
def createRandomBTree(rangeObj, valueAmount):
    return BTree(randomUnorderedSampleList(rangeObj, valueAmount))


if __name__ == "__main__":
    r, time = createRandomBTree(range(0, 100) ,100)
    print(r)
    print(f"Runtime {time}s")

    print(r.find(100))