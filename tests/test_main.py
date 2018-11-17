import time

import pytest

from fetching import Fetcher, FetchInBackground, FetchWhenNeeded


class Fetchable(object):
    """Mock object for something like a webpage scraper"""

    def __init__(self):
        self.data = []

    def fetch(self):
        self.data = [1, 2, 3]

    def whatever(self):
        return 4


class FetchableDelay(object):
    """Mock object for something like a webpage scraper,
    with delay to make async behavior obvious"""

    def __init__(self):
        self.data = []

    def fetch(self):
        time.sleep(1)
        self.data = [1, 2, 3]


def test_Fetcher_init():
    """Ensures that Fetcher init succeeds when the passed object
    has a 'fetch' method, and fails when it does not"""

    class NoFetch(object):
        pass

    Fetcher(Fetchable())

    with pytest.raises(AssertionError):
        Fetcher(NoFetch())


def test_sync_fetch():
    fetchable = Fetcher(Fetchable())
    assert isinstance(fetchable, Fetcher)
    fetchable.sync_fetch()
    assert isinstance(fetchable, Fetchable)


def test_async_fetch():
    fetchable = Fetcher(FetchableDelay())
    assert isinstance(fetchable, Fetcher)
    start_time = time.time()
    fetchable.async_fetch()

    # ensure it is truly async
    assert time.time() < start_time + 1
    assert isinstance(fetchable, Fetcher)

    time.sleep(1.5)
    assert isinstance(fetchable, FetchableDelay)


def test_callback_fetch():
    class Logger(object):
        def __init__(self):
            self.logged = []

        def __call__(self, obj):
            self.logged.append(obj.data)

    logger = Logger()

    fetchable = Fetcher(FetchableDelay())

    start_time = time.time()
    fetchable.callback_fetch(logger)

    # ensure it is truly async
    assert time.time() < start_time + 1
    assert isinstance(fetchable, Fetcher)

    time.sleep(1.5)
    assert isinstance(fetchable, FetchableDelay)

    # ensure the callback function was actually called
    assert logger.logged == [[1, 2, 3]]


def test_FetchWhenNeeded():
    fetchable = FetchWhenNeeded(Fetchable())
    assert isinstance(fetchable, FetchWhenNeeded)
    assert fetchable.data == [1, 2, 3]
    assert isinstance(fetchable, Fetchable)

    fetchable = FetchWhenNeeded(Fetchable())
    assert isinstance(fetchable, FetchWhenNeeded)
    assert fetchable.whatever() == 4
    assert isinstance(fetchable, Fetchable)

    with pytest.raises(AttributeError):
        fetchable = FetchWhenNeeded(Fetchable())
        fetchable.invalid()


def test_FetchInBackground():
    start_time = time.time()
    fetchable = FetchInBackground(FetchableDelay())

    # ensure it is truly async
    assert time.time() < start_time + 1
    assert isinstance(fetchable, FetchInBackground)

    time.sleep(1.5)
    assert isinstance(fetchable, FetchableDelay)
