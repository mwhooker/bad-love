import json
import pprint
from url import opener


class Corpus(object):

    def __init__(self):
        self.people = set()
        self.lines = []
        self._build_corpus()

    def _build_corpus(self):
        page1 = self._get_page(1)

        max_pages = int(page1[0][1])
        print "max pages: %d" % max_pages
        self._add_to_corpus(page1[1:])

        for i in xrange(1, max_pages):
            page = self._get_page(i+1)
            self._add_to_corpus(page[1:])

    def _get_page(self, page=1):
        print "reading page %s" % page
        page_str = "page=%d" % page
        response = opener.open('http://lovemachine.digg.com/gethistory.php', data=page_str)
        return json.loads(response.read())

    def _add_to_corpus(self,rows):
        for line in rows:
            self.people.add(line[3])
            self.lines.append(line[5])


