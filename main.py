import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from agents import *
from map import *


def run_simulation( epocs = 10,starting_agents = 10, food_created = 30, map_base = 100, map_side = 100,
                   show_animation = True, show_graphs = True, speed_mutation = True, size_mutation = True, 
                   view_mutation = True):
    list_agents = create_list_agents(n = starting_agents, xlim = map_base, ylim = map_side)
    number_of_agents_chronology = [10]
    avg_speed_chronology = [1]
    avg_view_chronology = [1]
    avg_size_chronology = [1]

    for i in range(epocs):
        list_food = generate_food(n = food_created, xlim = map_base, ylim = map_side)

        # obtain the list of hunters and prays for each agent!!!
        if show_animation:
            frame_agents,frame_food = create_figure(list_agents,list_food,compute_avg_speed(list_agents), xlim = map_base, ylim = map_side)

        agents_moving = 1

        while agents_moving != 0:

            agents_moving = move_all_agents(list_agents, list_food, delta_time=0.1)

            if show_animation:
                plt.pause(0.001)
                update_figure(list_agents,list_food,frame_agents,frame_food)

        list_agents = clear_stage(list_agents, speed_mutation = speed_mutation, size_mutation = size_mutation, view_mutation = view_mutation, xlim = map_base, ylim = map_side)
        
        if show_animation:
            plt.pause(0.5)
            update_figure(list_agents,list_food,frame_agents,frame_food)
            plt.close()
        
        avg_speed_chronology.append(compute_avg_speed(list_agents))
        avg_view_chronology.append(compute_avg_view(list_agents))
        avg_size_chronology.append(compute_avg_size(list_agents))
        number_of_agents_chronology.append(len(list_agents))

    x_axis = [i for i in range(len(number_of_agents_chronology))]

    if show_graphs:
        fig, axs = plt.subplots(2,2)
        fig.suptitle('Behaviour of the population and avg speed')
        graphs = [
            (axs[0][0], number_of_agents_chronology, "Total Population"),
            (axs[0][1], avg_speed_chronology, "Avg Speed"),
            (axs[1][0], avg_view_chronology, "Avg View"),
            (axs[1][1], avg_size_chronology, "Avg Size"),
        ]

        for i, (ax, y,title) in enumerate(graphs):
            ax.set(title=title)
            ax.plot(x_axis, y, "k")
        plt.show()


if __name__ == "__main__":
    run_simulation(epocs = 20, starting_agents = 50, food_created = 200, map_base = 200, 
                   map_side = 200, show_animation = False)