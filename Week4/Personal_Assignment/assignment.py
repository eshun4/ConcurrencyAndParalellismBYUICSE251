"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: <Your name>

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn

"""

import queue
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

""" This assignment was a bit confusing at first but once I understood what I was doing, I was able to do it.
I have been able to do it to my fullest and i belive I deserve a grade from 93 - 100"""

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, vehicle_queue, empty_queue, full_queue, statistics):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        super().__init__()
        self._vehicle_queue = vehicle_queue
        self._empty_queue = empty_queue
        self._full_queue = full_queue
        self._statistics = statistics
        self._vehicle_count = CARS_TO_PRODUCE


    def run(self):
        for i in range(self._vehicle_count ):
            # TODO Add you code here
            """create a car place the car on the queue signal the dealer that there is a car on the queue"""
            self._empty_queue.acquire()
            car = Car()
            self._vehicle_queue.put(car)
            self._full_queue.release()
            
        # signal the dealer that there there are not more cars

        


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, vehicle_queue, empty_queue, full_queue, statistics):
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
        super().__init__()
        self._vehicle_queue = vehicle_queue
        self._empty_queue = empty_queue
        self._full_queue = full_queue
        self._statistics = statistics

    def run(self):
        while True:
            # TODO Add your code here
            """
            take the car from the queue signal the factory that there is an empty slot in the queue"""
            if sum(self._statistics) >= CARS_TO_PRODUCE and self._vehicle_queue.size() == 0:
                break
            self._full_queue.acquire()
            some_car = self._vehicle_queue.get()
            self._statistics[self._vehicle_queue.size()] +=1
            some_car.display()
            # self._vehicle_queue.get()
            self._empty_queue.release()
            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)
    full = threading.Semaphore(0)
    empty = threading.Semaphore(MAX_QUEUE_SIZE)
    
    # TODO Create queue251 
    vehicle_queue= Queue251()
    
    # TODO Create lock(s) ?
    lock = threading.Lock()

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # TODO create your one factory
    factory = Factory(vehicle_queue=vehicle_queue, empty_queue=empty, full_queue=full, statistics=queue_stats,)
    
    # TODO create your one dealership
    dealership = Dealer(vehicle_queue=vehicle_queue, empty_queue=empty, full_queue=full, statistics=queue_stats,)
    log.start_timer()

    # TODO Start factory and dealership
    factory.start()
    dealership.start()

    # TODO Wait for factory and dealership to complete
    dealership.join()
    factory.join()

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()