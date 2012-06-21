"""
author: Matthew Hooker (mwhooker@gmail.com)
"""
import random


class People(object):
    """Collect a list of people and expose a method to randomly select one"""

    def __init__(self, api_handle):
        """initialize with people"""
        self.api = api_handle
        self.people = self.api.get_people()

    def get_random(self):
        """get a random person"""
        
        assert len(self.people) > 0

        return random.choice(self.people)
