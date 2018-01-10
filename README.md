# fetching

**Fetching** is a small library that enables easy [lazy initialization](https://en.wikipedia.org/wiki/Lazy_initialization).

To use Fetching, define your class with an `__init__` function that stores all necessary seed data, and a `fetch` function that does the computationally expensive initializations. Don't call `fetch` from `__init__`. If you designed the class correctly, the following sequence should result in a fully initialized class instance:

```python
someClass = SomeClass(args) # can have args
someClass.fetch()           # can't have args
```

An example:

```python
# not compatible with Fetching
class Example(object):
    def __init__(self,i):
        self.parsed = []
        for e in range(i):
            self.parsed.append(e)
            time.sleep(0.5)

    def getParsed(self):
        return self.parsed
```

```python
# compatible with Fetching
class Example(object):
    def __init__(self,i):
        self.i = i

    def fetch(self):
        self.parsed = []
        for e in range(self.i):
            self.parsed.append(e)
            time.sleep(0.5)       # the slow process is moved to fetch()

    def getParsed(self):
        return self.parsed
```

A more practical example:

```python
# not compatible with Fetching
class Webpage(object):
    def __init__(self,url):
        self.page = requests.get(url).text

    def pageText(self):
        return self.page
```

```python
# compatible with Fetching
class Webpage(object):
    def __init__(self,url):
        self.url = url
    
    def fetch(self):
        self.page = requests.get(url).text

    def pageText(self):
        return self.page
```

Once your class is formatted correctly, use simple wrapper classes to give the desired behavior:

```python
from fetching import FetchWhenNeeded

example = Example(5)
example = FetchWhenNeeded(5)

# example.parsed doesn't exist yet

print(example.getParsed()) # runs Example.fetch and returns .getParsed()

```

```python
from fetching import FetchInBackground

example = Example(5)
example = FetchInBackground(5)

# Example.fetch is being run in a separate thread

print(example.getParsed()) # runs Example.fetch and returns .getParsed()

```





