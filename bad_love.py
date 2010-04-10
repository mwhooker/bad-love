import json
import pprint
import os
from corpus import Corpus
from markov import Markov
from url import opener
import cPickle
import random

cache_path = 'cache/corpus.pkl'
if not os.path.exists(cache_path):
    corpus = Corpus()
    with open(cache_path, 'w+') as file:
        cPickle.Pickler(file).dump(corpus)
else:
    with open(cache_path, 'r') as file:
        corpus = cPickle.Unpickler(file).load()
markov = Markov(corpus.lines)

def send_love(to, msg):
    love_message = "to=%s&for1=%s&page=1&priv=0" % (to, msg)
    response = opener.open('http://lovemachine.digg.com/sendlove.php', data=love_message)
    print response.read()


love = markov.generate_markov_text()
to = random.choice(list(corpus.people))
print to
print love
#send_love(to, love)
