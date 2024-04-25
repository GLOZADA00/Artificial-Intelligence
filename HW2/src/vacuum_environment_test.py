'''Imports'''
import random
import collections
 
'''Classes'''
class Thing:
    def __init__(self, name):
        self.name = name
        
class Dirt(Thing):
    pass

class Wall(Thing):
    pass

class Obstacle(Thing):
    pass

class Agent(Thing):
    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None or not isinstance(program, collections.abc.Callable):
            print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

            def program(percept):
                return eval(input('Percept={}; action? '.format(percept)))

        self.program = program

    def can_grab(self, thing):
        return False

def TraceAgent(agent):
    old_program = agent.program

    def new_program(percept):
        action = old_program(percept)
        print('{} perceives {} and does {}'.format(agent, percept, action))
        return action

    agent.program = new_program
    return agent


class Environment:
    def __init__(self, width, height):
        # Initialize the 2D array with all locations as 'Clean'
        self.width = width
        self.height = height
        self.grid = [['Clean' for _ in range(width)] for _ in range(height)]
        self.things = []
        
    def dirty_locations(self, dirt_count):
        # Mark a specified number of random locations as 'Dirty'
        for _ in range(dirt_count):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            dirt = Dirt()
            self.grid[x][y] = dirt.name
            self.things.append((dirt, x, y))
            
    def add_thing(self, thing, x, y):
        # Add a Thing (obstacle or agent) to the specified location
        if 0 <= x < self.width and 0 <= y < self.height:
            self.things.append((thing, x, y))
            
    def get_thing_location(self, thing):
        # Get the location of a specific Thing
        for t, x, y in self.things:
            if t == thing:
                return x, y
        return None
    
    def print_environment(self):
        # Print the current state of the environment
        for row in self.grid:
            print(row)
            
        for thing, x, y in self.things:
            print(f'{thing.name} at ({x}, {y})')
    
class Environment_2D(Environment):
    def __init__(self, width, height):
        super().__init__(width, height)