import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from agents import *
from map import *


list_agents = create_list_agents(n = 10)
number_of_agents_chronology = [10]
avg_speed_chronology = [1]

for i in range(20):
    list_food = generate_food(n = 30)

    frame_agents,frame_food = create_figure(list_agents,list_food,compute_avg_speed(list_agents))

    agents_moving = 1

    while agents_moving != 0:

        plt.pause(0.001)
        agents_moving = move_all_agents(list_agents, list_food, delta_time=0.1)

        update_figure(list_agents,list_food,frame_agents,frame_food)

    plt.pause(0.5)
    list_agents = clear_stage(list_agents, speed_mutation = True)
    update_figure(list_agents,list_food,frame_agents,frame_food)
    plt.close()
    avg_speed_chronology.append(compute_avg_speed(list_agents))
    number_of_agents_chronology.append(len(list_agents))

x_axis = [i for i in range(len(number_of_agents_chronology))]

fig, axs = plt.subplots(1,2)
fig.suptitle('Behaviour of the population and avg speed')
axs[0].plot(x_axis,number_of_agents_chronology)
axs[1].plot(x_axis,avg_speed_chronology)
plt.show()
# for i,p in enumerate(list_agents):
#     print(f"Agent number {i}")
#     p.print_agent()

