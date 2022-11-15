"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: Kofi Junior Eshun
Purpose: Process Task Files
Instructions:  See I-Learn
TODO
I exchanged the pool size for each of the pools till i actually got the right size for each. 
And then I compared the run-times of each changes to the run-time of the others. Then, I came to a conclusion on the 
pool size that is optimal for the fastest run-time.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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
 
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    return is_prime(value)

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt') as f:
        if word in f.read():
            f.close()
            return f"{word} Found"
    f.close()
    return f"{word} not found *****"

def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return text.upper()

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    return sum([i for i in range(start_value, end_value+1)])

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    json = response.json()
    return json['name']

def add_task_upper(result):
    return result_upper.append(result)

def add_result_primes(result):
    return result_primes.append(result)

def add_result_words(result):
    return result_words.append(result)

def add_result_sums(result):
    return result_sums.append(result)

def add_result_names(result):
    return result_names.append(result)

def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    prime_pool = mp.Pool(4)
    word_pool = mp.Pool(4)
    upper_pool = mp.Pool(4)
    sum_pool = mp.Pool(4)
    name_pool = mp.Pool(4)
    
    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            prime_pool.apply_async(task_prime, args = (task['value'], ), callback = add_result_primes)
        elif task_type == TYPE_WORD:
            word_pool.apply_async(task_word, args = (task['word'], ), callback = add_result_words)
        elif task_type == TYPE_UPPER:
            upper_pool.apply_async(task_upper, args = (task['text'], ), callback = add_task_upper)
        elif task_type == TYPE_SUM:
            sum_pool.apply_async(task_sum, args = (task['start'], task['end'] ), callback = add_result_sums)
        elif task_type == TYPE_NAME:
            name_pool.apply_async(task_name, args = (task['url'],), callback = add_result_names)
        else:
            log.write(f'Error: unknown task type {task_type}')

    # TODO start and wait pools
    prime_pool.close()
    word_pool.close()
    upper_pool.close()
    sum_pool.close()
    name_pool.close()
    
    prime_pool.join()
    word_pool.join()
    upper_pool.join()
    sum_pool.join()
    name_pool.join()

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()