"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: <Add name here>

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

My strategy will be that when there is a fork in the road, the program will
create threads to determine the best route.
Majority of the lists,(meaning  all the lists but one of them), 
will return an empty list. Anyone that return an empty array(list) it will
add it to the path and move on.


Why would it work?

I think it would work because most of the maze will still be checked 
even though the path
wouldnt have to be as long as what's happening now. 

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


def solve_path(maze, start_point, color, path_found, lock):
    """Took this function from assignment09-p1.py and made some changes to it. """
    #To include the start thread in the thread_count
    global thread_count
    
    #Create a list of threads we are going to use
    threads = list()
    (startRow,startCol) = start_point

    #With a while loop we have to loop through till the end
    while True:
        #checks to see if no more moves can be made
        if not maze.can_move_here(startRow,startCol) or path_found[0]:
            #Then we join all the threads at this point
            join_threads = list([i for i in threads])
            for i in join_threads:
                i.join() 
            return

        #Move with a lock anytime ther's one
        with lock:
            maze.move(startRow,startCol, color)
        #Now we check for all the possible moves that can be made
        moves = maze.get_possible_moves(startRow,startCol)
        #If there are no more moves
        if len(moves) == 0:
            #If we find the end
            if not maze.at_end(startRow,startCol):
                #Then we join all the threads at this point
                join_threads = list([i for i in threads])
                for i in join_threads:
                    i.join() 
                return
                #Inidcate that the path_found is True
            path_found[0] = True
        #If the current position hits a fork
        else:
            if len(moves) > 1:
                new_threads = list()
                colr = get_color()
                #Here it creates all threads for all moves that can happen
                for i in range(len(moves) - 1):
                    #Update thread count
                    thread_count+=1
                    #Notice how the target function recursively calls itself
                    new_threads.append(threading.Thread(target = solve_path, args =
                        (maze, moves[i],colr , path_found, lock))) 
                # Add the threads to our threads list
                threads.extend(new_threads)

                #Start the threads
                for thread in new_threads:
                    thread.start() 
                (startRow, startCol) = moves[-1]
            else:
                (startRow, startCol) = moves[0]



def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """

    #To include the start thread in the thread_count
    global thread_count

    #Instead of a bool, a list is more efficient since it carries its value over all threads
    path_found = list([False])

    #Start pos
    start_pos = maze.get_start_pos()

    #Color
    color = get_color()

    #Lock
    lock = threading.Lock()
    
    #This initializes the thread that starts the maze
    start_thread = threading.Thread(target = solve_path,
        args = (maze, start_pos, color, path_found, lock))
    
    #List of Threads
    threads = list([start_thread])
    thread_count+=1

    #Start/Join
    for i  in threads:
        i.start()
    for i in threads:
        i.join()
    


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()