"""
author: Matthew Hooker (mwhooker@gmail.com)


TODO:
    login automatically.
        create cookie jar and send login
"""
from corpus import get_corpus
from markov import Markov
from people import People
from api import get_handle
import random


def main():
    """set-up applcation and send love"""
    api = get_handle()
    markov = Markov(get_corpus())
    people = People(api)

    love = markov.generate_markov_text(random.randrange(15, 20))
    to_email = people.get_random()
    print to_email
    print love
    if api.send_love(to_email, love):
        return 0
    else:
        return -1

if __name__ == "__main__":
    exit(main())
