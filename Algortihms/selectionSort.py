from Dependencies.algoVs import swap, swapAvs

def selectionSort(mutableList):
    for i in range(len(mutableList)-1):
        smallest = i
        for c, j in enumerate(mutableList[i+1:]):
            if j < mutableList[smallest]:
                smallest = c + i + 1
        if smallest != i:
            swap(mutableList, i, smallest)
    return mutableList

def selectionSortAvs(mutableList):
    for i in range(len(mutableList)-1):
        smallest = i
        for c, j in enumerate(mutableList[i+1:]):
            if j < mutableList[smallest]:
                smallest = c + i + 1
            yield c + i + 1
        if smallest != i:
            swapAvs(mutableList, i, smallest)
    #return mutableList