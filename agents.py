import numpy as np
import random as rd
import math
from map import *

class agent:
    energy = 500.0 # energy of each agent is fixed
    curvature = 0.05 # rotation of the random movement
    state = "Search"
    orientation = 0
    food_count = 0
    food_seen = [] # change into a pointer !!!
    direction = 0.0

    def __init__(self, speed = 1.0, x = 50.0, y = 0.0,size = 1.0, view = 1.0):
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
                if compute_distance(self,food) < self.view * 5:
                    self.state = "Found"
                    self.food_seen = food
                    if compute_distance(self,food) < 1.0:
                        self.state = "Search"
                        list_food.remove(self.food_seen)
                        self.food_seen = []
                        self.food_count += 1

                    break
                else:
                    self.state = "Search"
                    self.food_seen = []

    def decide(self):
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
        print(f"Velocity = {self.speed};\nPosition = [{self.x_position},{self.y_position}]")
        print(f"Food count: {self.food_count}")  
        print(f"State: {self.state} \n")

    def reduce_energy(self):
        self.energy -= self.size * self.speed + self.view
