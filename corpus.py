"""
author: Matthew Hooker (mwhooker@gmail.com)

TODO:
    use average message length for markov size
"""
import cPickle
import os
import logging
from api import get_handle
#from collections import Iterable

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def cache_expired(path):
    from time import time
#TTL is 24 hours
    TTL = 24 * 60 * 60 
    return (time() - os.path.getmtime(path)) > TTL

def get_corpus():
    """get cached corpus object, or create new and cache"""
    cache_path = os.path.join(os.path.dirname(__file__), 'cache', 'corpus.pkl')
    if not os.path.exists(cache_path) or cache_expired(cache_path):
        corpus = Corpus(get_handle())
        cache_file = open(cache_path, 'w+')
        cPickle.Pickler(cache_file, protocol=2).dump(corpus)
    else:
        cache_file =  open(cache_path, 'r')
        corpus = cPickle.Unpickler(cache_file).load()
    cache_file.close()
    return corpus


class Corpus(object):
    """build corpus from lovemachine and act like a list"""

    BLACKLIST_EMAILS=["mhooker+markov@digg.com",
                      "mhooker@digg.com"]

    CENSOR_WORDS = ['slut', 'bitch']

    def __init__(self, api_handle):
        """build the corpus on init"""
        self.lines = []
        self.api = api_handle
        self.build_corpus()

    def _censor(self, string):
        for cuss in self.CENSOR_WORDS:
            string.replace(cuss, '')
        return string

    def _add_to_corpus(self, rows):
        """loop through rows and add each message to self.lines"""
        log.debug("found message %s" % rows[0])
        for line in rows:
            if line[1] not in self.BLACKLIST_EMAILS:
                self.lines.append(self._censor(line[5]))

    def __iter__(self):
        return self.lines.__iter__()

    def build_corpus(self):
        """build the corpus from lovemachine"""
        del self.lines[:]
        page1 = self.api.get_page(1)

        max_pages = int(page1[0][1])
        log.debug("total pages: %d" % max_pages)
        self._add_to_corpus(page1[1:])

        for i in xrange(1, max_pages):
            page = self.api.get_page(i + 1)
            self._add_to_corpus(page[1:])
