from DataStructures.BTree import BTree, createRandomBTree

tree, time = createRandomBTree(range(1, 101), 100, timeIt = True)
print(tree)
print(time)

#print(BTree([1, 2, 3, 3]))

def test(argument: int) -> None:
	print(argument)

test("hello world")