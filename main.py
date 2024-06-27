import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from agents import *
from map import *


list_agents = create_list_agents(n = 5)

for i in range(5):
    list_food = generate_food(n = 20)

    frame_agents,frame_food = create_figure(list_agents,list_food)

    agents_moving = 1

    while agents_moving != 0:

        plt.pause(0.01)
        agents_moving = move_all_agents(list_agents, list_food, delta_time=0.1)

        update_figure(list_agents,list_food,frame_agents,frame_food)
    plt.pause(1)
    clear_stage(list_agents)
    plt.show()

for i,p in enumerate(list_agents):
    print(f"Agent number {i}")
    p.print_agent()

