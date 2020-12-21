import random
from src.SimulatorParameters import sim_params


class Agent:

    def __init__(self, age, position, max_age):
        self.age = age
        self.position = position
        self.max_age = max_age
        self.is_dead = False
        self.is_reproducing = False

    def move(self, action = None):
        # Action numbers: 0 = STATIONARY, 1=UP, 2=RIGHT, 3=DOWN, 4=LEFT
        if action == None:
            action = random.randint(0, 4)

        if (action == 1) and (self.position.Y > 0):
            self.position.Y -= 1
        elif (action == 2) and (self.position.X < sim_params['environment_width']):
            self.position.X += 1
        elif (action == 3) and (self.position.Y < sim_params['environment_height']):
            self.position.Y += 1
        elif (action == 4) and (self.position.X > 0):
            self.position.X -= 1

    def try_reproduce(self):
        print('This agent is trying to reproduce')

    def dies_at_max_age(self):
        if self.age >= self.max_age:
            self.die()

    def die(self):
        print('An agent died')
        self.is_dead = True

    def print_pos(self):
        print('X: ', self.position.X, ' Y: ', self.position.Y)


class Prey(Agent):

    def __init__(self, age, position, max_age, birth_rate):
        super().__init__(age, position, max_age)
        self.birth_rate = birth_rate


    def try_reproduce(self):
        r = random.randint(0, 100)
        if r <= self.birth_rate:
            self.is_reproducing = True

    def die(self):
        # print('A prey died')
        self.is_dead = True

    def step(self, action = None):
        self.age += 1
        if action is None:
            self.move()
        else:
            self.move(action)
        out = self.try_reproduce()
        out = out, self.will_die()
        return out


class Predator(Agent):

    def __init__(self, age, position, max_age, energy_level, energy_to_reproduce, energy_per_prey_eaten):
        super().__init__(age, position, max_age)
        self.energy_level = energy_level
        self.energy_to_reproduce = energy_to_reproduce
        self.energy_per_prey_eaten = energy_per_prey_eaten

    def try_reproduce(self):
        if self.energy_level >= self.energy_to_reproduce:
            self.is_reproducing = True

    def dies_when_no_energy(self):
        if self.energy_level <= 0:
            self.die()

    def die(self):
        # print('A predator died')
        self.is_dead = True
