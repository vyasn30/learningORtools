from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time
import math
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
from sklearn.neighbors import DistanceMetric

def calculateDistance(coor1, coor2):
  return math.sqrt((coor1.x-coor2.x)**2 + (coor1.y-coor2.y)**2)



class Coors:
  def __init__(self, latitude, longitude):
    self.latitude = latitude
    self.longitude = longitude

class TimingWindow:
  def __init__(self, startTime, endTime):
    self.startTime =  startTime
    self.endTime = endTime
    
  

class Node:
  def __init__(self, coors, timingWindow=None):
    self.timingWindow = timingWindow
    self.coors = coors
    self.id = id(self)


class Network:
  def __init__(self, depotNode, numVehicles, nodes = None):
    self.nodes = []
    self.depot = depotNode
    self.numVehicles = numVehicles
    print(self.numVehicles)

  def addNode(self, coors):
    newNode = Node(coors)
    self.nodes.append(newNode)
    
  

class DataModel:
  def __init__(self, network):
    self.data = {}
    self.network = network
    self.data["num_vehicles"] = self.network.numVehicles
    self.data["depot"] = self.network.depot
 
 


  def calculateDistanceMatrix(self):
    nodeCoorList =[[np.radians(node.coors.latitude), np.radians(node.coors.longitude)] for node in network.nodes]
    

    metric = DistanceMetric.get_metric("haversine")
    self.data["distance_matrix"] =  metric.pairwise(nodeCoorList)*6373

      
     


  def getData(self):
    self.calculateDistanceMatrix()
    return self.data
  
  


class vrpWrap:
  def __init__(self, data):
    self.data = data
    self.manager = pywrapcp.RoutingIndexManager(len(data["distance_matrix"]), data["num_vehicles"], data["depot"])
    self.routingManager = pywrapcp.RoutingModel(self.manager)
    self.transit_callback_index = None 
    self.solution = None

  def addDistanceDimension(self):
    self.routingManager.AddDimension(
        self.transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        "Distance"
      )
    
    distance_dimension = self.routingManager.GetDimensionOrDie("Distance")
    distance_dimension.SetGlobalSpanCostCoefficient(100)



  def distanceCallback(self, fromIndex, toIndex):
    fromNode = self.manager.IndexToNode(fromIndex)
    toNode = self.manager.IndexToNode(toIndex)
    return self.data['distance_matrix'][fromNode][toNode]

  def solve(self):
    self.transit_callback_index = self.routingManager.RegisterTransitCallback(self.distanceCallback)

    self.routingManager.SetArcCostEvaluatorOfAllVehicles(self.transit_callback_index)
    
    self.addDistanceDimension()
    
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    self.solution = self.routingManager.SolveWithParameters(search_parameters)

    return self.solution
  

  def print_solution(self):
    """Prints solution on console."""
    print(f'Objective: {self.solution.ObjectiveValue()}')
    max_route_distance = 0
    for vehicle_id in range(self.data['num_vehicles']):
        index = self.routingManager.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not self.routingManager.IsEnd(index):
            plan_output += ' {} -> '.format(self.manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(self.routingManager.NextVar(index))
            route_distance += self.routingManager.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(self.manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))





if __name__ == '__main__':
  nodes = []
  coors = [Coors(40.748817, -73.985428),Coors(40.743057, -73.972162)
           ,Coors(40.748359, -73.990814),Coors(40.743823, -73.995250)
           ,Coors(40.754181, -73.989855), Coors(40.754181, -73.989340)
           , Coors(40.754599, -73.994061), Coors(40.739551, -73.988505)
           , Coors(40.736550, -73.979024), Coors(40.755834, -73.983573)           ]



 
  network =  Network(1,1)

  for coor in coors:
    network.addNode(coor)    


  print(DataModel(network).getData())



  vrp = vrpWrap(DataModel(network).getData())
  solution = vrp.solve()
  print(solution)
  print(vrp.routingManager.GetArcCostForVehicle(0, 1, 0))
  print(vrp.print_solution())
