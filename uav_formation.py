from combined_dict import CombinedDict


class UAVFormation(CombinedDict):
    positions = 'positions'
    colors = 'colors'

    def __init__(self):
        super().__init__([UAVFormation.positions, UAVFormation.colors])
