# -*- coding: utf-8 -*-
#
# This file is part of the virus propagator simulation.
# Copyright (C) 2020 Daniel Prelipcean.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Main running script."""

from scripts.people import People
from scripts.world import World
from scripts.simulation import Simulation

from scripts.animate import generate_movie
from parameters.user_parameters import space_x, space_y, npeople, time


def main():

    world = World(space_x, space_y)

    population = People(npeople)
    population.initialize_population()

    simulation = Simulation(population, world)

    simulation.create_world_directory()

    time_range = range(time)
    for i in time_range:
        print(f'Computing time step: {i}')
        simulation.infect_people()

        for person in simulation.population.people:
            simulation.virus_outcome(person)
            simulation.move_person(person, i)

        simulation.save_data(i)

    print('Generating movie. This takes quite some time.')
    generate_movie('Movie', time)


if __name__ == '__main__':
    main()
