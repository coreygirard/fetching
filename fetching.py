import threading


class Fetcher(object):
    def __init__(self, c):
        assert hasattr(c, 'fetch')
        self.c = c

        # TODO: temporarily unmount the 'fetch' method to this class

    def sync_fetch(self):
        """Executes fetch function, then makes itself basically become
        the fetched object"""

        self.c.fetch()
        self.__class__ = self.c.__class__
        self.__dict__ = self.c.__dict__

    def async_fetch(self):
        """Same as sync_fetch, but asynchronous"""

        self.thread = threading.Thread(target=self.sync_fetch)
        self.thread.daemon = False
        self.thread.start()

    def _callback_fetch_helper(self, f):
        """Synchronous fetch and callback. Only used by callback_fetch"""

        self.sync_fetch()
        f(self)

    def callback_fetch(self, f):
        """Perform async fetch and then trigger a callback function"""

        self.thread = threading.Thread(target=self._callback_fetch_helper,
                                       args=(f,))
        self.thread.daemon = False
        self.thread.start()


class FetchWhenNeeded(Fetcher):
    """Executes sync fetch as soon as attr access is attempted"""

    def __getattr__(self, name):
        self.sync_fetch()
        return getattr(self, name)

class FetchInBackground(Fetcher):
    """Upon initialization, immediately begins async fetch"""

    def __init__(self, c):
        super(FetchInBackground, self).__init__(c)
        self.async_fetch()
