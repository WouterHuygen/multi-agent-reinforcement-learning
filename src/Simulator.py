from src.Environment import Environment
from src.SimulatorParameters import sim_params
import time
import pygame
import sys

GREEN = (0, 100, 0)
RED = (100, 0, 0)
TILE_SIZE = 4


class Simulator:

    def __init__(self):
        print('Welcome to the Predator-Prey-Simulator created by Wouter Huygen')
        self.environment = Environment(sim_params['environment_width'], sim_params['environment_height'],
                                       sim_params['amount_of_prey'], sim_params['prey_max_age'],
                                       sim_params['prey_birth_rate'],
                                       sim_params['amount_of_hunters'], sim_params['hunter_max_age'],
                                       sim_params['hunter_energy_to_reproduce'],
                                       sim_params['hunter_energy_per_prey_eaten'])
        pygame.init()
        self.DISPLAY = pygame.display.set_mode((sim_params['environment_width'] * TILE_SIZE,
                                                sim_params['environment_height'] * TILE_SIZE))

    def run(self):
        while self.environment.is_running:
            self.environment.step()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw_prey()
            self.draw_predator()
            pygame.display.update()
            self.DISPLAY.fill((0, 0, 0))
            time.sleep(1. / 1)

    def reset(self):
        print("The reset method isn't implemented yet")

    def draw_prey(self):
        for prey in self.environment.prey_list:
            pygame.draw.rect(self.DISPLAY, GREEN,
                             (prey.position.X * TILE_SIZE, prey.position.Y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw_predator(self):
        for prey in self.environment.predator_list:
            pygame.draw.rect(self.DISPLAY, RED,
                             (prey.position.X * TILE_SIZE, prey.position.Y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


if __name__ == '__main__':
    simulator = Simulator()
    simulator.simulator_run()
