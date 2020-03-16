from celluloid import Camera
import matplotlib.pyplot as plt
import numpy as np

from parameters.user_parameters import space


def animate(i, axs, camera):
    data = np.genfromtxt('worlds/world{0:04d}'.format(i))

    axs[0].scatter(data[:, 0], data[:, 1], c=data[:, 2])

    axs[0].set_xlim(0, space)
    axs[0].set_ylim(0, space)

    data = np.genfromtxt('worlds/status'.format(i))

    axs[1].plot(data[:, 0][0: i], data[:, 1][0: i], color="b")
    axs[1].plot(data[:, 0][0: i], data[:, 2][0: i], color="y")
    axs[1].plot(data[:, 0][0: i], data[:, 3][0: i], color="g")
    axs[1].plot(data[:, 0][0: i], data[:, 4][0: i], color="g")

    camera.snap()


def generate_movie(filename, nworlds):

    fig, axs = plt.subplots(2)

    camera = Camera(fig)

    for i in range(nworlds):
        animate(i, axs, camera)

    animation = camera.animate()
    animation.save(f'{filename}.gif', writer='imagemagick')
