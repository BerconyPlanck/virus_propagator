import os

from people import People
from world import World

from animate import generate_movie
from variables import space, npeople, time


def main():
    world = World(space)
    population = People(npeople, world)

    #Create worlds directory if it doesn't exist
    if not os.path.isdir('worlds'):
        os.mkdir('worlds')
    filename = 'worlds/world{0:04d}'

    i = 0
    while i < time and population.GetInfected() > 0:
        population.move_people(world)
        world.check_areas()
        population.writePeople(filename.format(i))
        i += 1

        print(i, end='\r')

    generate_movie('Movie', time)


if __name__ == '__main__':
    main()
