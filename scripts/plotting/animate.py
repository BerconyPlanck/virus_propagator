# -*- coding: utf-8 -*-
#
# This file is part of the virus propagator simulation.
# Copyright (C) 2020 Daniel Prelipcean.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Animation and plotting scripts."""

from celluloid import Camera
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from parameters.user_parameters import analysises, data_path


class Plotter:

    colors = sns.color_palette(palette='colorblind')

    def __init__(self):
        pass

    def plot_data_sets(self, index, data_time, data_sets, legend, labels):
        for data_set_index in range(len(data_sets)):
            data = data_sets[data_set_index]
            plt.plot(data_time[0: index], data[0: index], color=self.colors[data_set_index])

        plt.legend(legend)

        plt.xlabel(labels['xlabel'])
        plt.ylabel(labels['ylabel'])


def define_which_graphs_to_plot():
    if analysises['virus_outbreak']:
        analysises['virus_outbreak'] = animate_virus_outbreak
    else:
        analysises.pop('virus_outbreak', None)

    if analysises['population_status']:
        analysises['population_status'] = animate_population_status
    else:
        analysises.pop('population_status', None)

    if analysises['dead_people_female_male']:
        analysises['dead_people_female_male'] = animate_dead_people_female_male
    else:
        analysises.pop('dead_people_female_male', None)

    if analysises['dead_age_distribution']:
        analysises['dead_age_distribution'] = animate_dead_age_distribution
    else:
        analysises.pop('dead_age_distribution', None)


def animate_virus_outbreak(i, camera):
    data = np.genfromtxt(f'{data_path}/world{i:04d}')

    plt.scatter(data[:, 0], data[:, 1], c=data[:, 2])

    plt.xlabel('Space x coordinate [au]')
    plt.ylabel('Space y coordinate [au]')

    camera.snap()


def animate_dead_age_distribution(i, camera):
    data = np.genfromtxt(f'{data_path}/world{i:04d}')

    data_age = data[:, 4]
    data_status = data[:, 2]

    data_plot = {10: 0, 20: 0, 30: 0, 40: 0, 50: 0, 60: 0, 70: 0, 80: 0, 90: 0, 100: 0}

    for i in range(len(data_age)):
        if data_status[i] == 3:
            for key in data_plot.keys():
                if key - 10 <= data_age[i] < key:
                    data_plot[key] += 1

    plt.bar(list(data_plot.keys()), list(data_plot.values()))

    # plt.xlabel('Space x coordinate [au]')
    # plt.ylabel('Space y coordinate [au]')

    camera.snap()


def animate_population_status(i, camera):
    plotter = Plotter()
    data = np.genfromtxt(f'{data_path}/status')

    data_time = data[:, 0]

    data_healthy = data[:, 1]
    data_infected = data[:, 2]
    data_recovered = data[:, 3]
    data_dead = data[:, 4]

    data_sets = [data_healthy, data_infected, data_recovered, data_dead]

    legend = ['Healthy/Uninfected', 'Infected', 'Recovered', 'Dead']
    labels = {'xlabel': 'Time [a.u.]', 'ylabel': 'People'}

    plotter.plot_data_sets(i, data_time, data_sets, legend, labels)

    camera.snap()


def animate_dead_people_female_male(i, camera):
    plotter = Plotter()

    data = np.genfromtxt(f'{data_path}/status')

    data_time = data[:, 0]

    data_female = data[:, 5]
    data_male = data[:, 6]

    legend = ['Female', 'Male']
    labels = {'xlabel': 'Time [a.u.]', 'ylabel': 'Dead People'}
    data_sets = [data_female, data_male]

    plotter.plot_data_sets(i, data_time, data_sets, legend, labels)
    camera.snap()


def generate_movies(filename, nworlds):
    define_which_graphs_to_plot()

    for key, value in analysises.items():
        fig = plt.figure()

        camera = Camera(fig)
        for i in range(nworlds):
            # Avoid running into memory/cache problems by plotting only a quarter of the plots over time
            if i % 4 == 0:
                value(i, camera)

        animation = camera.animate(interval=20)
        animation.save(f'{filename}_{key}.gif', writer='imagemagick')
        fig.clf()

        print(f'Generated movie for {key}')
