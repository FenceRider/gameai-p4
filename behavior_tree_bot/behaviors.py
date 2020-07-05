import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import logging
import functools 
from heapq import heappop, heappush
from math import ceil, sqrt
from collections import namedtuple

def attack_weakest_enemy_planet(state):

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)



def getCenter(planets):
    #calculate center of mass
    pos = functools.reduce(\
    lambda a,b: [{"top":a[0]["top"] + (b.x*b.num_ships), "bottom":a[0]["bottom"] + b.num_ships},\
                 {"top":a[1]["top"] + (b.y*b.num_ships), "bottom":a[1]["bottom"] + b.num_ships}],\
                 planets, [{"top":0, "bottom":0},{"top":0, "bottom":0}])
    pos[0] = pos[0]["top"]/pos[0]["bottom"]
    pos[1] = pos[1]["top"]/pos[1]["bottom"]
    
    
    #pos[0] = pos[0] / len(planets)
    #pos[1] = pos[1] / len(planets) 
    return pos[0], pos[1]
def distance(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return int(ceil(sqrt(dx * dx + dy * dy)))

"""
    predicts a planets pop after all ships have been settled
    also takes into account the growth rate
    returns all planets
"""
def settled_predictPop(state):
    #make both fleets and planets mutable
    fleets = state.enemy_fleets() + state.my_fleets()
    
    fleets = [f._asdict() for f in fleets]

    planets_list = state.not_my_planets() + state.my_planets()
    
    planets = {}
    #key each planet by its id
    for p in planets_list:
        p = p._asdict()
        planets[p['ID']] = p
        #logging.info('\n' + str(planets[p['ID']]['x']))
        
    #planets = [p._asdict() for p in planets]
    
    while len(fleets) != 0:
        for p in planets.items():
            p = p[1] #PYTHON! plz give me debugger
            if p['owner'] != 0:
                p['num_ships'] = p['num_ships'] + p['growth_rate']
        for f in fleets:
            f['turns_remaining'] = f['turns_remaining'] - 1
            if f['turns_remaining'] <= 0:
                fleets.remove(f)
                p = planets[f['destination_planet']]
                if p['owner'] == f['owner']:
                    p['num_ships'] += f['num_ships']
                else:
                    p['num_ships'] -= f['num_ships']
                    if p['num_ships'] < 0:
                        p['owner'] = ['f.owner']
                        p['num_ships'] = abs(p['num_ships'])
                        logging.info(p['num_ships'])
    return planets
        
def toNametuple(dict_data):
    return namedtuple(
        "X", dict_data.keys()
    )(*tuple(map(lambda x: x if not isinstance(x, dict) else toNametuple(x), dict_data.values())))

def popAtArrival(planet, turns):
    return planet.num_ships + (turns * planet.growth_rate)


def imperial(state):
    
    planets = settled_predictPop(state)
    
    #get the predicts population of planets, then sort them based on that
    my_planets = []
    #for p in planets.items():
    #    logging.info('\n' + str(p[1]["ID"]))
    #    if p[1]['owner'] == 1: #wtf is python!
    #        my_planets.append(toNametuple(p[1]))

    #my_planets = [toNametuple(p[1]) for p in planets.items() if p[1]['owner'] == 1]
    my_planets = state.my_planets()
    my_planets.sort(key=lambda p : p.num_ships)
    other_planets = [toNametuple(p[1]) for p in planets.items() if p[1]['owner'] != 1] # state.not_my_planets()#state.neutral_planets()
    
    my_center = getCenter(my_planets)
    
    #sorted distance
    #neutral_planets.sort(key=lambda p : distance(getCenter(my_planets), (p.x,p.y) ))
    #sorted lowest pop
    #other_planets.sort(key=lambda p : p.num_ships )
    #combined value
    other_planets.sort(key=lambda p : popAtArrival(p, distance(getCenter(my_planets), (p.x,p.y))/3) * distance(getCenter(my_planets), (p.x,p.y) ))
    
    #logging.info('\n' + my_planets)

    if len(my_planets) == 0 or len(other_planets) == 0:
        return False
    else:
        for n in other_planets:
            if len(other_planets) == 0:
                break
            
            total = n.num_ships
            while len(my_planets) > 0 and total > 0:
                p = my_planets.pop()
                if p.num_ships < 50:
                    break
                x = p.num_ships - 10 
                
                if x >0:
                    total = total - x
                    issue_order(state, p.ID, n.ID, p.num_ships-10)

    return True
    
    pass

def cluster(state):

    closest_distance_to_enemy = []
    closest_distance_to_savages = []
    # (1) Determine Imperial Border / Planets closest to the enemy
    border_planets = state.my_planets()
    enemy = state.enemy_planets()
    
    for planet in border_planets:
        lowest_distance =  float('inf')
        temp_distance = 0
        for destination in enemy:
            temp_distance = state.distance(planet, destination)
            if temp_distance < lowest_distance:
                lowest_distance = temp_distance
        heappush(closest_distance_to_enemy,(lowest_distance, planet))



    # (2) Find closest planets inhabited by ignorant savages.
    closest_planets = state.neutral_planets()

    for planet in border_planets:
        lowest_distance =  float('inf')
        temp_distance = 0
        for destination in closest_planets:
            temp_distance = state.distance(planet, destination)
            if temp_distance < lowest_distance:
                lowest_distance = temp_distance
        heappush(closest_distance_to_savages,(lowest_distance, planet))

    

    # (3) Target Savages for Enlightenment in the Imperial Faith
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not closest_planets or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) The Inquisition sends its regards to the ignorant savages
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    pass

def Annihilate(state):
    
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

    
    pass

def reinforce_friends(state):
    
    planets = state.my_planets()
    if(len(planets)>=2):
        issue_order(state, planets[0].ID, planets[1].ID, 1)
   
    pass

