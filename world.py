import numpy as np

class World:
    #Infected area represented by 1, normal area represented by 0
    def __init__(self, space):
        # self.x = np.zeros((space, space)).astype('int')

        self.x = [[list() for i in range(space)] for j in range(space)]

    def check_areas(self):
        notzeros = np.where(self.x != 0)
        self.x[notzeros] += 1
        uninfected = np.where(self.x > 3)
        self.x[uninfected] = 0

    def write_world(self, filename):
        output = open(filename, 'w')
        for i in range(len(self.x)):
            for j in range(len(self.x)):
                output.write('{0:d}\t{1:d}\t{2:d}\n'.format(i, j, self.x[i, j]))
        output.close()
