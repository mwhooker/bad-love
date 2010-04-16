"""
author: Matthew Hooker (mwhooker@gmail.com)

TODO:
    use average message length for markov size
"""
import cPickle
import os
import logging
from api import get_handle
from collections import Iterable

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def get_corpus():
    """get cached corpus object, or create new and cache"""
    cache_path = 'cache/corpus.pkl'
#todo check if cache is older than x
    if not os.path.exists(cache_path):
        corpus = Corpus(get_handle())
        with open(cache_path, 'w+') as cache_file:
            cPickle.Pickler(cache_file, protocol=2).dump(corpus)
    else:
        with open(cache_path, 'r') as cache_file:
            corpus = cPickle.Unpickler(cache_file).load()
    return corpus


class Corpus(Iterable):
    """build corpus froom lovemachine and act like a list"""

    FROM_EMAIL="mhooker+markov@digg.com"

    def __init__(self, api_handle):
        """build the corpus on init"""
        self.lines = []
        self.api = api_handle
        self.build_corpus()

    def _add_to_corpus(self, rows):
        """loop through rows and add each message to self.lines"""
        log.info("found message %s" % rows[0])
        for line in rows:
            if line[1] is not self.FROM_EMAIL:
                self.lines.append(line[5])

    def __iter__(self):
        return self.lines.__iter__()

    def build_corpus(self):
        """build the corpus from lovemachine"""
        del self.lines[:]
        page1 = self.api.get_page(1)

        max_pages = int(page1[0][1])
        print "max pages: %d" % max_pages
        self._add_to_corpus(page1[1:])

        for i in xrange(1, max_pages):
            page = self.api.get_page(i + 1)
            self._add_to_corpus(page[1:])
