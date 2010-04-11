"""
author: Matthew Hooker (mwhooker@gmail.com)
"""
import urllib2
import json
import logging
import re

log = logging.getLogger(__name__)


class Lovemachine(object):
    """handle to the lovemachine api"""
    phpsessid = "PHPSESSID=4f1506664279b6a6de2e723b90e5c9ee"

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

        log.info("reading page %s" % page)
        page_str = "page=%d" % page
        response = self.api.open('http://lovemachine.digg.com/gethistory.php',
                               data=page_str)
        return json.loads(response.read())

    def get_people(self):
        """get a set of people as email addresses"""
        request = "q=%&limit=1000"
        response = self.api.open('http://lovemachine.digg.com/getemails.php',
                                data=request)
        mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
        return set(mailsrch.findall(response.read()))

    def send_love(self, to_email, msg):
        """send love"""
        love_message = "to=%s&for1=%s&page=1&priv=0" % (to_email, msg)
        response = self.api.open('http://lovemachine.digg.com/sendlove.php',
                                 data=love_message)
        return json.loads(response.read()) == u'ok'


def get_handle():
    """get lovemachine handle"""
    return Lovemachine()
