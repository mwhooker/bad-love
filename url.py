import urllib2


opener = urllib2.build_opener()
opener.addheaders = [('Referer', "http://lovemachine.digg.com/tofor.php"), ('Cookie', "PHPSESSID=41e6d16cb86440a42d6fc8628b115ba4")]
