'''Imports'''

from __future__ import annotations
import random

'''Classes'''

# Vacuum Environment Class
class VacuumEnvironment:
    def __init__(self, width, height, dirt = None) -> None:
        self.width = width
        self.height = height
        self.locations = []
        self.dirt = []
        self.genDirt()
        self.genLocations()

    #Generates a list of all valid locations within the environment
    def genLocations(self):
        for x in range(self.width):
            for y in range(self.height):
                self.locations.append((x,y))                 

    #Generates a list of dirty locations inside the environment
    def genDirt(self):
        for x in range(self.width):
            for y in range(self.height):
                if random.randint(0,1) == 1:
                    self.dirt.append((x,y))
    
    #Removes a location from the dirt list
    def cleanLocation(self, agent: VacuumAgent, location):
        if location in self.dirt:
            self.dirt.remove(location)

    #Checks the dirt/clean state of a given location
    def isClean(self, location):
        if location in self.dirt:
            return False
        else:
            return True
      
                
# Vacuum Agent Class
class VacuumAgent:
    def __init__(self, program = 'ReflexAgent', defaultLocation = (0, 0)) -> None:
        self.bump = False
        self.program = program
        self.performance = 0
        self.location = defaultLocation
        #State only used for when programming is not reflex or random based
        self.map = [] 

    #The sensors available to the agent are accessed through this function
    def sense(self, env: VacuumEnvironment):
        if env.isClean(self.location):
            return 'Clean'
        else:
            return 'Dirty'

    #All valid moves are sensed with a given step size, NOT in use for this agent    
    def validMove(self, env: VacuumEnvironment, step = 1):
        moveloc = []
        for loc in env.locations:
            x = loc[0]
            y = loc[1]

            if(y == self.location[1]):
                if x == self.location[0] + step:
                    moveloc.append(loc)
                elif x == self.location[0] - step:
                    moveloc.append(loc)
                    
            elif(x == self.location[0]):
                if y == self.location[1] + step:
                    moveloc.append(loc)
                elif y == self.location[1] - step:
                    moveloc.append(loc)

        return moveloc
    
    #The actuators available to the agent are accessed through this function
    def actuate(self, action, env: VacuumEnvironment,):
        prevLoc = self.location

        if action == 'Right':
            self.location = (self.location[0] + 1, self.location[1])
            self.performance -= 1
        elif action == 'Left':
            self.location = (self.location[0] - 1, self.location[1])
            self.performance -= 1
        elif action == 'Up':
            self.location = (self.location[0], self.location[1] + 1)
            self.performance -= 1
        elif action == 'Down':
            self.location = (self.location[0], self.location[1] - 1)
            self.performance -= 1
        elif action == 'Suck':
            if env.isClean(self.location) == False:
                self.performance += 10
                env.cleanLocation(self, self.location)

        if(self.location not in env.locations):
            self.bump = True
            self.location = prevLoc

    #For the use of the state program of this agent. Adds a coordinate to the state list of invalid coordinates to remember not to use       
    def bumpListAppend(self, action):
        if action == 'Right':
            self.map.append((self.location[0] + 1, self.location[1]))

        elif action == 'Left':
            self.map.append((self.location[0] - 1, self.location[1]))

        elif action == 'Up':
            self.map.append((self.location[0], self.location[1] + 1))

        elif action == 'Down':
            self.map.append((self.location[0], self.location[1] - 1))

    #For the use of the state program of this agent. Checks if a given coordinate is in the bump list.
    def checkBumpList(self, location):
        if(location in self.map):
            return True
        else:
            return False

    #Given an action returns the resulting location of the agent
    def actionToLocation(self, action) -> tuple:
        if action == 'Right':
            return (self.location[0] + 1, self.location[1])

        elif action == 'Left':
            return (self.location[0] - 1, self.location[1])

        elif action == 'Up':
            return (self.location[0], self.location[1] + 1)

        elif action == 'Down':
            return (self.location[0], self.location[1] - 1)

    #Makes the agent take a step in the environment. Currently senses and takes an action.
    def act(self, env: VacuumEnvironment) -> str:
        if self.program == 'Reflex':

            actions = ['Right','Left','Suck']
            
            #Cleaning
            if self.sense(env) == 'Dirty':
                self.actuate(actions[2], env)
                return actions[2]

            #Movement
            elif self.sense(env) != 'Dirty': 
                if self.location in env.locations:
                    self.actuate(actions[0], env)
                    return actions[0]
                
        elif self.program == 'Reflex_2D':

            actions = ['Right','Left','Up','Down','Suck']
            
            #Cleaning
            if self.sense(env) == 'Dirty':
                self.actuate(actions[4], env)
                return actions[4]

            #Movement
            elif self.sense(env) != 'Dirty': 
                if self.location in env.locations:
                    random_move = random.choice(actions[:-1])
                    self.actuate(random_move, env)
                    return random_move
        
            
        elif self.program == 'Random':
            #Sense current location
            #If dirty clean
            if self.sense(env) == 'Dirty':
                self.actuate('Suck', env)
                return 'Suck'

            #Random Action to change location
            else:
                actions = ['Right','Left','Up','Down']
                randomAction = random.choice(actions)
                self.actuate(randomAction, env)
                return randomAction
    
        elif self.program == 'State':
            #Sense current location
            #If dirty clean
            if self.sense(env) == 'Dirty':
                self.actuate('Suck', env)
                return 'Suck'

            #Random actions to change location
            #Check if coordinate is stored in state
            #If not, perform selected action
            #If location did not change add coordinate as invalid to the state

            validChoice  = False

            while(validChoice == False):
                actions = ['Right','Left','Up','Down']
                randomAction = random.choice(actions)
                if(self.checkBumpList(self.actionToLocation(randomAction)) == False):
                    self.actuate(randomAction, env)
                    validChoice = True

            if(self.bump == True):
                self.bumpListAppend(randomAction)
                self.bump =  False
            
            return randomAction
