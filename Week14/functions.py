"""
Course: CSE 251, week 14
File: functions.py
Author: Kofi Junior Eshun

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')


You will lose 10% if you don't detail your part 1 
and part 2 code below

Describe how to speed up part 1

I created all the threads for this part and started them.
Then I recursively called the Request_thread
class in a for loop. However, in order to increase the 
speed I waited for them to join at the end. I was hoping
this will increase the speed greatly. 


Describe how to speed up part 2

I used the same principles above without the recursion though. I created
a queue with a list and used it to implement the logic behing my breadth 
first search algorithm and it worked.


10% Bonus to speed up part 3

<Add your comments here>


"""
from common import *
# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    if not family_id:
        return
    
    if tree.does_family_exist(family_id):
        return
   
    #Retrieve family by id and start and join thread
    print(f'Getting Family: {family_id}')
    requested_fam = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    requested_fam.start()
    requested_fam.join()
    
    #Create New Family Object and add it to the tree
    new_fam = Family(family_id, requested_fam.response)
    tree.add_family(new_fam)
    husband, wife = None, None
    
    #Create array to store list of people
    list_of_people = list()
    
    # Let's get the husband and wife's details starting with the husband
    husband_id = new_fam.husband
    print(f'Getting Husband : {husband_id}')
    husband_thread = Request_thread(f'{TOP_API_URL}/person/{husband_id}')
    list_of_people.append(husband_thread)
    
    #Now let's get the Wife's details
    wife_id = new_fam.wife
    print(f'Getting Wife    : {wife_id}')
    wife_thread = Request_thread(f'{TOP_API_URL}/person/{wife_id}')
    list_of_people.append(wife_thread)
    
    #Now Let's retrive the children too
    print(f'Getting children: {str(new_fam.children)[1:-1]}')
    
    for each_child_id in new_fam.children:
        if not tree.does_person_exist(each_child_id): 
            requested_child = Request_thread(f'{TOP_API_URL}/person/{each_child_id}')
            list_of_people.append(requested_child)
            # requested_child.start()
    for i in list_of_people:
        i.start()   
    for i in list_of_people:
        i.join()
    
    next_gen = list()
    for i in list_of_people:
        person = Person(i.response)
        if not tree.does_person_exist(person.id):
            tree.add_person(person)
            next_gen.append(threading.Thread(target=depth_fs_pedigree, args=(person.parents, tree)))

    for i in next_gen:
        i.start()
    for i in next_gen:
        i.join()
            
    
    
        
        


# -----------------------------------------------------------------------------
def breadth_fs_pedigree(start_id, tree):
    queue = list()
    queue.append(start_id)
    
    while len(queue) > 0:
        fam_thread = list()
        for fam_id in queue:
            if fam_id == None or tree.does_family_exist(fam_id):
                continue
            fam_thread.append((fam_id, Request_thread(f'{TOP_API_URL}/family/{fam_id}')))
        for _, j in fam_thread:
            j.start()
        for _, j in fam_thread:
            j.join() 
        pers_details = list()
        for fam_id, k in fam_thread:
            family = Family(fam_id, k.response)   
            tree.add_family(family)
            if family.husband:
                pers_details.append((family.husband, Request_thread(f'{TOP_API_URL}/person/{family.husband}')))
            if family.wife:
                pers_details.append((family.wife, Request_thread(f'{TOP_API_URL}/person/{family.wife}')))
            for child_id in family.children:
                pers_details.append((child_id, Request_thread(f'{TOP_API_URL}/person/{child_id}')))
        queue = list()
        for _, j in pers_details:
            j.start()
        for _, j in pers_details:
            j.join() 
        
        for _, pers in pers_details:
            person = Person(pers.response)
            if tree.does_person_exist(person.id):
                continue
            tree.add_person(person)
            queue.append(person.parents)



# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_id, tree):
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5

    print('WARNING: BFS (Limit of 5 threads) function not written')

    pass
