import math

from src.Agent import Prey, Predator
from src.Vector2D import Vector2D
import random


class Environment:

    def __init__(self, width, height, amount_of_prey, prey_max_age, prey_birth_rate, amount_of_hunters, hunter_max_age,
                 hunter_energy_to_reproduce, hunter_energy_per_prey_eaten):
        self.width = width
        self.height = height
        self.amount_of_prey = amount_of_prey
        self.prey_max_age = prey_max_age
        self.prey_birth_rate = prey_birth_rate
        self.amount_of_hunters = amount_of_hunters
        self.hunter_max_age = hunter_max_age
        self.hunter_energy_to_reproduce = hunter_energy_to_reproduce
        self.hunter_energy_per_prey_eaten = hunter_energy_per_prey_eaten
        self.predator_list = []
        self.prey_list = []
        self.amount_of_steps = 0
        self.generate_environment()
        self.is_running = True

    def generate_environment(self):
        for j in range(self.amount_of_prey):
            self.prey_list.append(self.generate_random_prey())
        for i in range(self.amount_of_hunters):
            self.predator_list.append(self.generate_random_predator())

    def generate_random_prey(self):
        pos = Vector2D(random.randint(0, self.width),
                       random.randint(0, self.height))
        prey = Prey(0, pos, self.prey_max_age, self.prey_birth_rate)

        return prey

    def generate_random_predator(self):
        pos = Vector2D(random.randint(0, self.width),
                       random.randint(0, self.height))
        predator = Predator(0, pos, self.hunter_max_age, 20, self.hunter_energy_to_reproduce,
                            self.hunter_energy_per_prey_eaten)
        return predator

    def reproduce_prey(self, prey):
        pos = Vector2D(prey.position.X, prey.position.Y)
        prey = Prey(0, pos, self.prey_max_age, self.prey_birth_rate)
        return prey

    def reproduce_predator(self, predator):
        pos = Vector2D(predator.position.X, predator.position.Y)
        predator = Predator(0, pos, self.hunter_max_age, 20, self.hunter_energy_to_reproduce,
                            self.hunter_energy_per_prey_eaten)
        return predator

    def step(self, env = None, actions = None):
        self.amount_of_steps += 1
        print('Step: ', self.amount_of_steps)

        if env == "prey":
            self.update_preys(random = False, actions = actions)
        else:
            self.update_preys(True)

        if env == "predator":
            self.update_predators(random = False, actions = actions)
        else:
            self.update_predators(True)

        #if (self.is_prey_extinct()) or (self.is_predator_extinct()) or (self.is_overpopulated()):
        #    self.stop()

        return self.is_prey_extinct() or self.is_predator_extinct() or self.is_overpopulated()

    def reset(self):
        self.stop()
        self.predator_list = []
        self.prey_list = []
        self.amount_of_steps = 0
        self.generate_environment()

    def stop(self):
        print('The simulation has ended:')
        self.is_running = False

    def update_preys(self, random = True, actions = None):
        temp_prey_list = []
        actionCtr = 0
        while self.prey_list:
            prey = self.prey_list.pop()
            prey.dies_at_max_age()
            prey.age += 1
            if not prey.is_dead:
                prey.try_reproduce()
                if prey.is_reproducing:
                    temp_prey_list.append(self.reproduce_prey(prey))
                if random:
                    prey.move()
                else:
                    prey.move(actions["prey_"+str(actionCtr)])

                temp_prey_list.append(prey)
            actionCtr += 1
        while temp_prey_list:
            self.prey_list.append(temp_prey_list.pop())

    def update_predators(self, random = True, actions = None):
        temp_predator_list = []
        actionCtr = 0
        while self.predator_list:
            predator = self.predator_list.pop()
            predator.dies_at_max_age()
            predator.dies_when_no_energy()
            predator.age += 1
            predator.energy_level -= 1
            if not predator.is_dead:
                self.try_eat_prey(predator)
                if random:
                    predator.move()
                else:
                    if actions["predator_"+str(actionCtr)] == 5:
                        predator.try_reproduce()
                        if predator.is_reproducing:
                            temp_predator_list.append(self.reproduce_predator(predator))
                    else:
                        predator.move(actions["predator_"+str(actionCtr)])
                temp_predator_list.append(predator)
            actionCtr += 1

        while temp_predator_list:
            self.predator_list.append(temp_predator_list.pop())
        print(len(self.predator_list))

    def getClosestPredator(self, prey):
        closestDistance = -1
        closestPredator = None

        for p in self.predator_list:
            dx = prey.position.X - p.position.X
            dy = prey.position.Y - p.position.Y
            d = math.sqrt(dx * dx + dy * dy)
            if d < closestDistance or closestDistance == -1:
                closestPredator = p

        return closestPredator

    def getClosestPrey(self, predator):
        closestDistance = -1
        closestPrey = None

        for p in self.prey_list:
            dx = predator.position.X - p.position.X
            dy = predator.position.Y - p.position.Y
            d = math.sqrt(dx * dx + dy * dy)
            if d < closestDistance or closestDistance == -1:
                closestPrey = p

        return closestPrey


    def prey_obs(self):
        obs = {}
        prey_ctr  =0
        for p in self.prey_list:
            closestPredator = self.getClosestPredator(p)

            if closestPredator is None:
                obs["prey_" + str(prey_ctr)] = [p.age, 0, 0]
            else:
                obs["prey_"+str(prey_ctr)] = [p.age, abs(closestPredator.position.X - p.position.X), abs(closestPredator.position.Y - p.position.Y)]
            prey_ctr += 1
        return obs

    def predator_obs(self):
        obs = {}
        predator_ctr = 0
        for p in self.predator_list:
            closestPrey = self.getClosestPrey(p)
            if closestPrey is None:
                obs["predator_" + str(predator_ctr)] = [p.age, p.energy_level, 0, 0]
            else:
                obs["predator_"+str(predator_ctr)] = [p.age, p.energy_level, abs(closestPrey.position.X - p.position.X),
                            abs(closestPrey.position.Y - p.position.Y)]
            predator_ctr += 1
        return obs

    def prey_rewards(self):
        rewards = {}
        prey_ctr = 0
        #Reward is number of preys
        for p in self.prey_list:
            rewards["prey_"+str(prey_ctr)] = len(self.prey_list)
            prey_ctr += 1
        return rewards

    def predator_rewards(self):
        rewards = {}
        predator_ctr = 0
        # Reward is number of predators
        for p in self.predator_list:
            rewards["predator_"+str(predator_ctr)] = len(self.predator_list)
            predator_ctr += 1
        return rewards

    def prey_dones(self):
        dones ={"__all__": self.is_prey_extinct() or self.is_predator_extinct() or self.is_overpopulated()}
        prey_ctr = 0
        # Reward is number of predators
        for p in self.prey_list:
            dones["prey_"+str(prey_ctr)] = p.is_dead
            prey_ctr += 1
        return dones

    def predator_dones(self):
        dones = {"__all__": self.is_prey_extinct() or self.is_predator_extinct() or self.is_overpopulated()}
        predator_ctr = 0
        # Reward is number of predators
        for p in self.predator_list:
            dones["predator_"+str(predator_ctr)] = p.is_dead
            predator_ctr += 1
        return dones

    def try_eat_prey(self, predator):
        temp_prey_list = []
        while self.prey_list:
            prey = self.prey_list.pop()
            if (predator.position.X-2 <= prey.position.X <= predator.position.X+2) and\
                    (predator.position.Y-2 <= prey.position.Y <= predator.position.Y+2):
                prey.is_dead = True
                # print('A prey was eaten')
                predator.energy_level += predator.energy_per_prey_eaten
            else:
                temp_prey_list.append(prey)
        while temp_prey_list:
            self.prey_list.append(temp_prey_list.pop())

    def is_prey_extinct(self):
        if not self.prey_list:
            return True
        else:
            return False

    def is_predator_extinct(self):
        if not self.predator_list:
            return True
        else:
            return False

    def is_overpopulated(self):
        if (len(self.prey_list) > 10000) or (len(self.predator_list) > 10000):
            return True
        else:
            return False

    def print_amount_of_prey(self):
        print('There are ', len(self.prey_list), 'prey left')

    def print_amount_of_predators(self):
        print('There are ', len(self.predator_list), 'predators left')
