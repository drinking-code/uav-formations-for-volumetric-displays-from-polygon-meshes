from combined_dicts import CombinedDicts


class UAVFormation(CombinedDicts):
    positions = 'positions'
    colors = 'colors'

    def __init__(self):
        super().__init__([UAVFormation.positions, UAVFormation.colors])
