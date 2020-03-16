import numpy as np
import os


class Simulation:

    def __init__(self, population, physical_world):
        self.population = population
        self.physical_world = physical_world

        self.healthy = list()
        self.infected = list()
        self.cured = list()
        self.dead = list()

        self._place_population_in_the_physical_world()

        self.filename_world = None
        self.filename_status = None

    def _place_population_in_the_physical_world(self):
        for person in self.population.people:
            person.set_position(self.physical_world.space)

    def move_person(self, person, i):
        if person in self.physical_world.physical_world[person.get_position()[0]][person.get_position()[1]]:
            self.physical_world.physical_world[person.get_position()[0]][person.get_position()[1]].remove(person)

        person.motion(i)

        self.physical_world.physical_world[person.get_position()[0]][person.get_position()[1]].append(person)

    def infect_people(self):
        for row in self.physical_world.physical_world:
            for position in row:
                if position:
                    if len(position) > 1:
                        a = np.array([person.is_infected() for person in position])

                        if a.any():
                            for person in position:
                                person.get_infected()

    def virus_outcome(self, person):
        if person.is_infected():
            person.get_cured_or_die()

    def save_data(self, i):
        self.write_populated_world(i)
        self.count_cases()
        self.write_status()

    def create_world_directory(self, filename_world='worlds/world{0:04d}', filename_status='worlds/status'):
        self.filename_world = filename_world
        self.filename_status = filename_status

        # Create worlds directory if it doesn't exist
        if not os.path.isdir('worlds'):
            os.mkdir('worlds')

    def write_populated_world(self, i):
        with open(self.filename_world.format(i), 'w') as output:
            for person in self.population.people:
                x, y = person.get_position()
                output.write(f'{x}\t{y}\t{person.get_status()}\n')

    def write_status(self):
        with open(self.filename_status, 'w') as output:
            for i in range(len(self.healthy)):
                output.write(f'{i}\t{self.healthy[i]}\t{self.infected[i]}\t{self.cured[i]}\t{self.dead[i]}\n')

    def count_cases(self):
        number_of_people_healthy = 0
        number_of_people_infected = 0
        number_of_people_cured = 0
        number_of_people_dead = 0

        for person in self.population.people:
            if person.is_infected():
                number_of_people_infected += 1
            elif person.is_cured():
                number_of_people_cured += 1
            elif person.is_dead():
                number_of_people_dead += 1
            else:
                number_of_people_healthy += 1

        self.healthy.append(number_of_people_healthy)
        self.infected.append(number_of_people_infected)
        self.cured.append(number_of_people_cured)
        self.dead.append(number_of_people_dead)

        print(f'{number_of_people_healthy} {number_of_people_infected} {number_of_people_cured} {number_of_people_dead}')