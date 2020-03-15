from celluloid import Camera
import matplotlib.pyplot as plt
import numpy as np

from variables import space


def animate(i, camera):
    data = np.genfromtxt('worlds/world{0:04d}'.format(i))

    plt.scatter(data[:, 0], data[:, 1], c=data[:, 2])

    plt.xlim(0, space)
    plt.ylim(0, space)

    camera.snap()


def generate_movie(filename, nworlds):

    fig = plt.figure()

    camera = Camera(fig)

    for i in range(nworlds):
        animate(i, camera)

    animation = camera.animate()
    animation.save(f'{filename}.gif', writer='imagemagick')
