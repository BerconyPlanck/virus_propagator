import numpy as np
import os


class Simulation:

    def __init__(self, population, physical_world, data_path):
        self.population = population
        self.physical_world = physical_world

        self.healthy = list()
        self.infected = list()
        self.cured = list()
        self.dead = list()

        self.deaths_female = list()
        self.deaths_male = list()

        self.data_path = data_path

        self._place_population_in_the_physical_world()

        self.filename_world = None
        self.filename_status = None

    def _place_population_in_the_physical_world(self):
        for person in self.population.people:
            person.set_position(self.physical_world.space_x, self.physical_world.space_y)

    def move_person(self, person, i):
        """

        Parameters
        ----------
        person: Person
        i: int
        """
        if person in self.physical_world.physical_world[person.get_position()[0]][person.get_position()[1]]:
            self.physical_world.physical_world[person.get_position()[0]][person.get_position()[1]].remove(person)

        person.motion(i)

        self.physical_world.physical_world[person.get_position()[0]][person.get_position()[1]].append(person)

    def infect_people(self):
        """Infect people based on their position."""
        for row in self.physical_world.physical_world:
            for position in row:
                if position:
                    if len(position) > 1:
                        a = np.array([person.is_infected() for person in position])

                        if a.any():
                            for person in position:
                                person.get_infected()

    def save_data(self, i):
        """

        Parameters
        ----------
        i: int

        """
        self.write_populated_world(i)
        self.count_cases()
        self.write_status()

    def create_world_directory(self, filename_world='/world{0:04d}', filename_status='/status'):
        self.filename_world = self.data_path + filename_world
        self.filename_status = self.data_path + filename_status

        # Create worlds directory if it doesn't exist
        if not os.path.isdir(self.data_path):
            os.mkdir(self.data_path)

    def write_populated_world(self, i):
        """
        Parameters
        ----------
        i
        """
        with open(self.filename_world.format(i), 'w') as output:
            for person in self.population.people:
                x, y = person.get_position()
                status = person.get_status()
                gender = person.get_gender()
                age = person.get_age()

                output.write(f'{x}\t{y}\t{status}\t{gender}\t{age}\n')

    def write_status(self):
        with open(self.filename_status, 'w') as output:
            for i in range(len(self.healthy)):
                output.write(f'{i}\t{self.healthy[i]}\t{self.infected[i]}\t{self.cured[i]}\t{self.dead[i]}\t{self.deaths_female[i]}\t{self.deaths_male[i]}\n')

    def count_cases(self):
        number_of_people_healthy = 0
        number_of_people_infected = 0
        number_of_people_cured = 0
        number_of_people_dead = 0

        number_of_dead_female = 0
        number_of_dead_male = 0

        for person in self.population.people:
            if person.is_infected():
                number_of_people_infected += 1
            elif person.is_recovered():
                number_of_people_cured += 1
            elif person.is_dead():
                number_of_people_dead += 1
                if person.get_gender() == 'female':
                    number_of_dead_female += 1
                else:
                    number_of_dead_male += 1
            else:
                number_of_people_healthy += 1

        self.healthy.append(number_of_people_healthy)
        self.infected.append(number_of_people_infected)
        self.cured.append(number_of_people_cured)
        self.dead.append(number_of_people_dead)

        self.deaths_female.append(number_of_dead_female)
        self.deaths_male.append(number_of_dead_male)

        print(f'{number_of_people_healthy} {number_of_people_infected} {number_of_people_cured} {number_of_people_dead}')