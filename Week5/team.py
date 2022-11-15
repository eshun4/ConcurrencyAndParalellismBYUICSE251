"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau
Purpose: Check for prime values
Instructions:
- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it
"""
import time
import threading
import multiprocessing as mp
import random

#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 1

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

#TODO create read_thread function

def read_thread(filename, q):
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            q.put(int(line))
            

    
# TODO create prime_process function
def prime_process(q, list):
    n = q.get()
    while True:
        if n == "NO_MORE_NUMBERS":
            break
        if is_prime(n):
            print(n)
            list.append(n)
    # for i in q.get():
    #     if is_prime[q[i]] == True:
    #         list.append(q)
        

def create_data_txt(filename):
    with open(filename, 'w') as f:
        for _ in range(1000):
            f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'

    # Once the data file is created, you can comment out this line
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    shared_queue = mp.Queue()
    # TODO create reading thread
    t = threading.Thread(target= read_thread, args=(filename, shared_queue) )

    # TODO create prime processes
    primes = mp.Manager().list()
    processes = [mp.Process(target= prime_process, args=(i, primes)) for i in range(PRIME_PROCESS_COUNT)]
    # TODO Start them all
    
    t.start()
    for i in processes:
        i.start()
        
    # TODO wait for them to complete
    t.join()
    for i in processes:
        i.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()