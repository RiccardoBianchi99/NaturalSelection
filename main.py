import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from agents import *
from map import *


p1 = agent()
p2 = agent(1.2,0.0,60.0)
p3 = agent(1.5, 100.0,60.0)

list_agents = [p1,p2,p3]

list_food = generate_food( n = 20)

frame_agents,frame_food = create_fig(list_agents,list_food)

agents_moving = 1
while agents_moving != 0:

    plt.pause(0.1)
    agents_moving = move_all(list_agents, list_food, delta_time=0.1)
    update_fig(list_agents,list_food,frame_agents,frame_food)

plt.show()

for i,p in enumerate(list_agents):
    print(f"Agent number {i}")
    p.print_agent()