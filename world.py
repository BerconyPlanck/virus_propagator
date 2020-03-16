
class World:

    def __init__(self, space):
        self.space = space
        self.physical_world = [[list() for i in range(space)] for j in range(space)]
