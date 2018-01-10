import time
from fetching import Fetcher, FetchWhenNeeded, FetchInBackground

class Example(object):
    def __init__(self,i):
        self.i = i

    def fetch(self):
        self.parsed = []
        for e in range(self.i):
            self.parsed.append(e)
            time.sleep(0.5)

    def getParsed(self):
        return self.parsed

example = Example(10)
example = FetchInBackground(example)

print(example)
time.sleep(6)
print(example)

'''
example = FetchWhenNeeded(example)

print(example)
print(example.getParsed())
print(example.getParsed())
print(example)
'''
