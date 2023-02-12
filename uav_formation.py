import math
import random
import sys
from functools import reduce

from combined_dict import CombinedDict
from utils import is_iterable


class UAVFormation(CombinedDict):
    positions = 'positions'
    colors = 'colors'

    def __init__(self):
        super().__init__([UAVFormation.positions, UAVFormation.colors])

    def __setitem__(self, key, value, category=None):
        result = super().__setitem__(key, value, category)
        if category == UAVFormation.positions:
            if not is_iterable(value) or len(value) != 3:
                raise Exception(f'"value" for category `{UAVFormation.positions}` must be iterable of length 3.')
            iterable_strings = map(lambda a: str(a), value)
            sys.stdout.write(' '.join(iterable_strings) + '\n')
            sys.stdout.flush()
        return result

    def add_position(self, point):
        # todo: fix: comes from "safe_placement_on_corners" function
        if any(map(lambda coordinate: math.isnan(coordinate), list(point))):
            return False
        # todo
        for position in self.data[UAVFormation.positions].values():
            if list(position) == list(point):
                return False

        key = random.randint(0, 2 ** 32)
        self[key][UAVFormation.positions] = point
        return key
