class Router:
   def __init__(self, id: str, net: 'Network'):
      # Create ID for a new router
      self.id: str = id
      self.network: 'Network' = net

      # List of adjacent routers
      self.adjacents: list = list()
      # Distance vector
      self.distance_vector: dict = dict()
      # Routing table
      # Entry format {dest: fwd_to}
      self.routing_table: dict = dict()

   # Creates a one way connection entry in router
   def connect(self, r: 'Router', wt: float):
      if (r in self.adjacents):
         print('[WARNING] router already connected, updating link weight')
         self.distance_vector[r.id] = wt
      else:
         self.adjacents.append(r)
         self.routing_table[r.id] = r
         self.distance_vector[r.id] = wt




class Network:
   def __init__(self, network_name: str):
      self.name: str = network_name
      self.router_list: list = list()
      self.size: int = 0

   def add_router(self, rt: 'Router'):
      if rt in self.router_list:
         print('[WARNING] Unable to add entry, router already exists')
      else:
         self.router_list.append(rt)
         self.size += 1
