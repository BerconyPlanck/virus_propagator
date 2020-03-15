import os
import numpy as np

from people import People
from world import World

from animate import generate_movie
from variables import space, npeople, time, p_get_infected, p_get_cured


class Simulation:

    def __init__(self, population, physical_world):
        self.population = population
        self.physical_world = physical_world

        self._place_population_in_the_physical_world()

        self.healthy = list()
        self.infected = list()
        self.cured = list()

    def _place_population_in_the_physical_world(self):
        for person in self.population.people:
            person.set_position(space)

    def move_people(self):
        for person in self.population.people:

            if person in self.physical_world.x[person.get_position()[0]][person.get_position()[1]]:
                self.physical_world.x[person.get_position()[0]][person.get_position()[1]].remove(person)

            person.motion()

            self.physical_world.x[person.get_position()[0]][person.get_position()[1]].append(person)

    def infect_people(self):
        for row in self.physical_world.x:
            for position in row:
                if position:
                    if len(position) > 1:
                        a = np.array([person.is_infected() for person in position])

                        if a.any():
                            for person in position:
                                if np.random.random() < p_get_infected:
                                    person.get_infected()

    def recover_people(self):
        for person in self.population.people:
            if person.is_infected():
                if np.random.random() < p_get_cured:
                    person.get_cured()


    def write_populated_world(self, filename):
        with open(filename, 'w') as output:
            for person in self.population.people:
                x, y = person.get_position()
                output.write('{0:d}\t{1:d}\t{2:d}\n'.format(x, y, person.get_status()))

    def write_status(self, filename):
        with open(filename, 'w') as output:
            for i in range(len(self.healthy)):
                output.write('{0:d}\t{1:d}\t{2:d}\t{3:d}\n'.format(i, self.healthy[i], self.infected[i], self.cured[i]))

    def count_cases(self):
        number_of_people_healthy = 0
        number_of_people_infected = 0
        number_of_people_cured = 0

        for person in self.population.people:
            if person.is_infected():
                number_of_people_infected += 1
            elif person.is_cured():
                number_of_people_cured += 1
            else:
                number_of_people_healthy += 1

        self.healthy.append(number_of_people_healthy)
        self.infected.append(number_of_people_infected)
        self.cured.append(number_of_people_cured)


def main():

    world = World(space)
    population = People(npeople, world)

    simulation = Simulation(population, world)

    filename_world = 'worlds/world{0:04d}'
    filename_status = 'worlds/status'
    #Create worlds directory if it doesn't exist
    if not os.path.isdir('worlds'):
        os.mkdir('worlds')

    time_range = range(time)
    for i in time_range:
        print(f'Computing time step: {i}')
        simulation.move_people()

        simulation.infect_people()
        simulation.recover_people()

        simulation.write_populated_world(filename_world.format(i))

        simulation.count_cases()

        simulation.write_status(filename_status)

    print('Generating movie. This takes quite some time.')
    generate_movie('Movie', time)


if __name__ == '__main__':
    main()
