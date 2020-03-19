# -*- coding: utf-8 -*-
#
# This file is part of the virus propagator simulation.
# Copyright (C) 2020 Daniel Prelipcean.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Animmation"""

from celluloid import Camera
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from parameters.user_parameters import analysises



def animate_virus_outbreak(i, fig, camera):
    data = np.genfromtxt('worlds/world{0:04d}'.format(i))

    plt.scatter(data[:, 0], data[:, 1], c=data[:, 2])

    plt.xlabel('Space x coordinate [au]')
    plt.ylabel('Space y coordinate [au]')

    # fig.set_xlim(0, space_x)
    # fig.set_ylim(0, space_y)

    camera.snap()


def animate_population_status(i, fig, camera):
    plotter = Plotter()

    data = np.genfromtxt('worlds/status'.format(i))
    data_time = data[:, 0]

    data_healthy = data[:, 1]
    data_infected = data[:, 2]
    data_recovered = data[:, 3]
    data_dead = data[:, 4]

    data_sets = [data_healthy, data_infected, data_recovered, data_dead]

    legend = ['Healthy', 'Infected', 'Cured', 'Dead']
    labels = {'xlabel': 'Time [a.u.]', 'ylabel': 'People'}

    plotter.plot_data_sets(fig, i, data_time, data_sets, legend, labels)

    camera.snap()


def animate_dead_people_female_male(i, fig, camera):
    plotter = Plotter()

    data = np.genfromtxt('worlds/status'.format(i))
    data_time = data[:, 0]

    data_female = data[:, 5]
    data_male = data[:, 6]

    legend = ['Female', 'Male']
    labels = {'xlabel': 'Time [a.u.]', 'ylabel': 'Dead People'}
    data_sets = [data_female, data_male]

    plotter.plot_data_sets(fig, i, data_time, data_sets, legend, labels)
    camera.snap()


class Plotter:

    colors = sns.color_palette(palette='colorblind')

    def __init__(self):
        pass

    def plot_data_sets(self, plot_ax, index, data_time, data_sets, legend, labels):
        for data_set_index in range(len(data_sets)):
            data = data_sets[data_set_index]
            plt.plot(data_time[0: index], data[0: index], color=self.colors[data_set_index])

        plt.legend(legend)

        plt.xlabel(labels['xlabel'])
        plt.ylabel(labels['ylabel'])


def define_which_graphs_to_plot():
    if analysises['animate_virus_outbreak']:
        analysises['animate_virus_outbreak'] = animate_virus_outbreak
    else:
        analysises.pop('animate_virus_outbreak', None)

    if analysises['population_status']:
        analysises['population_status'] = animate_population_status
    else:
        analysises.pop('population_status', None)

    if analysises['animate_dead_people_female_male']:
        analysises['animate_dead_people_female_male'] = animate_dead_people_female_male
    else:
        analysises.pop('animate_dead_people_female_male', None)


def generate_movies(filename, nworlds):
    define_which_graphs_to_plot()

    for key, value in analysises.items():
        fig = plt.figure()

        camera = Camera(fig)
        for i in range(nworlds):
            if i % 4 == 0:
                value(i, fig, camera)

        animation = camera.animate(interval=20)
        animation.save(f'{filename}_{key}.gif', writer='imagemagick')
        fig.clf()
