import numpy as np

from variables import displacement, p_get_infected, space, lifetime


class Person:
    def __init__(self, space):
        self.infected = 0
        self.cured = 0

        self.infected_time = 0

        self.set_position(space)

    def set_position(self, space):
        self.x = np.random.randint(space)
        self.y = np.random.randint(space)

    def get_position(self):
        return self.x, self.y

    def move(self, world):
        self.motion()

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

    def is_infected(self):
        return bool(self.infected)

    def get_infected(self):
        if self.cured == 0:
            self.infected = 1

    def is_cured(self):
        return bool(self.cured)

    def get_cured(self):
        self.infected = 0
        self.cured = 1

    def get_status(self):
        if self.infected == 1:
            status = 1
        elif self.cured == 1:
            status = 2
        else:
            status = 0
        return status


class People:
    def __init__(self, npeople, world):
        self.people = []

        for i in range(npeople):
            self.people.append(Person(space))

        self.people[0].infected = 1
        self.people[0].infected_time += 1

    def move_people(self, world):
        for i in self.people:
            i.move(world)
        self.people = [i for i in self.people if i.infected_time < lifetime]

    def GetInfected(self):
        return len([i for i in self.people if i.infected > 0])
