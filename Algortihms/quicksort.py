from Dependencies.Utilities import randomUnorderedList

def quicksort(unsortedList, startIndex=None, endIndex=None):
    def _partionate(unsortedList, left, right):
        i, j = left, right-1
        pivotElement = unsortedList[endIndex]
        while i < j:
            while i < right and unsortedList[i] < pivotElement:
                i += 1
            while j > left and unsortedList[j] >= pivotElement:
                j -= 1
            if i < j:
                unsortedList[i], unsortedList[j] = unsortedList[j], unsortedList[i]
        if unsortedList[i] > pivotElement:
            unsortedList[i], unsortedList[right] = unsortedList[right], unsortedList[i]
        return i

    if startIndex is None and endIndex is None:
        startIndex, endIndex = 0, len(unsortedList)-1
    if startIndex < endIndex:
        pivotIndex = _partionate(unsortedList, startIndex, endIndex)
        quicksort(unsortedList, startIndex, pivotIndex - 1)
        quicksort(unsortedList, pivotIndex + 1, endIndex)

if __name__  == "__main__":
    l = randomUnorderedList(0, 100, 50)
    print(l)
    quicksort(l)
    print(l)

