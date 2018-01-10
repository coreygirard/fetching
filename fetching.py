import copy
import threading

class Fetcher(object):
    def __init__(self,c):
        assert(hasattr(c,'fetch'))
        self.c = c

        # TODO: temporarily unmount the 'fetch' method to this class

    def syncFetch(self):
        self.c.fetch()
        self.__class__ = self.c.__class__
        self.__dict__ = self.c.__dict__

    def asyncFetch(self):
        self.thread = threading.Thread(target=self.syncFetch)
        self.thread.daemon = False
        self.thread.start()

    def _callbackFetchHelper(self,f):
        self.syncFetch()
        f(self)

    def callbackFetch(self,f):
        self.thread = threading.Thread(target=self._callbackFetchHelper,
                                       args=(f,))
        self.thread.daemon = False
        self.thread.start()


class FetchWhenNeeded(Fetcher):
    def __getattr__(self,name):
        self.syncFetch()
        return getattr(self,name)

class FetchInBackground(Fetcher):
    def __init__(self,c):
        super(FetchInBackground, self).__init__(c)
        self.asyncFetch()
