import os


from people import People
from world import World
from simulation import Simulation

from animate import generate_movie
from variables import space, npeople, time

def main():

    world = World(space)
    population = People(npeople, world)

    simulation = Simulation(population, world)

    filename_world = 'worlds/world{0:04d}'
    filename_status = 'worlds/status'
    #Create worlds directory if it doesn't exist
    if not os.path.isdir('worlds'):
        os.mkdir('worlds')

    time_range = range(time)
    for i in time_range:
        print(f'Computing time step: {i}')
        simulation.move_people(i)

        simulation.infect_people()
        simulation.recover_people()

        simulation.write_populated_world(filename_world.format(i))

        simulation.count_cases()

        simulation.write_status(filename_status)

    print('Generating movie. This takes quite some time.')
    generate_movie('Movie', time)


if __name__ == '__main__':
    main()
