"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: <Your name here>
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change

from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# Global variables
COMPLETE_MESSAGE = "COMPLETED!";

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, pipe_conn, marbles, delay ):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.pipe_conn = pipe_conn
        self.marbles = marbles       
        self.delay = delay

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for i in range(self.marbles):
            rand_var = random.choice(self.colors)
            # print(rand_var)
            self.pipe_conn.send(rand_var)
            time.sleep(self.delay)
        self.pipe_conn.send(COMPLETE_MESSAGE)
        self.pipe_conn.close()


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self,fromCreat, toAssembler, bagNumber, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.fromCreat = fromCreat
        self.toAssembler = toAssembler
        self.bagNumber = bagNumber
        self.delay = delay
        
    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        # number_of_bags =[]
        while True:
            bag = Bag()
            for i in range(self.bagNumber):
                marble = self.fromCreat.recv()
                if marble == COMPLETE_MESSAGE:
                    self.toAssembler.send(COMPLETE_MESSAGE)
                    self.fromCreat.close()
                    self.toAssembler.close()
                    return
                bag.add(marble)
                # time.sleep(self.delay)
                # else:
            self.toAssembler.send(bag)
            time.sleep(self.delay)
        
                    # return
            # number_of_bags.append(bag)


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, thisBag, wrapper_receiver, delay, number_of_gifts_created):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.thisBag = thisBag
        self.wrapper_receiver = wrapper_receiver
        self.delay = delay
        self.number_of_gifts_created = number_of_gifts_created

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            bag = self.thisBag.recv()
            if bag == COMPLETE_MESSAGE:
                break
            gift = Gift(random.choice(self.marble_names),bag.items)
            time.sleep(self.delay)
            self.number_of_gifts_created.value += 1
            # number_of_gifts.append(gift)
            self.wrapper_receiver.send(gift)
        self.wrapper_receiver.send(COMPLETE_MESSAGE)
        self.thisBag.close()
        self.wrapper_receiver.close()


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, from_assembler,file_name, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.from_assembler = from_assembler
        self.file_name = file_name
        self.delay = delay
        
    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.file_name, "w") as f:
            while True:
                gift = self.from_assembler.recv()
                if gift == COMPLETE_MESSAGE:
                    break
                f.write(str(gift))
                f.write("\n")
                time.sleep(self.delay)
        f.close()
        self.from_assembler.close()
        

def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}') 
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    parent_creator , child_creator = mp.Pipe()
    parent_bagger, child_bagger = mp.Pipe()
    parent_assembler,child_assembler = mp.Pipe()
    
    # TODO create variable to be used to count the number of gifts
    number_of_gifts_created = mp.Value('i', 0)
    
    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    creator_process = Marble_Creator(parent_creator, settings[MARBLE_COUNT], settings[CREATOR_DELAY])
    bagger_process = Bagger(child_creator, parent_bagger, settings[BAG_COUNT], settings[BAGGER_DELAY])
    assembler_process = Assembler(child_bagger, parent_assembler, settings[ASSEMBLER_DELAY], number_of_gifts_created)
    wrapper_process = Wrapper(child_assembler, BOXES_FILENAME, settings[WRAPPER_DELAY])

    log.write('Starting the processes')
    # TODO add code here
    processes_list = [creator_process,bagger_process, assembler_process, wrapper_process ]
    for i in processes_list:
        i.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    for i in processes_list:
        i.join()
        
    display_final_boxes(BOXES_FILENAME, log)

    # TODO Log the number of gifts created.
    log.write(f"Number of gifts - {number_of_gifts_created.value}")



if __name__ == '__main__':
    main()
