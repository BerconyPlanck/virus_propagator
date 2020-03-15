import numpy as np

from variables import displacement, p_get_infected, space, lifetime


class Person:
    def __init__(self, space):
        self.infected = 0
        self.infected_time = 0

        self.set_position(space)

    def set_position(self, space):
        self.x = np.random.randint(space)
        self.y = np.random.randint(space)

    def get_position(self):
        return self.x, self.y

    def move(self, world):
        self.motion()

        #If the area is infected the person becomes infected
        if world.x[self.x, self.y] != 0:
            if np.random.random() < p_get_infected:
                if self.infected == 0:
                    self.infected = 1

        #If the person is infected the area becomes infected or it's counter start over
        #The living time of the infected increases
        if self.infected != 0:
            world.x[self.x,self.y] = 1
            self.infected_time += 1

    def motion(self):
        dx, dy = int((np.random.randint(displacement+1))-(displacement/2)), \
                 int((np.random.randint(displacement+1))-(displacement/2))

        self.x += dx
        self.y += dy

        if self.x >= space or self.x < 0:
            self.x = space - np.abs(self.x)

        if self.y >= space or self.y < 0:
            self.y = space - np.abs(self.y)


class People:
    def __init__(self, npeople, world):
        self.people = []

        for i in range(npeople):
            self.people.append(Person(space))

        self.people[0].infected = 1
        self.people[0].infected_time += 1

        x, y = self.GetCoordinate(i)
        # world.x[x, y] = 1

    def move_people(self, world):
        for i in self.people:
            i.move(world)
        self.people = [i for i in self.people if i.infected_time < lifetime]

    def GetInfected(self):
        return len([i for i in self.people if i.infected > 0])

    def GetCoordinate(self, i):
        return self.people[i].x, self.people[i].y

    def writePeople(self, filename):
        output = open(filename, 'w')
        for i in range(len(self.people)):
            x, y = self.GetCoordinate(i)
            output.write('{0:d}\t{1:d}\t{2:d}\n'.format(x, y, self.people[i].infected))
        output.close()
