import math
import random
import sys

from utils.combined_dict import CombinedDict
from utils import is_iterable


class UAVFormation(CombinedDict):
    positions = 'positions'
    colors = 'colors'

    corner = 'c'
    edge = 'e'
    face = 'f'

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

    def add_position(self, point, group):
        # todo: fix: comes from "safe_placement_on_corners" function
        if any(map(lambda coordinate: math.isnan(coordinate), list(point))):
            return False
        # todo
        for position in self.data[UAVFormation.positions].values():
            if list(position) == list(point):
                return False

        key = random.randint(0, 2 ** 32)
        super().__setitem__(key, point, UAVFormation.positions)
        if not is_iterable(point) or len(point) != 3:
            raise Exception(f'"value" for category `{UAVFormation.positions}` must be iterable of length 3.')
        iterable_strings = map(lambda a: str(a), point)
        sys.stdout.write(f'{group} {" ".join(iterable_strings)}\n')
        sys.stdout.flush()
        return key
