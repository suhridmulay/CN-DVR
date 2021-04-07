import threading
from typing import NewType

class Router:
    """
    Encapcsulating the behaviour of a single router
    Steps
    1. Calculate distance to all clients
    2. Broadcast table to all neighbours
    3. When recieving a table, recalibrate distance vectors

    Behaviour
    init - Initialise new router
    incorporate - incorporates given distance vector from given sender into current router
    broadcast - send own routing table to neighbours
    """

    def __init__(self, id: str):
        # ID for individual routers
        self.id = id
        # Records of distances to other nodes
        # Formate: { client: distance }
        self.distance_vector: dict = {}
        self.distance_vector[self.id] = float(0)
        # Lock for distance vector
        self.dv_lock = threading.Lock()
        # List of adjacent routers
        self.adjacents: list = []

    def incorporate(self, sender: 'Router', dv: dict):
        # If communication looks to be from non neighbouring nodes
        if sender not in self.adjacents:
            # Raise an error
            raise Exception('Recieved distance vector from invalid router')
        else:
            # Lock own distance vector
            self.dv_lock.acquire()
            # Calculate new distances via the connected node
            base_dist = self.distance_vector[sender.id]
            for key in dv.keys():
                # If new distance is less than old one
                if base_dist + dv[key] < self.distance_vector[key]:
                    # Update the old one
                    self.distance_vector[key] = base_dist + dv[key]
            # Release the dv lock
            self.dv_lock.release()

    # Broadcast self's distance vector to all others
    def broadcast(self):
        # Acquire lock to own distance vector
        self.dv_lock.acquire()
        # Send the distance vector to neigbours
        for router in self.adjacents:
            router.incorporate(self, self.distance_vector)
        # Release lock on own distance vector
        self.dv_lock.release()
    
    def lockdv(self): self.dv_lock.acquire()
    def releasedv(self): self.dv_lock.release()

class Netowrk:
    """
    Network class
    Abstraction for networks

    Members
    network_name,
    router_list

    Behaviour
    init - create a new network
    add_router - add a router to the network
    join - joins two routers with a connection
    sim_init - creates the starting condition for simulation
    sim_tick - simulates one time step of the bellman ford algorithm
    """

    # Creates a network
    def __init__(self, network_name: str):
        self.routers: list = []
        self.name = network_name

    # Adds a router to the netowrk
    def add_router(self, r: 'Router'):
        # append only if router not already present
        if r not in self.routers:
            self.routers.append(r)
        # Otherwise present warning
        else:
            print('[WARNING] Router already added to network')
        # Set distance vectors to infinity
        router: 'Router'
        for router in self.routers:
            if router != r:
                router.distance_vector[r.id] = float('Inf')
                r.distance_vector[router.id] = float('Inf')
        # Set self distance to 0
        r.distance_vector[r.id] = 0

    # Creates a connection between two routers with said weight
    def join(self, r1: 'Router', r2: 'Router', wt: float):
        if r1 not in self.routers or r2 not in self.routers:
            print('[ERROR] add routers to network before joining')
        if r2 not in r1.adjacents and r1 not in r2.adjacents:
            r1.adjacents.append(r2)
            r2.adjacents.append(r1)
        r1.distance_vector[r2.id] = wt
        r2.distance_vector[r1.id] = wt

    def sim_tick(self):
        router: 'Router'
        for router in self.routers:
            router.broadcast();

n = Netowrk('New Network')
A = Router('A')
B = Router('B')
C = Router('C')

n.add_router(A)
n.add_router(B)
n.add_router(C)

n.join(A, B, 5)
n.join(A, C, 2)

n.sim_tick()

print(A.distance_vector)
print(B.distance_vector)
print(C.distance_vector)