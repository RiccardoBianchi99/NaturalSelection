import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from agents import *
from map import *


p1 = agent()
p2 = agent(5,0.0,60.0,0.0)

list_agents = [p1,p2]

p1.print_agent()
p2.print_agent()

list_food = generate_food( n = 9)

frame = create_fig(list_agents,list_food)

for i in range(100):
    plt.pause(0.1)
    move_all(list_agents,delta_time=0.1)
    update_fig(list_agents,frame)
plt.show()