"""
author: Matthew Hooker (mwhooker@gmail.com)
"""
from corpus import get_corpus
from markov import Markov
from people import People
from api import get_handle


def main():
    """set-up applcation and send love"""
    markov = Markov(get_corpus())
    people = People(get_handle())

    love = markov.generate_markov_text(7)
    to_email = people.get_random()
    print people.people
    print to_email
    print love
    #send_love(to, love)

if __name__ == "__main__":
    main()
