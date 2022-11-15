"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: <Add name here>

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included

"""
import math
from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
MIN_MOVES=1



# TODO add any functions

def solve_path(maze, pos=None):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """
    # TODO start add code here
    #This updates the current position
    path = list()
    if pos == None:
        #This is where the game starts at position (0,0)
        (rowPath, colPath) = (0,0)
    else:
        (rowPath, colPath) = pos
    
    #This returns the locations for its next moves
    moves = maze.get_possible_moves(rowPath, colPath)
    
    #checks to see if we are at the end of the path then return the path    
    if len(moves) < MIN_MOVES:
        if maze.at_end(rowPath, colPath):
            my_paths = list([(rowPath,colPath)])
            return my_paths
        
    for (rowMaze, rowCol) in moves:
        #This moves to any of the possible locations
        maze.move(rowMaze,rowCol,COLOR)
        #This recursively calls for the possible paths
        possible_paths = solve_path(maze, (rowMaze,rowCol) )
        #This is the base case for the recursion to take place
        if len(possible_paths) != 0:
            #This creates the path
            paths = list([(rowPath,colPath)]) 
            #The extend method appends the whole list passed in it
            path.extend(possible_paths)
            return paths
        else:
            #For the purpose of turning all the dead ends grey in color
            maze.restore(rowMaze,rowCol)
            
    return path 


def get_path(log, filename):
    """ Do not change this function """

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

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

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()