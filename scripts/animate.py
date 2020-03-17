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

from parameters.user_parameters import space_x, space_y


def animate(i, axs, camera):
    data = np.genfromtxt('worlds/world{0:04d}'.format(i))

    axs[0].scatter(data[:, 0], data[:, 1], c=data[:, 2])

    axs[0].set_xlim(0, space_x)
    axs[0].set_ylim(0, space_y)

    data = np.genfromtxt('worlds/status'.format(i))

    axs[1].plot(data[:, 0][0: i], data[:, 1][0: i], color="b")
    axs[1].plot(data[:, 0][0: i], data[:, 2][0: i], color="y")
    axs[1].plot(data[:, 0][0: i], data[:, 3][0: i], color="g")
    axs[1].plot(data[:, 0][0: i], data[:, 4][0: i], color="c")

    axs[1].legend(['Healthy', 'Infected', 'Cured', 'Dead'])

    axs[2].plot(data[:, 0][0: i], data[:, 5][0: i], color="b")
    axs[2].plot(data[:, 0][0: i], data[:, 6][0: i], color="y")
    axs[2].legend(['Female', 'Male'])

    camera.snap()


def generate_movie(filename, nworlds):

    fig, axs = plt.subplots(3)

    camera = Camera(fig)

    for i in range(nworlds):
        if i % 4 == 0:
            animate(i, axs, camera)

    animation = camera.animate(interval=20)
    animation.save(f'{filename}.gif', writer='imagemagick')
