# -*- coding: utf-8 -*-
#
# This file is part of the virus propagator simulation.
# Copyright (C) 2020 Daniel Prelipcean.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Main running script."""

from people import People
from world import World
from simulation import Simulation

from animate import generate_movie
from variables import space, npeople, time


def main():

    world = World(space)

    population = People(npeople)
    population.initialize_population()

    simulation = Simulation(population, world)

    simulation.create_world_directory()

    time_range = range(time)
    for i in time_range:
        print(f'Computing time step: {i}')
        for person in simulation.population.people:
            simulation.recover_people(person)
            simulation.move_person(person, i)

        simulation.infect_people()

        simulation.save_data(i)

    print('Generating movie. This takes quite some time.')
    generate_movie('Movie', time)


if __name__ == '__main__':
    main()
