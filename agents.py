import numpy as np
import random as rd
import math
from map import *

# Defintion of the agent class and its characteristics:
# Speed
# Size
# View range

class agent_class:

    # All agents have the same enery. 
    # This is consumed at each step based on its characteristics.
    # It is fully charged at the beginning of the next day and an agent dies when it gets to zero.
    energy = 500.0 

    # The curvature decides how much an agent changes its direction after each step.
    curvature = 0.05 

    # There are many states: Search, Food, Home, Wait, Dead.
    state = "Search"

    # Attitude of curving clockwise (negative), anti-clockwise (positive) or mantain the direction (zero)
    orientation = 0

    # Number of food eaten in the current day
    food_count = 0
    
    # List of Food inside the view range
    food_seen = [] 

    # List of hunters in the view range
    hunters_seen = []

    # List of prays in the view range
    prays_seen = []
    
    hunters_list = []
    prays_list = []
    # Direction in radiant with respect to the x positive axis
    direction = 0.0

    previous_state = "Search"

    # Generator of the agents
    def __init__(self, speed = 1.0, x = 50.0, y = 0.0, size = 1.0, view = 1.0, xlim = 100, ylim = 100):
        
        # Speed decide the length of each step and the amount of energy consumed to make it
        self.speed = float(speed)

        # Size can allow to eat smaller agents
        self.size = size

        # The view range of the agent to see both food and other agents
        self.view = view

        # Position in the 2D space
        self.x_position = float(x) # position of the agent
        self.y_position = float(y) 

        self.xlim = xlim 
        self.ylim = ylim


    # Function to compute the direction of the agent based on the state he is in 
    def change_direction(self, list_agents):

        change_orientation_prob = 0.3

        # If no food is in sight and the agent is looking for it we change randomly its movement
        if self.state == "Search":

            # Direction is changed based on the fixed curvature and the orientation
            self.direction += self.curvature * self.orientation

            # The orientation can change in range [-3;+3] but the probability changes based on the current orientation
            coin_flip = rd.uniform(0,1)
            if coin_flip < (change_orientation_prob + self.orientation * 0.1) :
                self.orientation -= 1
            elif coin_flip > (1 - change_orientation_prob + self.orientation * 0.1):
                self.orientation += 1  


            # If the agent reaches the borders the direction is changed automatically so that it is perpendicular to the side
            if np.abs(self.x_position - 0.0) < 1:
                self.direction = 0.0
            elif np.abs(self.x_position - self.xlim) < 1:
                self.direction = np.pi

            if np.abs(self.y_position - 0.0) < 1:
                self.direction = np.pi/2
            elif np.abs(self.y_position - self.ylim) < 1:
                self.direction = np.pi*3/2 

        # In the found state the agent moves toward the food
        elif self.state == "Found":
            self.direction = math.atan2(self.food_seen.y - self.y_position,self.food_seen.x - self.x_position)

        # In the home state the agent moves toward the closest side of the table
        elif self.state == "Home":

            distances = [np.abs(self.x_position - 0), np.abs(self.x_position - self.xlim), np.abs(self.y_position - 0), np.abs(self.y_position - self.ylim)]
            min_pos = distances.index(min(distances))
            if distances[min_pos] < 1:
                self.state = "Wait"

            if min_pos == 0:
                self.direction = np.pi
            elif min_pos == 1:
                self.direction = 0.0
            elif min_pos == 2:
                self.direction = np.pi*3 / 2
            elif min_pos == 3:
                self.direction = np.pi/2

        elif self.state == "Feared":
            vectors = []
            for agent_id in self.hunter_seen:
                x_component = self.x_position - list_agents[agent_id].x_position
                y_component = self.y_position - list_agents[agent_id].y_position
                norm = np.sqrt(x_component**2 + y_component**2)
                if norm > 1e-6:
                    vectors.append((x_component/norm, y_component/norm))
            
            x_component = 0
            y_component = 0
            for vector in vectors:
                x_component += vector[0]
                y_component += vector[1]                

            # this may not be necessary            
            norm = np.sqrt(x_component**2 + y_component**2)
            if norm > 1e-6:    
                self.direction = math.atan2(y_component/norm,x_component/norm)

        elif self.state == "Hunt":
            minimum = 100
            for agent_id in self.prays_seen:
                if compute_distance_agents(self,list_agents[agent_id]) < minimum:
                    minimum = compute_distance_agents(self,list_agents[agent_id])
                    self.direction = math.atan2(list_agents[agent_id].y_position - self.y_position,list_agents[agent_id].x_position - self.x_position)


    # Function that moves an agent
    def step(self, list_agents, delta_time, step_size):
        # The only states in which we don't move are wait and dead
        if self.state != "Wait" and self.state != "Dead" and self.state!="Killed":

            self.change_direction(list_agents)

            self.x_position += np.cos(self.direction)*delta_time*self.speed*step_size
            self.y_position += np.sin(self.direction)*delta_time*self.speed*step_size

            self.update_energy()
            
            if self.x_position > self.xlim:
                self.x_position = self.xlim
            elif self.x_position < 0.0:
                self.x_position = 0.0

            if self.y_position > self.ylim:
                self.y_position = self.ylim
            elif self.y_position < 0.0:
                self.y_position = 0.0

            return 1       
        # change with environment constrains

        else:
            return 0


    # This function estimate if there is food in sight
    def look_around(self, list_agents,list_food):
        if self.state == "Dead" or self.state == "Wait" or self.state == "Killed":
            return 
        
        self.hunter_seen = []
        self.prays_seen = []
        for agent_id in self.hunters_list:
            if compute_distance_agents(self,list_agents[agent_id])< self.view * 5 and list_agents[agent_id] != "Dead" and list_agents[agent_id]!="Killed" and list_agents[agent_id]!= "Wait":
                self.hunter_seen.append(agent_id)
        
        if len(self.hunter_seen) != 0:
            self.previous_state = self.state
            self.state = "Feared"
            return 
        
        if len(self.hunter_seen) == 0 and self.state == "Feared":
            self.state = self.previous_state

        # If the state is search we look for the first food in sight. 
        # Since this is performed after each step we should find the closest and the process does not have to be repeated
        if self.state == "Search" or self.state == "Hunt":
            for i, food in enumerate(list_food):
                if compute_distance_food(self,food) < self.view * 5:
                    self.state = "Found"
                    self.food_seen = food
                    break
            
            for agent_id in self.prays_list:
                if compute_distance_agents(self,list_agents[agent_id])< self.view * 5 and list_agents[agent_id].state != "Killed" and list_agents[agent_id].state != "Wait":
                    self.prays_seen.append(agent_id)
            if len(self.prays_seen) != 0:
                self.state = "Hunt"


    # update the game if the agent is able to eat something
    def eat(self, list_agents,list_food):
        # If state is found we check if we are on top of it or if the food is still available
        if self.state == "Found":
            if self.food_seen in list_food:
                if compute_distance_food(self,self.food_seen) < 1.0:
                    self.state = "Search"
                    list_food.remove(self.food_seen)
                    self.food_seen = []
                    self.food_count += 1
            else:
                self.state = "Search"
                self.food_seen = []
            
            return

        if self.state == "Hunt":
            if len(self.prays_seen) == 0:
                self.state = "Search"
                return 
            for agent_id in self.prays_seen:
                if compute_distance_agents(self,list_agents[agent_id]) < 1.0 and list_agents[agent_id].state != "Killed" and list_agents[agent_id].state != "Wait":
                    self.state = "Search"
                    list_agents[agent_id].kill()
                    self.food_seen = []
                    self.food_count += 1
                    return
    
    
    # This function make the decision of the next action of the agent based on its information
    def decide_state(self):

        if self.state == "Killed":
            return
        
        # State wait can't be changed until end of the day
        if self.state == "Wait":
            return

        # Dead is achived when energy is zero, it can still be eaten 
        if self.energy <= 0:
            self.state = "Dead"
            return
    
        # When an agent has eaten two food it automatically goes home
        elif self.food_count > 1:
            self.state = "Home"
            return 
        
        # If the agent is low on energy and has already eaten it will go home
        elif self.food_count == 1 and self.energy < 100 and self.state == "Search": # cambiare con una condizione migliore sull'energia
            self.state = "Home"

        if len(self.hunters_seen) == 0 and len(self.prays_seen)==0 and self.state != "Found" and self.state!="Home":
            self.state = "Search"


    # Function to print the information of the agent
    def print_agent(self):
        print(f"Speed: {self.speed}; Size: {self.size}; View range: {self.view}")


    # Function that checks which are the agents that could hunt or be hunted by the agent.
    # This has to be lunched at the beginning of each day.
    def identify_prays_hunters(self, list_agents, n ):
        self.hunters_list = []
        self.prays_list =  []

        for i,p in enumerate(list_agents):
            if (self.size * 1.2) < p.size:
                self.hunters_list.append(i)

            elif self.size > (p.size * 1.2):
                self.prays_list.append(i)


    # Function that has the formula of the energy update
    def update_energy(self):
        self.energy -= (self.size * self.speed**2 + self.view)

    
    # Invoked when then agent is killed by another one 
    def kill(self):
        self.energy = 0
        self.state = "Killed"
        print("I've been killed")


def compute_avg_speed(list_agents):
    if len(list_agents )==0:
        return 0
    total = 0
    for agent in list_agents:
        total += agent.speed
    return total/len(list_agents)

def compute_avg_size(list_agents):
    if len(list_agents )==0:
        return 0
    total = 0
    for agent in list_agents:
        total += agent.size
    return total/len(list_agents)

def compute_avg_view(list_agents):
    if len(list_agents )==0:
        return 0
    total = 0
    for agent in list_agents:
        total += agent.view
    return total/len(list_agents)

def create_new_agent(speed = 1, size = 1, view = 1, xlim = 100.0, ylim = 100.0):
    coin_flip = rd.uniform(0,1)
    if coin_flip < 1/4:
        new_agent = agent_class(speed = speed, x = rd.uniform(0.01,xlim - 0.01), y = ylim, size = size, view = view, xlim=xlim, ylim = ylim)
    elif coin_flip < 2/4:
        new_agent = agent_class(speed = speed, x = xlim , y = rd.uniform(0.01,ylim - 0.01), size = size, view = view, xlim=xlim, ylim = ylim)
    elif coin_flip < 3/4:
        new_agent = agent_class(speed = speed, x = rd.uniform(0.01, xlim - 0.01), y = 0.0, size = size, view = view, xlim=xlim, ylim = ylim)
    else:
        new_agent = agent_class(speed = speed, x = 0.0 , y = rd.uniform(0.01, ylim - 0.01), size = size, view = view, xlim=xlim, ylim = ylim)

    return new_agent

def create_list_agents(n = 10, xlim = 100, ylim = 100):
    list_agents = []
    for i in range(n):
        list_agents.append(create_new_agent(xlim = xlim, ylim = ylim))

    return list_agents

def duplicate_agent_with_mutations(speed, size, view, speed_mutation = True, size_mutation = False, view_mutation = False, xlim = 100.0, ylim = 100.0):

    if speed_mutation:
        speed_variation = rd.uniform(-0.2, 0.2)
    else:
        speed_variation = 0

    if size_mutation:
        size_variation = rd.uniform(-0.2, 0.2)
    else:
        size_variation = 0
    
    if view_mutation:
        view_variation = rd.uniform(-0.2, 0.2)
    else:
        view_variation = 0

    coin_flip = rd.uniform(0,1)
    if coin_flip < 1/4:
        new_agent = agent_class(speed = speed + speed_variation, x = rd.uniform(0.01, xlim - 0.01), y = ylim, size = size + size_variation, view = view + view_variation, xlim= xlim, ylim = ylim )
    elif coin_flip < 2/4:
        new_agent = agent_class(speed = speed + speed_variation, x = xlim, y = rd.uniform(0.01, ylim - 0.01), size = size + size_variation, view = view + view_variation, xlim= xlim, ylim = ylim)
    elif coin_flip < 3/4:
        new_agent = agent_class(speed = speed + speed_variation, x = rd.uniform(0.01, xlim - 0.01), y = 0.0, size = size + size_variation, view = view + view_variation, xlim= xlim, ylim = ylim)
    else:
        new_agent = agent_class(speed = speed + speed_variation, x=0.0, y = rd.uniform(0.01, ylim - 0.01), size = size + size_variation, view = view + view_variation, xlim= xlim, ylim = ylim)
    
    return new_agent

def clear_stage(list_agents, speed_mutation = False, size_mutation = False, view_mutation = False, xlim = 100.0, ylim = 100.0):
    
    list_cloned_agents = []
    list_deleted_agents = []
    for agent in list_agents:
        if agent.state == "Dead" or agent.state == "Killed":
            list_deleted_agents.append(agent)
            continue 
        elif agent.state == "Wait" :
            agent.state = "Search"
            agent.energy = 500
            agent.food_seen = []
            if agent.food_count > 1:
                list_cloned_agents.append(duplicate_agent_with_mutations(agent.speed, agent.size, agent.view, speed_mutation = speed_mutation, size_mutation = size_mutation, view_mutation = view_mutation, xlim = xlim , ylim = ylim))     
            agent.food_count = 0
        else:
            print(f"Error: An agent is in the state {agent.state}")
    
    if list_deleted_agents != []:
        for agent in list_deleted_agents:
            list_agents.remove(agent)
    print(f"The total popolation is: {len(list_agents)+len(list_cloned_agents)}")
    new_list = list_agents + list_cloned_agents
    
    return new_list