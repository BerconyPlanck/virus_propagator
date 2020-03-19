# -*- coding: utf-8 -*-
#
# This file is part of the virus propagator simulation.
# Copyright (C) 2020 Daniel Prelipcean.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Main running script."""

from scripts.analysis.population import Population
from scripts.analysis.world import World
from scripts.analysis.simulation import Simulation

from scripts.plotting.animate import generate_movies
from parameters.user_parameters import space_x, space_y, npeople, time, data_path


def main():

    world = World(space_x, space_y)

    population = Population(npeople)
    population.initialize_population()

    simulation = Simulation(population, world, data_path)

    simulation.create_world_directory()

    time_range = range(time)
    for i in time_range:
        print(f'Computing time step: {i}')
        simulation.infect_people()

        for person in simulation.population.people:
            person.virus_outcome()
            simulation.move_person(person, i)

        simulation.save_data(i)

    print('Generating movie. This takes quite some time.')
    generate_movies('results/graphs/drafts/movie', time)


if __name__ == '__main__':
    main()
