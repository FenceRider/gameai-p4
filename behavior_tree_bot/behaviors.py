import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import logging
import functools 
from heapq import heappop, heappush

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






def imperial(state):

    my_planets = state.my_planets().sort(key=lambda p : p.num_ships, reverse=True)
    neutral_planets = state.neutral_planets().sort(key=lambda p : p.num_ships, reverse = True)
    

    if len(my_planets) == 0 or len(neutral_planets) == 0:
        return False
    else:
        for p in my_planets:
            if len(neutral_planets) == 0:
                break
            current_n = neutral_planets.pop()
            total = p.num_ships
            if total - current_n.num_ships >= 10:
                    issue_order(state, p.ID, current_n.ID, current_n.num_ships)
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

