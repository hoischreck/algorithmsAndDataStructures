from Dependencies.algoVs import *
from Algortihms.selectionSort import selectionSortAvs
from Dependencies.Utilities import randomUnorderedList, randomUnorderedSampleList

color = lambda: (0, 0, 255)

a = AlgoSortingVs(algorithm=selectionSortAvs, mutableIterable=randomUnorderedSampleList(range(1, 501), 50), colorFunction=color)

a.visualize()
