import numpy as np
from variables import displacement, min_recovery_time, min_recovery_time, space, lifetime


class Person:
    def __init__(self, space):
        self.infected = 0
        self.cured = 0

        self.time = 0
        self.personal_recovery_time = np.random.randint(low=min_recovery_time, high=min_recovery_time+1)

        self.set_position(space)

    def set_position(self, space):
        self.x = np.random.randint(space)
        self.y = np.random.randint(space)

    def get_position(self):
        return self.x, self.y

        # #If the person is infected the area becomes infected or it's counter start over
        # #The living time of the infected increases
        # if self.infected != 0:
        #     world.x[self.x,self.y] = 1
        #     self.infected_time += 1

    def motion(self, i):
        dx, dy = int((np.random.randint(displacement+1))-(displacement/2)), \
                 int((np.random.randint(displacement+1))-(displacement/2))

        self.x += dx
        self.y += dy

        if self.x >= space or self.x < 0:
            self.x = space - np.abs(self.x)

        if self.y >= space or self.y < 0:
            self.y = space - np.abs(self.y)

        self.time = i

    def is_infected(self):
        return bool(self.infected)

    def get_infected(self):
        if self.cured == 0:
            self.infected = 1
            self.contact_time = self.time

    def is_cured(self):
        return bool(self.cured)

    def get_cured(self):
        if (self.time - self.contact_time) > self.personal_recovery_time:
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
    def __init__(self, npeople):
        self.people = []
        self.npeople = npeople

    def initialize_population(self):
        self._create_population()
        self._initialize_infected_people()

    def _create_population(self):
        for i in range(self.npeople):
            self.people.append(Person(space))

    def _initialize_infected_people(self):
        self.people[0].infected = 1
        self.people[0].contact_time = 0

