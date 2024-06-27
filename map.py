import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random as rd
from agents import *

class foods:
    def __init__(self, min = 10, max = 90):
        self.x = rd.uniform(min,max)
        self.y = rd.uniform(min,max)

def compute_distance(a, f):
    return np.sqrt((a.x_position-f.x)**2 + (a.y_position-f.y)**2)
    
def food_coordinates(list_food):
    x = []
    y = []
    for food in list_food:
        x.append(food.x)
        y.append(food.y)
    return x,y
 
def create_fig(list_agents,list_food,xlim=100,ylim=100):
    fig, ax = plt.subplots()
    x,y = agents_coordinates(list_agents)
    points_agents, = ax.plot(x, y, marker='o', linestyle='None')
    x,y = food_coordinates(list_food)
    points_food, =  ax.plot(x,y,marker = 'o', color = "green",linestyle = 'None')
    ax.set_xlim(0, xlim) 
    ax.set_ylim(0, ylim) 
    return points_agents, points_food

def update_fig(list_agents,list_food,points_agents,points_food):
    new_x,new_y = agents_coordinates(list_agents)
    points_agents.set_data(new_x, new_y)
    new_x,new_y = food_coordinates(list_food)
    points_food.set_data(new_x,new_y)

def move_all(list_agents, list_food, delta_time=0.1, step_size = 10):
    count_agents_moving = 0
    for a in list_agents:
        if a.state != "Wait" and a.state != "Dead":

            a.change_direction()

            a.x_position += np.cos(a.direction)*delta_time*a.speed*step_size
            a.y_position += np.sin(a.direction)*delta_time*a.speed*step_size

            a.reduce_energy()
            
            count_agents_moving += 1

        # change with environment constrains

        if a.x_position > 100.0:
            a.x_position = 100.0
        elif a.x_position < 0.0:
            a.x_position = 0.0

        if a.y_position > 100.0:
            a.y_position = 100.0
        elif a.y_position < 0.0:
            a.y_position = 0.0

        a.is_food_close(list_food)
        a.decide()

    return count_agents_moving

def agents_coordinates(list_agents):
    list_points_x = []
    list_points_y = []
    for agent in list_agents:
        list_points_x.append(agent.x_position)
        list_points_y.append(agent.y_position)
    return list_points_x,list_points_y

def generate_food(n = 10):
    food_list = []
    for i in range(n):
        new_food = foods()
        food_list.append(new_food)
    return food_list

if __name__ == "__main__":
    vec = [1,2,3,4,5,0.2]
    min_pos = vec.index(min(vec))
    print(vec[min_pos])
