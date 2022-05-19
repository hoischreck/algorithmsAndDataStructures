import timeit, random

def timeFunction(function):
    def inner(*args, timeIt = True, **kwargs):
        start = timeit.default_timer()
        if timeIt:
            return function(*args, **kwargs), timeit.default_timer() - start
        else:
            return function(*args, **kwargs)
    return inner

def splitEveryNth(iterable, n):
    return [iterable[i:i+n] for i in range(0, len(iterable), n)]

def randomUnorderedSampleList(rangeObj, numeralAmount):
    return random.sample(rangeObj, numeralAmount)

def randomUnorderedList(a, b, numeralAmount):
    return [random.randint(a, b) for _ in range(numeralAmount)]