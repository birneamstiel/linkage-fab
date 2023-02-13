from typing import List
import math

class LinkageHub:
    """ ... """

    id = 1

    def __init__(self, position: List[int]):
        """ ... """

        self.position = position
        self.id = LinkageHub.id
        LinkageHub.id = LinkageHub.id + 1

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, LinkageHub):
            return math.isclose(self.position[0], other.position[0]) and math.isclose(self.position[1], other.position[1])
        return False

    def __hash__(self):
        return int(self.position[0] + self.position[1])

    def __str__(self):
        return '[{}, {}]'.format(self.position[0], self.position[1])

    def get_id(self) -> str:
        return chr(ord('@') + self.id)
