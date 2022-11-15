"""This is from the Udemy course on Parallelism and Concurrency"""

import time
import threading
from Thread_CLasses.sum_of_workers_class import Sum_of_Squares
from Thread_CLasses.sleep_class import Sleepy_Timey


def main():
    sum_time = time.time()
   
    all_threads = []
    for i in range(6):
        highest_val = ((i + 1) * (1000000))
        sumOfSquares = Sum_of_Squares(n=highest_val)
        # sum_of_squares(highest_val)
       
        # thread= threading.Thread(target=sum_of_squares, args =(highest_val,))
        # thread.start()
        all_threads.append(sumOfSquares)
        
        for t in range(len(all_threads)):
            all_threads[t].join()
        
    print(f"Calculating time it took for sum of squares: {round(time.time() - sum_time, 1)}")
    
    sleep_time = time.time()
    for i in range(6):
        sleepWorker = Sleepy_Timey(seconds=i)
        # time_sleep(i)
        # thread = threading.Thread(target=time_sleep, args=(i,))
        # thread.start()
        all_threads.append(sleepWorker)
        for t in range(len(all_threads)):
            all_threads[t].join()
    
    print(f"Calculating time it took to sleep: {round(time.time() - sleep_time, 1)}")
    


if __name__ == "__main__":
    main()
    