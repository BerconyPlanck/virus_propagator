import numpy as np

from people import People
from world import World

from animate import generate_movie
from variables import space, npeople, time

class Simulation:

    def __init__(self, population, physical_world):
        self.population = population
        self.physical_world = physical_world

        self._place_population_in_the_physical_world()

    def _place_population_in_the_physical_world(self):
        for person in self.population.people:
            person.set_position(space)

    def move_people(self):
        for person in self.population.people:

            if person in self.physical_world.x[person.get_position()[0]][person.get_position()[1]]:
                self.physical_world.x[person.get_position()[0]][person.get_position()[1]].remove(person)

            person.motion()

            self.physical_world.x[person.get_position()[0]][person.get_position()[1]].append(person)



def main():

    world = World(space)
    population = People(npeople, world)

    simulation = Simulation(population, world)
    filename = 'worlds/world{0:04d}'

    for i in range(10):
        simulation.move_people()
        population.writePeople(filename.format(i))


    generate_movie('Movie', 10)


if __name__ == '__main__':
    main()
