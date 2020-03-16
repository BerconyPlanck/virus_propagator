import numpy as np

from parameters.user_parameters import displacement, space, FEATURES
from parameters.virus_parameters import min_recovery_time, max_recovery_time, data_age, incubation_time,  \
    p_get_cured, p_get_infected, p_dies


class Person:
    def __init__(self, age=None):
        self.age = age
        if age:
            self.age_risk = self.find_age_risk(age)

        self.healthy = 1
        self.infected = 0
        self.cured = 0
        self.dead = 0

        self.time = 0

        self.personal_incubation_time = np.random.randint(low=incubation_time[0], high=incubation_time[1]+1)
        self.personal_recovery_time = np.random.randint(low=min_recovery_time, high=max_recovery_time+1)

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

    def is_healthy(self):
        return bool(self.healthy)

    def is_infected(self):
        return bool(self.infected)

    def is_cured(self):
        return bool(self.cured)

    def is_dead(self):
        return bool(self.dead)

    def get_infected(self):
        if self.healthy == 1:
            if np.random.random() < p_get_infected:
                self.healthy = 0
                self.infected = 1
                self.cured = 0
                self.dead = 0

                self.contact_time = self.time

    def get_cured_or_die(self):
        time_infected = (self.time - self.contact_time)
        if time_infected > self.personal_incubation_time:
            # A person can die only after an incubation time
            self.get_death()

            if time_infected > self.personal_recovery_time:
                self.get_cured()

    def get_cured(self):
        if np.random.random() < p_get_cured:
            self.healthy = 0
            self.infected = 0
            self.cured = 1
            self.dead = 1

    def die(self):
        self.healthy = 0
        self.infected = 0
        self.cured = 0
        self.dead = 1

    def get_death(self):
        if self.age:
            if np.random.random() < self.age_risk:
                self.die()
        else:
            if np.random.random() < p_dies:
                self.die()

    def get_status(self):
        if self.infected == 1:
            status = 1
        elif self.cured == 1:
            status = 2
        elif self.dead == 1:
            status = 3
        else:
            status = 0
        return status

    @staticmethod
    def find_age_risk(age):
        age_risk = None
        for key in data_age.keys():
            if int(key[0:2]) <= age <= int(key[-2:]):
                age_risk = float(data_age[key][:-1])/100
        return age_risk


class People:
    def __init__(self, npeople):
        self.people = []
        self.npeople = npeople

    def initialize_population(self):
        self._create_population()
        self._initialize_infected_people()

    def _create_population(self):
        for i in range(self.npeople):
            if FEATURES['consider_age']:
                age = np.random.randint(low=0, high=99+1)
            else:
                age = None
            self.people.append(Person(age))

    def _initialize_infected_people(self):
        self.people[0].infected = 1
        self.people[0].contact_time = 0

