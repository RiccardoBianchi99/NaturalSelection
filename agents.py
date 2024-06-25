import numpy as np
import random as rd

class agent:
    energy = 100 # energy of each agent is fixed
    curvature = 0.05 # rotation of the random movement
    state = "Search"
    orientation = 0
    view = 5
    food = 0

    def __init__(self, speed = 10.0, x = 50.0, y = 0.0,direction = np.pi / 2):
        self.speed = float(speed) # speed of this particular agent
        self.x_position = float(x) # position of the agent
        self.y_position = float(y) 
        self.direction = float(direction) # direction in radiants

    def change_direction(self):
        if self.state == "Search":
            self.direction += self.curvature * self.orientation

            coin_flip = rd.uniform(0,1)
            if coin_flip < float(1/5) and self.orientation > -1:
                self.orientation -= 1
            elif coin_flip > float(4/5) and self.orientation < 1:
                self.orientation += 1  

            if self.x_position == 0.0:
                self.direction = 0.0
            elif self.x_position == 100.0:
                self.direction = np.pi
            if self.y_position == 0.0:
                self.direction = np.pi/2
            elif self.y_position == 100.0:
                self.direction = np.pi*3/2 
    
    def 

    def print_agent(self):
        print(f"Velocity = {self.speed};\nPosition = [{self.x_position},{self.y_position}]\n")  
                

