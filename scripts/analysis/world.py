
class World:

    def __init__(self, space_x, space_y):
        self.space_x = space_x
        self.space_y = space_y

        self.physical_world = [[list() for i in range(space_y)] for j in range(space_x)]
