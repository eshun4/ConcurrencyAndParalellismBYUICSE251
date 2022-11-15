"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau
Purpose: Retrieve Star Wars details from a server
Instructions:
- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.
The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.
{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.response = dict()
        self.url=url

    def run(self):
        response = requests.get(self.url)
        self.response=response.json()
        global call_count
        call_count += 1

# TODO Add any functions you need here
def getDetails(diction,name):
    return [Request_thread(x) for x in diction[name] ]


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    top = Request_thread(TOP_API_URL) 
    top.start()
    top.join()
    # print_dict(top.response)
    second = Request_thread(top.response["films"] + "6") 
    second.start()
    second.join()

        
    # TODO Retireve Details on film 6
    film = second.response
    #Collecting all the threads before starting them
    thread=[]
    for x in getDetails(film,'characters'):
      thread.append(x)
    char_length = len(thread)  
    for x in getDetails(film,'planets'):
      thread.append(x)
    plan_len = len(thread)
    for x in getDetails(film,'starships'):
      thread.append(x)
    star_len = len(thread)  
    for x in getDetails(film,'vehicles'):
      thread.append(x)
    veh_len = len(thread)
    for x in getDetails(film,'species'):
      thread.append(x)
    spec_len = len(thread)

    #Starting all the threads, joining all the threads
    [x.start() for x in thread]
    [x.join() for x in thread]
 
    #Creating lists of the names
    characters=[x.response['name'] for x in thread[:char_length ]]
    planets=[x.response['name'] for x in thread[char_length :plan_len]]
    starships=[x.response['name'] for x in thread[plan_len:star_len]]
    vehicles=[x.response['name'] for x in thread[star_len:veh_len]]
    species=[x.response['name'] for x in thread[veh_len:spec_len]]

    #Sorting the lists
    characters.sort()
    planets.sort()
    starships.sort()
    vehicles.sort()
    species.sort()


    # TODO Display results
    log.write("----------------------------------------")
    log.write('Title   : {}'.format(film['title']))
    log.write('Director: {}'.format(film['director']))
    log.write('Producer: {}'.format(film['producer']))
    log.write('Released: {}'.format(film['release_date']))

    log.write('')

    log.write("Characters: {}".format(len(characters)))
    log.write(", ".join(characters))
    
    log.write('')

    log.write("Planets: {}".format(len(planets)))
    log.write(", ".join(planets))

    log.write('')

    log.write("Starships: {}".format(len(starships)))
    log.write(", ".join(starships))

    log.write('')

    log.write("Vehicles: {}".format(len(vehicles)))
    log.write(", ".join(vehicles))

    log.write('')

    log.write("Species: {}".format(len(species)))
    log.write(", ".join(species))

    log.write('')
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()