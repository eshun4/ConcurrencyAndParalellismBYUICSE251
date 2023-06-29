"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))

def cleaner(id, start_time,lock_clean, clean_counter):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    timer = time.time() - start_time
    while (timer) < TIME:
        cleaner_waiting()
        with lock_clean:
            print(STARTING_CLEANING_MESSAGE)
            clean_counter.value = clean_counter.value + 1
            cleaner_cleaning(id)
            print(STOPPING_CLEANING_MESSAGE)

def guest(id, guest_lock, start_time, lock_clean, party_counter, at_party_count):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    timer = time.time() - start_time
    while (timer) < TIME:
        guest_waiting()
        with guest_lock:
            at_party_count.value = at_party_count.value + 1
            if at_party_count.value == 1:
                lock_clean.acquire()
                print(STARTING_PARTY_MESSAGE)
                party_counter.value= party_counter.value + 1
        
        guest_partying(id)
        with guest_lock:
            at_party_count.value = at_party_count.value - 1
            if at_party_count.value == 0:
                print(STOPPING_PARTY_MESSAGE)
                lock_clean.release()

def main():
    # Start time of the running of the program. 
    start_time = time.time()
    # TODO - add any variables, data structures, processes you need
    #Cleaners lock
    lock_clean = mp.Manager().Lock()
    
    #Guests lock
    guest_lock = mp.Manager().Lock()
    
    # Number of cleaners
    clean_counter = mp.Manager().Value('i', 0)
    
    # Number of party guests
    party_counter = mp.Manager().Value('i', 0)
    
    # Number of people at the 
    at_party_count = mp.Manager().Value('i', 0)
    
    # TODO - add any arguments to cleaner() and guest() that you need
    cleaners, guests = list(), list()
    for i in range(CLEANING_STAFF):
        cleaners +=[mp.Process(target=cleaner, args=(i+1,start_time,lock_clean, clean_counter ))]
    
    for i in range(HOTEL_GUESTS):
        guests += [mp.Process(target=guest, args=(i+1, guest_lock, start_time, lock_clean, party_counter, at_party_count))]
    
    # Start all the processes
    for g in guests:
        g.start()
    for c in cleaners:
        c.start()
    
    
    #Join all the processes
    for g in guests:
        g.join()
    for c in cleaners:
        c.join()
    
    
    # Results
    print(f'Room was cleaned {clean_counter.value} times, there were {party_counter.value} parties')


if __name__ == '__main__':
    main()

