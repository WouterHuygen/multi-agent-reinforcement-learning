import math

from src.Agent import Prey, Predator
from src.Vector2D import Vector2D
import random
from src.SimulatorParameters import sim_params


class Environment:

    def __init__(self, width, height, amount_of_prey, prey_max_age, prey_birth_rate, amount_of_hunters, hunter_max_age,
                 hunter_energy_to_reproduce, hunter_energy_per_prey_eaten, init_energy):
        self.width = width
        self.height = height
        self.max_amount_of_prey = amount_of_prey
        self.prey_max_age = prey_max_age
        self.prey_birth_rate = prey_birth_rate
        self.max_amount_of_hunters = amount_of_hunters
        self.hunter_max_age = hunter_max_age
        self.hunter_energy_to_reproduce = hunter_energy_to_reproduce
        self.hunter_energy_per_prey_eaten = hunter_energy_per_prey_eaten
        self.init_energy = init_energy
        self.predator_list = []
        self.dead_predator = []
        self.prey_list = []
        self.dead_prey = []
        self.amount_of_steps = 0
        self.is_running = True
        self.prey_reward = 0
        self.predator_reward = 0
        self.number_of_living_predators = 0
        self.number_of_living_preys = 0
        self.generate_environment()

    def generate_environment(self):
        for j in range(int(sim_params["init_amount_of_prey"])):
            self.prey_list.append(self.generate_random_prey())
            self.number_of_living_preys += 1
        for i in range(int(sim_params["init_amount_of_hunters"])):
            self.predator_list.append(self.generate_random_predator())
            self.number_of_living_predators += 1



    def generate_random_prey(self):
        pos = Vector2D(random.randint(0, self.width),
                       random.randint(0, self.height))
        prey = Prey(0, pos, self.prey_max_age, self.prey_birth_rate)
        return prey

    def generate_random_predator(self):
        pos = Vector2D(random.randint(0, self.width),
                       random.randint(0, self.height))
        predator = Predator(0, pos, self.hunter_max_age, self.init_energy, self.hunter_energy_to_reproduce,
                            self.hunter_energy_per_prey_eaten)
        return predator

    def reproduce_prey(self, prey):
        pos = Vector2D(prey.position.X, prey.position.Y)
        prey = Prey(0, pos, self.prey_max_age, self.prey_birth_rate)
        return prey

    def reproduce_predator(self, predator):
        pos = Vector2D(predator.position.X, predator.position.Y)
        predator = Predator(0, pos, self.hunter_max_age, self.init_energy, self.hunter_energy_to_reproduce,
                            self.hunter_energy_per_prey_eaten)
        return predator

    def step(self, env = None, actions = None):
        self.amount_of_steps += 1
        # print("-----------------------------------------------------")
        # print("NumberOfPredators: "+str(Predator.numberOfPredators))
        # print("Predators Alive: "+str(len(self.predator_list)))
        # print("Predators dead: "+str(len(self.dead_predator)))
        # print("NumberOfPreys: " + str(Prey.numberOfPreys))
        # print("Preys Alive: " + str(len(self.prey_list)))
        # print("Preys dead: " + str(len(self.dead_prey)))
        # print("-----------------------------------------------------")
        if env == "prey" or env == "multiagent":
            self.update_preys(random = False, actions = actions)
        else:
            self.update_preys()

        if env == "predator" or env == "multiagent":
            self.update_predators(random = False, actions = actions)
        else:
            self.update_predators()

        #if (self.is_prey_extinct()) or (self.is_predator_extinct()) or (self.is_overpopulated()):
        #    self.stop()

        return self.is_prey_extinct() or self.is_predator_extinct()

    def reset(self):
        #print("Resetting")
        self.predator_list = []
        self.prey_list = []
        self.dead_prey = []
        self.dead_predator = []
        self.amount_of_steps = 0
        Prey.numberOfPreys = 0
        Predator.numberOfPredators = 0
        self.predator_reward = 0
        self.prey_reward = 0
        self.number_of_living_predators = 0
        self.number_of_living_preys = 0
        self.generate_environment()

    def stop(self):
        print('The simulation has ended:')
        self.is_running = False

    def update_preys(self, random = True, actions = None):
        new_preys = []
        dying_preys = []
        for p in self.prey_list:
            p.is_dead = self.prey_get_eaten(p) or (p.age >= self.prey_max_age)
            if self.prey_get_eaten(p):
                self.prey_reward -= 1
            p.age += 1
            if not p.is_dead:
                p.try_reproduce()
                if p.is_reproducing and (self.number_of_living_preys < self.max_amount_of_prey):
                    new_preys.append(self.reproduce_prey(p))
                    self.number_of_living_preys += 1
                if random:
                    p.move()
                else:
                    p.move(actions[p.id])
            else:
                dying_preys.append(p)
                self.number_of_living_preys -= 1

        for p in new_preys:
            self.prey_list.append(p)

        for p in dying_preys:
            self.prey_list.remove(p)
            self.dead_prey.append(p)

    def update_predators(self, random = True, actions = None):
        new_predators = []
        dying_predators = []
        for predator in self.predator_list:
            predator.is_dead = (predator.energy_level <= 0) or (predator.age >= self.hunter_max_age)
            predator.age += 1
            predator.energy_level -= 1
            if not predator.is_dead:
                if self.try_eat_prey(predator):
                    self.predator_reward += 1
                    predator.energy_level += self.hunter_energy_per_prey_eaten
                if random:
                    predator.move()
                else:
                    if actions[predator.id] == 4:
                        predator.try_reproduce()
                        if predator.is_reproducing and (self.number_of_living_predators < sim_params["max_amount_of_hunters"]):
                            new_predators.append(self.reproduce_predator(predator))
                            self.number_of_living_predators += 1
                            predator.is_reproducing =  False
                            self.predator_reward += 4
                    else:
                        predator.move(actions[predator.id])
            else:
                dying_predators.append(predator)
                self.number_of_living_predators -= 1

        for p in new_predators:
            self.predator_list.append(p)

        for p in dying_predators:
            self.predator_list.remove(p)
            self.dead_predator.append(p)


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

    def total_obs(self):
        obs = {}
        for p in self.prey_list:
            closestPredator = self.getClosestPredator(p)
            if closestPredator is None:
                obs[p.id] = [p.age, 0, 0]
            else:
                obs[p.id] = [p.age, abs(closestPredator.position.X - p.position.X),
                             abs(closestPredator.position.Y - p.position.Y)]
        for p in self.dead_prey:
            obs[p.id] = [0, 0, 0]
        for p in self.predator_list:
            closestPrey = self.getClosestPrey(p)
            if closestPrey is None:
                obs[p.id] = [p.age, p.energy_level, 0, 0]
            else:
                obs[p.id] = [p.age, p.energy_level, abs(closestPrey.position.X - p.position.X),
                             abs(closestPrey.position.Y - p.position.Y)]
        for p in self.dead_predator:
            obs[p.id] = [0, 0, 0, 0]
        return obs

    def prey_obs(self):
        obs = {}
        for p in self.prey_list:
            closestPredator = self.getClosestPredator(p)
            if closestPredator is None:
                obs[p.id] = [p.age, 0, 0]
            else:
                obs[p.id] = [p.age, abs(closestPredator.position.X - p.position.X), abs(closestPredator.position.Y - p.position.Y)]
        for p in self.dead_prey:
             obs[p.id] = [0, 0, 0]
        return obs

    def predator_obs(self):
        obs = {}
        for p in self.predator_list:
            closestPrey = self.getClosestPrey(p)
            if closestPrey is None:
                obs[p.id] = [p.age, p.energy_level, 0, 0]
            else:
                obs[p.id] = [p.age, p.energy_level, abs(closestPrey.position.X - p.position.X),
                            abs(closestPrey.position.Y - p.position.Y)]

        for p in self.dead_predator:
            obs[p.id] = [0, 0, 0, 0]
        return obs

    def total_rewards(self):
        rewards = {}
        # Reward is number of preys
        for p in self.prey_list:
            # rewards[p.id] = self.prey_reward
            rewards[p.id] = self.prey_reward
        for p in self.dead_prey:
            rewards[p.id] = self.prey_reward
            # Reward is number of predators
        for p in self.predator_list:
            # rewards[p.id] = self.predator_reward
            rewards[p.id] = self.predator_reward
        for p in self.dead_predator:
            rewards[p.id] = self.predator_reward
        return rewards
    def prey_rewards(self):
        rewards = {}
        #Reward is number of preys
        for p in self.prey_list:
            #rewards[p.id] = self.prey_reward
            rewards[p.id] = len(self.prey_list)
        for p in self.dead_prey:
            rewards[p.id] = 0
        return rewards

    def predator_rewards(self):
        rewards = {}
        # Reward is number of predators
        for p in self.predator_list:
            #rewards[p.id] = self.predator_reward
            rewards[p.id] = len(self.predator_list)
        for p in self.dead_predator:
            rewards[p.id] = 0
        return rewards

    def total_dones(self):
        dones = {"__all__": self.is_prey_extinct() or self.is_predator_extinct()}
        for p in self.prey_list:
            dones[p.id] = p.is_dead
        for p in self.dead_prey:
            dones[p.id] = p.is_dead
        for p in self.predator_list:
            dones[p.id] = p.is_dead
        for p in self.dead_predator:
            dones[p.id] = p.is_dead
        return dones

    def prey_dones(self):
        dones ={"__all__": self.is_prey_extinct() or self.is_predator_extinct()}
        for p in self.prey_list:
            dones[p.id] = p.is_dead
        for p in self.dead_prey:
            dones[p.id] = p.is_dead
        return dones

    def predator_dones(self):
        dones = {"__all__": self.is_prey_extinct() or self.is_predator_extinct()}
        for p in self.predator_list:
            dones[p.id] = p.is_dead
        for p in self.dead_predator:
            dones[p.id] = p.is_dead
        return dones

    def try_eat_prey(self, predator):
        preyEaten = False
        for prey in self.prey_list:
            if (predator.position.X-2 <= prey.position.X <= predator.position.X+2) and\
                    (predator.position.Y-2 <= prey.position.Y <= predator.position.Y+2):
                preyEaten = True
                self.predator_reward += 1
        return preyEaten

    def prey_get_eaten(self, prey):
        is_dead = False
        for predator in self.predator_list:
            if (predator.position.X-2 <= prey.position.X <= predator.position.X+2) and\
                    (predator.position.Y-2 <= prey.position.Y <= predator.position.Y+2):
                is_dead = True
                self.prey_reward -= 1
        return  is_dead

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
