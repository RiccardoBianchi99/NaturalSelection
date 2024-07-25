import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random as rd
from agents import *

# Food object that can be improved in the future
class food_class:
    def __init__(self, min = 10, max = 90):
        self.x = rd.uniform(min,max)
        self.y = rd.uniform(min,max)

# Distance between an agent and a piece of food
def compute_distance_food(a, f):
    return np.sqrt((a.x_position-f.x)**2 + (a.y_position-f.y)**2)

# Distance between agents
def compute_distance_agents(a1,a2):
    return np.sqrt((a1.x_position - a2.x_position)**2 + (a1.y_position - a2.y_position)**2)

# generate the new day
def create_figure(list_agents,list_food, title, xlim=100,ylim=100):
    fig, ax = plt.subplots()
    x,y = agents_coordinates_from_list(list_agents)
    points_agents, = ax.plot(x, y, marker='o', linestyle='None')
    x,y = food_coordinates_from_list(list_food)
    points_food, =  ax.plot(x,y,marker = 'o', color = "green",linestyle = 'None')
    ax.set_xlim(0, xlim) 
    ax.set_ylim(0, ylim) 
    ax.set_title(f"Avg speed: {title}")
    return points_agents, points_food

# change the position of the agents and update the food left
def update_figure(list_agents,list_food,points_agents,points_food):
    new_x,new_y = agents_coordinates_from_list(list_agents)
    points_agents.set_data(new_x, new_y)
    new_x,new_y = food_coordinates_from_list(list_food)
    points_food.set_data(new_x,new_y)

# make the agents make a step and decide what to do base on the current state of the game
def move_all_agents(list_agents, list_food, delta_time=0.1, step_size = 10):
    count_agents_moving = 0
    for a in list_agents:
        # agents make their move
        count_agents_moving += a.step(delta_time,step_size)
        
        # they check if the food is close to them
        a.look_around(list_food)
        a.eat(list_food)
        # they decide what to do based on this information
        a.decide_state()

    return count_agents_moving

# coordinates of the agents for the image update
def agents_coordinates_from_list(list_agents):
    list_points_x = []
    list_points_y = []
    for agent in list_agents:
        list_points_x.append(agent.x_position)
        list_points_y.append(agent.y_position)
    return list_points_x,list_points_y

# returns the list of positions for the image update
def food_coordinates_from_list(list_food):
    x = []
    y = []
    for food in list_food:
        x.append(food.x)
        y.append(food.y)
    return x,y

# create the food fot the new day
def generate_food(n = 10):
    food_list = []
    for i in range(n):
        new_food = food_class()
        food_list.append(new_food)
    return food_list

if __name__ == "__main__":
    vec = [1,2,2,3,4,5,0.2]
    vec2 = [1,2,2,2,2,2,2]
    vec3 = np.ones(7)
    plt.plot(vec,vec2)
    plt.plot(vec,vec3)
    plt.show()
