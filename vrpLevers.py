from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time
import math
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix


def calculateDistance(coor1, coor2):
  return math.sqrt((coor1.x-coor2.x)**2 + (coor1.y-coor2.y)**2)

class Coors:
  def __init__(self, x, y):
    self.x = x
    self.y = y


class Node:
  def __init__(self, coors):
    self.coors = coors
  
class DataModel:
  def __init__(self, nodes):
    self.data = {}
    self.nodes = nodes 


  def calculateDistanceMatrix(self):
    nodeCoorList =[[node.coors.x, node.coors.y] for node in nodes]
    return distance_matrix(nodeCoorList, nodeCoorList)

  

if __name__ == '__main__':
  nodes = []

  coor1 = Coors(5,7)
  coor2 = Coors(7,3)
  coor3 = Coors(8,2)

  node1 = Node(coor1)
  node2 = Node(coor2)
  node3 = Node(coor3)

  nodes.append(node1)
  nodes.append(node2)
  nodes.append(node3)

  print(type(nodes))


  print(DataModel(nodes).calculateDistanceMatrix())

