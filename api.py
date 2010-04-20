"""
author: Matthew Hooker (mwhooker@gmail.com)
"""
import urllib2
import json
import logging
import re
from BeautifulSoup import BeautifulSoup

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


class Lovemachine(object):
    """handle to the lovemachine api"""
    phpsessid = "PHPSESSID=5e3bbf2ff9a580373de59ba4e8519e0d"

    def __init__(self):
        """initialize headers"""
        self.api = urllib2.build_opener()
        self.api.addheaders = [
            ('Referer', "http://lovemachine.digg.com/tofor.php"),
            ('Cookie', self.phpsessid)]

    def get_page(self, page=1):
        """get a page of love. response will be in this format:

               [[cur_page, 'total_pages', 'total_messages'],
                [???,
                from_email,
                from_name,
                to_email,
                to_name,
                message,
                ???],
                [...]]
        """

        log.debug("reading page %s" % page)
        page_str = "page=%d" % page
        response = self.api.open('http://lovemachine.digg.com/gethistory.php',
                               data=page_str)
        soup = BeautifulSoup(response.read(),
                             convertEntities=BeautifulSoup.ALL_ENTITIES)
        return json.loads(soup.encode())

    def get_people(self):
        """get a set of people as email addresses"""
        data = "?q=%&limit=1000"
        uri = 'http://lovemachine.digg.com/getemails.php%s' % data
        log.debug("finding people at %s" % uri)
        response = self.api.open(uri)
        mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
        emails = mailsrch.findall(response.read())
        return set(emails)

    def send_love(self, to_email, msg):
        """send love"""
        love_message = "to=%s&for1=%s&page=1&priv=0" % (to_email, msg)
        response = self.api.open('http://lovemachine.digg.com/sendlove.php',
                                 data=love_message)
        return json.loads(response.read()) == u'ok'


def get_handle():
    """get lovemachine handle"""
    return Lovemachine()
