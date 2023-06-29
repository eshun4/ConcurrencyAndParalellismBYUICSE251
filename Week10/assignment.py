"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  
  
- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:


"""
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

def shared_list_index_location(buffer, start_lock):
    #We will call this function at the index of the shared_list inside the writeBuffer function
    with start_lock:
      return buffer[BUFFER_SIZE]

def writeBuffer(shared_list, start_lock, end_lock, empty, full, items_to_send):
    sent_items = 0
    for i in range(items_to_send):
        
        random_integer = random.randint(0, 255)
        
        #This is to acquire empty semaphore 
        empty.acquire()
        
        shared_list[shared_list_index_location(shared_list, start_lock)] = random_integer
        
        #This lock is needed to release the list
        with start_lock:
            shared_list[BUFFER_SIZE] = (shared_list[BUFFER_SIZE] + 1) % BUFFER_SIZE
        
        #This is to release the full semaphore
        full.release()
        sent_items += 1
        
    #This pointer is needed to sent the pointer to True
    with end_lock:
      shared_list[BUFFER_SIZE + READERS] = True
      
    #Store all the items sent in the items_sent variable declared above
    shared_list[BUFFER_SIZE+3] = sent_items

def reading_complete(buf, start_lock, finish_lock):
    writing_complete = False
    complete = False

    #This updates the writing_complete to the pointer
    with finish_lock:
        writing_complete = buf[BUFFER_SIZE + READERS]
        
    #Check if the buffer has completed reading
    with start_lock:
        complete = buf[BUFFER_SIZE] == buf[BUFFER_SIZE+1]

    return writing_complete and complete

def createPointer(shared_list, empty, full):
    
  #This is to acquire the full semaphore
  full.acquire()

  #This creates a pointer
  pointer = shared_list[shared_list[BUFFER_SIZE + 1]]

  #This updates the pointer
  shared_list[BUFFER_SIZE+1] = (shared_list[BUFFER_SIZE + 1] + 1) % BUFFER_SIZE
  
  #This releases an empty semaphore
  empty.release()
  return pointer
    
def readBuffer(shared_list, start_lock, end_lock, empty, full):
    total = 0
    #This keeps running until we are done reading
    while not reading_complete(shared_list,  start_lock, end_lock):
        createPointer(shared_list, empty, full)
    
         #Now update total to the final number of iterations 
        total += 1
        
     # Store the total
    shared_list[BUFFER_SIZE+4] = total
    
    #Store the total into your list
    shared_list[BUFFER_SIZE + READERS + WRITERS] = total
    

      
def main():
    processes_list = list()
    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    shareableList = smm.ShareableList( [0] *(BUFFER_SIZE + 5))
    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    start_lock = mp.Lock()
    end_lock = mp.Lock()
    empty = mp.Semaphore(10)
    full = mp.Semaphore(0)
    
    # TODO - create reader and writer processes
    reader = mp.Process(target=readBuffer, args=(shareableList, start_lock, end_lock, empty, full))
    writer = mp.Process(target=writeBuffer, args=(shareableList, start_lock, end_lock, empty, full, items_to_send))
    
    processes_list = [reader, writer]
    # TODO - Start the processes and wait for them to finish
    for _ in processes_list:
        _.start()
        
    for _ in processes_list:
        _.join()

    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')
    sent = shareableList[BUFFER_SIZE + 3]
    print(f'{sent} values sent')
    
    received = shareableList[BUFFER_SIZE + 4]
    print(f'{received} values received')
    
    print("\nCompleted!")
    
    smm.shutdown()
    


if __name__ == '__main__':
    main()