"""
author: Matthew Hooker (mwhooker@gmail.com)
"""
import random


class People(object):
    """Collect a list of people and expose a method to randomly select one"""

    def __init__(self, api_handle):
        """initialize with people"""
        self.people = list()
        self.api = api_handle
        self.find_people()

    def find_people(self):
        """clear current people and find others"""
        del self.people[:]
        self.people = list(self.api.get_people())

    def get_random(self):
        """get a random person"""
        if not self.people:
            self.find_people()

        assert len(self.people) > 0

        return random.choice(self.people)
