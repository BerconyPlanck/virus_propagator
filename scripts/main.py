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
from scripts.analysis.healthcare_system import HealthcareSystem

from scripts.plotting.animate import generate_movies
from parameters.user_parameters import space_x, space_y, npeople, time, data_path, healthcare_system_capacity


def main():

    world = World(space_x, space_y)

    population = Population(npeople)
    population.initialize_population()

    healthcare_system = HealthcareSystem(healthcare_system_capacity)

    simulation = Simulation(population, world, healthcare_system, data_path)

    time_range = range(time)
    for i in time_range:
        simulation.compute_iteration_step(i)

    print('Generating movie. This takes quite some time.')
    generate_movies('results/graphs/drafts/movie', time)


if __name__ == '__main__':
    main()
