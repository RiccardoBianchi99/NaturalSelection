import numpy as np
import random as rd
import math
from map import *

class agent_class:
    energy = 500.0 # energy of each agent is fixed
    curvature = 0.05 # rotation of the random movement
    state = "Search"
    orientation = 0
    food_count = 0
    food_seen = [] 
    direction = 0.0

    def __init__(self, speed = 1.0, x = 50.0, y = 0.0, size = 1.0, view = 1.0):
        self.speed = float(speed) # speed of this particular agent
        self.size = size
        self.view = view
        self.x_position = float(x) # position of the agent
        self.y_position = float(y) 

    def change_direction(self):
        if self.state == "Search":
            self.direction += self.curvature * self.orientation

            coin_flip = rd.uniform(0,1)
            if coin_flip < float(1/5) and self.orientation > -1:
                self.orientation -= 1
            elif coin_flip > float(4/5) and self.orientation < 1:
                self.orientation += 1  


            if np.abs(self.x_position - 0.0) < 1:
                self.direction = 0.0
            elif np.abs(self.x_position - 100.0) < 1:
                self.direction = np.pi

            if np.abs(self.y_position - 0.0) < 1:
                self.direction = np.pi/2
            elif np.abs(self.y_position - 100.0) < 1:
                self.direction = np.pi*3/2 


        elif self.state == "Found":
            self.direction = math.atan2(self.food_seen.y - self.y_position,self.food_seen.x - self.x_position)

        elif self.state == "Home":

            distances = [np.abs(self.x_position-0.0),np.abs(self.x_position-100.0),np.abs(self.y_position-0.0),np.abs(self.y_position-100.0)]
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
    
    def is_food_close(self, list_food):
        if self.state == "Search" or self.state == "Found":
            for i,food in enumerate(list_food):
                if compute_distance_food(self,food) < self.view * 5:
                    self.state = "Found"
                    self.food_seen = food
                    if compute_distance_food(self,food) < 1.0:
                        self.state = "Search"
                        list_food.remove(self.food_seen)
                        self.food_seen = []
                        self.food_count += 1

                    break
                else:
                    self.state = "Search"
                    self.food_seen = []

    def decide_state(self):
        if self.state == "Wait":
            return

        if self.energy < 0:
            self.state = "Dead"
            return

        elif self.food_count > 1:
            self.state = "Home"
            return 
        
        elif self.food_count == 1 and self.energy < 100 and self.state != "Found": # cambiare con una condizione migliore sull'energia
            self.state = "Home"

    def print_agent(self):
        print(f"Speed: {self.speed}; Size: {self.size}; View range: {self.view}")

    def update_energy(self):
        self.energy -= self.size * self.speed + self.view

def compute_avg_speed(list_agents):
    total = 0
    for agent in list_agents:
        total += agent.speed
    return total/len(list_agents)

def create_new_agent(speed = 1, size = 1, view = 1):
    coin_flip = rd.uniform(0,1)
    if coin_flip < 1/4:
        new_agent = agent_class(speed = speed, x = rd.uniform(0.01,99.9), y = 100.0, size = size, view = view)
    elif coin_flip < 2/4:
        new_agent = agent_class(speed = speed, x = 100.0, y = rd.uniform(0.01,99.9), size = size, view = view)
    elif coin_flip < 3/4:
        new_agent = agent_class(speed = speed, x = rd.uniform(0.01,99.9), y = 0.0, size = size, view = view)
    else:
        new_agent = agent_class(speed = speed, x = 0.0, y = rd.uniform(0.01,99.9), size = size, view = view)

    return new_agent

def create_list_agents(n = 10):
    list_agents = []
    for i in range(n):
        list_agents.append(create_new_agent())

    return list_agents

def duplicate_agent_with_mutations(speed, size, view, speed_mutation = True, size_mutation = False, view_mutation = False):

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
        new_agent = agent_class(speed = speed + speed_variation, x = rd.uniform(0.01,99.9), y = 100.0, size = size + size_variation, view = view + view_variation)
    elif coin_flip < 2/4:
        new_agent = agent_class(speed = speed + speed_variation, x = 100.0, y = rd.uniform(0.01,99.9), size = size + size_variation, view = view + view_variation)
    elif coin_flip < 3/4:
        new_agent = agent_class(speed = speed + speed_variation, x = rd.uniform(0.01,99.9), y = 0.0, size = size + size_variation, view = view + view_variation)
    else:
        new_agent = agent_class(speed = speed + speed_variation, x=0.0, y = rd.uniform(0.01,99.9), size = size + size_variation, view = view + view_variation)
    
    return new_agent

def clear_stage(list_agents, speed_mutation = False, size_mutation = False, view_mutation = False):
    
    list_cloned_agents = []
    list_deleted_agents = []
    for agent in list_agents:
        if agent.state == "Dead":
            list_deleted_agents.append(agent)
            continue 
        if agent.state == "Wait" :
            agent.state = "Search"
            agent.energy = 500
            agent.food_seen = []
            if agent.food_count > 1:
                list_cloned_agents.append(duplicate_agent_with_mutations(agent.speed, agent.size, agent.view, speed_mutation = speed_mutation, size_mutation = size_mutation, view_mutation = view_mutation))     
            agent.food_count = 0
        else:
            print(f"Error: An agent is in the state {agent.state}")
    
    if list_deleted_agents != []:
        for agent in list_deleted_agents:
            list_agents.remove(agent)
    print(f"The total popolation is: {len(list_agents)+len(list_cloned_agents)}")
    new_list = list_agents + list_cloned_agents
    
    return new_list