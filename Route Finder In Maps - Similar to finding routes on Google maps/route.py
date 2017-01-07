# -*- coding: utf-8 -*-
# route.py
# Sagar Shah, September 2016

# Formulation of search problem:
# The problem is built into a graph with the nodes as cities and road segments as edges.
# Now we have to search a path from the start city to end city based on the additional information given by the user.

# State space: All list of cities and junctions constitute the total state space.
# Successor function: Cities and junctions connected to a particular city/junction are the successors
# of that city/junction.
# Edge weights: Depending on the type of routing option, the edge weights could either be the distance, time,
# segment(weight of 1) or scenic(weight of highway distance of a road)

# Heuristic:
# Heuristic function is only used in A*.
# Segment and Distance heuristic – Calculate the haversine distance between the current state and goal state.
# This is admissible because the haversine distance will give the minimum distance between the two states given that a
# straightline road(curve) exists between the two states.
# Time: Since time = distance/speed,take the min distance possible and max speed possible to guarantee an underestimate.
# Since dataset has max speed limit as 65, 65 is used as the speed limit.
# Scenic: Here we check a possible outgoing routes and if any of them is scenic, it will return 0,
# else if all are highways then it will take the minimum of the available highway distances.
# This is admissible because if there is at least one outgoing scenic route there is a possibility that
# future all roads to the destination would be scenic and thus the heuristics is accurate at 0.
# If all are highways, then we know that no matter what the minimum value added now to the highway distance
# would be the minimum of the available highways to take.
#
# How the algorithm works:
# BFS: Keep traversing the nodes in BFS order and print when destination is found.
# DFS: Keep traversing the nodes in DFS order and print when destination is found.
# IDS: Keep traversing the nodes in IDS manner, increasing the depth by 1 for every iteration
# and print when destination is found.
# A*: Implemented A* using the heuristics as defined above.
#
# Assumptions/simplifications:
# Since latitude and longitude of junctions are not given, we have calculated them by using the formula:
# Summation of |total_of_connecting_segments – length_of_each_connecting_segment|  /total_of_connecting_segments
# Answers:
# 1) A* seems to work best since it selects the next node to visit by taking the best available option.
# 2) A* seems to work the fastest because since it selects the best available option, it reaches the destination faster.
# 3) IDS uses the least amount of memory
# 4) Refer above for heuristic functions.
# 5) Tete_Jaune_Cache,_British_Columbia is the farthest city from Bloomington,_Indiana. (The code for this is commented out at the bottom)
#


import heapq
import sys
import time
from math import radians, cos, sin, asin, sqrt

startCity = sys.argv[1]
endCity = sys.argv[2]
routingOption = sys.argv[3]
routingAlgorithm = sys.argv[4]


cityMapping = {}
# print sys.getrecursionlimit()
class City:
    name = None
    latitude = None
    longitude = None
    depth = 0

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)

class RoadSegment:
    firstCity = ""
    secondCity = ""
    length = None
    speedLimit = None
    nameOfHighway = None
    time = None
    category = None
    highwayDistance = 0
    segmentLength = 1

    def __init__(self,first_city,second_city,length,speed_limit,name_of_highway):
        self.firstCity = first_city
        self.secondCity = second_city
        self.length = int(length)
        self.speedLimit = int(speed_limit)
        self.nameOfHighway = name_of_highway
        self.time = self.length*1.0/self.speedLimit if self.speedLimit > 0 else self.length*1.0/25  #Set speed limit as 25 as it is minimum speed limit in the dataet
        self.category = 'highway' if self.speedLimit >= 55 else 'scenic'
        self.highwayDistance = self.length if self.category == 'highway' else 0

citiesList = []
noOfCities = 0;
with open('city-gps.txt') as f:
    for line in f:
        each_city = line.split()
        cityMapping[each_city[0]] = noOfCities
        noOfCities += 1
        citiesList.append(City(each_city[0],each_city[1],each_city[2]))

# print noOfCities
roadSegmentsList = []
with open('road-segments.txt') as f:
    for line in f:
        each_road = line.split()
        if not each_road[3].isdigit():
            each_road.append(each_road[3]);
            each_road[3] = 0
        if len(each_road) == 4:
            each_road.append('DummyRoadName')
        roadSegmentsList.append(RoadSegment(each_road[0],each_road[1],each_road[2],each_road[3],each_road[4]))
        roadSegmentsList.append(RoadSegment(each_road[1], each_road[0], each_road[2], each_road[3], each_road[4]))

# for x in roadSegments:
#     print x.name_of_highway

class Map:
    visited = [None]*noOfCities
    adj = [None]*noOfCities
    cities = []

    def __init__(self,cities):
        self.cities = cities
        for i in range(0,noOfCities):
            self.adj[i] = []
            self.visited[i] = 0

    def addEdge(self,rs):
        try:
            self.adj[cityMapping.get(rs.firstCity)].append(rs)
        except:
            global noOfCities
            citiesList.append(City(rs.firstCity,0,0))    #update latitude and longitude for this case
            cityMapping[rs.firstCity] = noOfCities
            noOfCities += 1
            self.adj.append([])
            self.visited.append(0)
            # print noOfCities
            self.adj[cityMapping.get(rs.firstCity)].append(rs)


    # def clearVisited(self):
    #     for i in range(0,noOfCities):
    #         self.visited[i] = 0

    # def Bfs(self,startCity, endCity, routingOption):
    #     q = Queue.Queue(maxsize=0)
    #     q.put(startCity)
    #     # distance = 0
    #     # distanceArray = [0]*noOfCities
    #     # tempDistanceArray = [0]*noOfCities
    #
    #     while not q.empty():
    #         node = q.get()
    #         if self.visited[cityMapping[node]] == 1:
    #             # if node == endCity:
    #             #     tempDistanceArray[cityMapping[node]] =
    #             continue
    #
    #         # if node!=endCity and (routingOption == "distance" or routingOption== "segments"):
    #         #     distanceArray = tempDistanceArray
    #         #     tempDistanceArray = [0] * noOfCities
    #         print node, " "
    #         self.visited[cityMapping[node]] = 1
    #         if node == endCity and routingOption == "segments":
    #             break
    #
    #         neighbours = self.adj[cityMapping[node]]
    #         for temp in neighbours:
    #             # if temp.firstCity == node:
    #             #     sourceCity = temp.firstCity
    #             #     destinationCity = temp.secondCity
    #             # else:
    #             #     sourceCity = temp.secondCity
    #             #     destinationCity = temp.firstCity
    #             # if self.visited[cityMapping[destinationCity]] == 0:
    #             #     tempDistanceArray[cityMapping[destinationCity]] = distanceArray[cityMapping[sourceCity]] + temp.length
    #             if self.visited[cityMapping[temp.secondCity]] == 0:
    #                 q.put(temp.secondCity)
    #
    #     self.clearVisited()

    # def BfsDfs(self,startCity, endCity, routingOption, routingAlgorithm, maxDepth):
    #     if routingAlgorithm == "Bfs":
    #         index = 0
    #     else:
    #         index = -1
    #
    #     depth = 0
    #
    #     for c in citiesList:
    #         c.depth = 0
    #
    #     path = [None]*noOfCities
    #
    #     distance = [sys.maxint]*noOfCities
    #     distance[cityMapping[startCity]] = 0
    #
    #     visited = [0]*noOfCities
    #
    #     visited[cityMapping[startCity]] = 1
    #     # currentCityNo = (0, cityMapping[startCity])
    #
    #     fringe = []
    #     fringe.append(cityMapping[startCity])
    #
    #     while len(fringe) > 0:
    #         neighbours = self.adj[fringe.pop(index)]
    #         for n in neighbours:
    #             if visited[cityMapping[n.secondCity]] == 0:
    #                 citiesList[cityMapping[n.secondCity]].depth = citiesList[cityMapping[n.firstCity]].depth + 1
    #
    #         for temp in neighbours:
    #             # citiesList[cityMapping[temp.secondCity]].depth = depth
    #             # if temp[1] > maxDepth:
    #             #     print "Max depth reached. Depth= ", temp[1], "Max depth", maxDepth
    #             #     return False
    #             # if citiesList[cityMapping[temp.secondCity]].depth == 95:
    #             #     for f in fringe:
    #             #         try:
    #             #             print citiesList[f].name, citiesList[f].depth
    #             #         except:
    #             #             print f
    #             #     raw_input(int)
    #             if citiesList[cityMapping[temp.secondCity]].depth > maxDepth:
    #                 print "Max depth reached. Depth= ",citiesList[cityMapping[temp.secondCity]].depth , "Max depth", maxDepth
    #                 continue
    #                 # return False
    #             if visited[cityMapping[temp.secondCity]] == 0:
    #                 # allExplored = False
    #                 visited[cityMapping[temp.secondCity]] = 1
    #                 path[cityMapping[temp.secondCity]] = temp.firstCity
    #                 # print temp.secondCity
    #                 if cityMapping[temp.secondCity] == cityMapping[endCity]:
    #                     # print "Depth before printing final path ",depth
    #                     self.printPath(path, startCity, endCity)
    #                     return True
    #
    #                 fringe.append(cityMapping[temp.secondCity])
    #         # if allExplored:
    #         #         depth -= 1
    #         # else:
    #         #     depth += 1
    #     return False

    def BfsDfs(self,startCity, endCity, routingOption, routingAlgorithm, maxDepth):
        if routingAlgorithm == "Bfs":
            index = 0
        else:
            index = -1

        depth = 0

        for c in citiesList:
            c.depth = 0

        path = [None]*noOfCities

        distance = [sys.maxint]*noOfCities
        distance[cityMapping[startCity]] = 0

        visited = [0]*noOfCities

        visited[cityMapping[startCity]] = 1
        # currentCityNo = (0, cityMapping[startCity])

        fringe = []
        fringe.append((cityMapping[startCity],citiesList[cityMapping[startCity]].depth))

        while len(fringe) > 0:
            tuple = fringe.pop(index)
            node = tuple[0]
            level = tuple[1]
            neighbours = self.adj[node]
            for n in neighbours:
                if visited[cityMapping[n.secondCity]] == 0:
                    citiesList[cityMapping[n.secondCity]].depth = level + 1
                else:
                    if citiesList[cityMapping[n.secondCity]].depth > level +1:
                        path[cityMapping[n.secondCity]] = node
                        citiesList[cityMapping[n.secondCity]].depth = level + 1


            for temp in neighbours:
                # citiesList[cityMapping[temp.secondCity]].depth = depth
                # if temp[1] > maxDepth:
                #     print "Max depth reached. Depth= ", temp[1], "Max depth", maxDepth
                #     return False
                # if citiesList[cityMapping[temp.secondCity]].depth == 95:
                #     for f in fringe:
                #         try:
                #             print citiesList[f].name, citiesList[f].depth
                #         except:
                #             print f
                #     raw_input(int)
                if citiesList[cityMapping[temp.secondCity]].depth > maxDepth:
                    # print "Max depth reached. Depth= ", citiesList[cityMapping[temp.secondCity]].depth, "Max depth", maxDepth
                    continue

                if visited[cityMapping[temp.secondCity]] == 0:
                    # allExplored = False
                    visited[cityMapping[temp.secondCity]] = 1
                    path[cityMapping[temp.secondCity]] = temp.firstCity
                    # print temp.secondCity
                    if cityMapping[temp.secondCity] == cityMapping[endCity]:
                        # print "Depth before printing final path ",depth
                        self.printPath(path, startCity, endCity)
                        return True

                    fringe.append((cityMapping[temp.secondCity],citiesList[cityMapping[temp.secondCity]].depth ))
                # else:
                #     if citiesList[cityMapping[temp.secondCity]].depth > level:
                #         fringe.append((cityMapping[temp.secondCity], level))

            # if allExplored:
            #         depth -= 1
            # else:
            #     depth += 1
        return False

    # def DfsDjikstra(self,startCity, endCity, routingOption):  #Referred online for Djikstra's algorithm concept. Code implemented without referencing any pseudocode.
    #     path = [None]*noOfCities
    #
    #     distance = [sys.maxint]*noOfCities
    #     distance[cityMapping[startCity]] = 0
    #
    #     visited = set()
    #
    #     currentCityNo = self.getMinDistance(distance,visited)
    #     visited.add(currentCityNo[1])
    #     fringe = []
    #     fringe.append(cityMapping[startCity])
    #     while (currentCityNo[1] != cityMapping[endCity]):
    #         # while i < no:
    #         # node = fringe.pop()
    #         # neighbours = self.adj[node]
    #         for temp in self.adj[fringe.pop()]:
    #             # visited.add(temp.firstCity)
    #             if routingOption == 'segments':
    #                 minify = temp.segmentLength
    #             if routingOption == 'distance':
    #                 minify = temp.length
    #             if routingOption == 'time':
    #                 minify = temp.time
    #             if routingOption == 'scenic':
    #                 minify = temp.highwayDistance
    #
    #             if(cityMapping[temp.secondCity] not in visited):
    #                 print "lhs",distance[cityMapping[temp.secondCity]]
    #                 print "rhs", distance[currentCityNo[1]] + minify
    #                 if distance[cityMapping[temp.secondCity]] > distance[currentCityNo[1]] + minify:
    #                     distance[cityMapping[temp.secondCity]] = distance[currentCityNo[1]] + minify
    #                     print "path ",temp.firstCity
    #                     path[cityMapping[temp.secondCity]] = temp.firstCity
    #             fringe.append(cityMapping[temp.secondCity])
    #             # x = time.clock()
    #         currentCityNo = self.getMinDistance(distance,visited)
    #         # print time.clock() - x , "seconds"
    #         visited.add(currentCityNo[1])
    #
    #     print path
    #     print distance
    #     self.printPath(path,distance,startCity,endCity)


    # def BfsDfs(self,startCity, endCity, routingOption):  #Referred online for Djikstra's algorithm concept. Code implemented without referencing any pseudocode.
    #     path = [None]*noOfCities
    #
    #     distance = [sys.maxint]*noOfCities
    #     distance[cityMapping[startCity]] = 0
    #
    #     visited = set()
    #
    #     currentCityNo = self.getMinDistance(distance,visited)
    #     visited.add(currentCityNo[1])
    #     fringe = []
    #     fringe.append(cityMapping[startCity])
    #     while (currentCityNo[1] != cityMapping[endCity]):
    #         # while i < no:
    #         # node = fringe.pop()
    #         # neighbours = self.adj[node]
    #         for temp in self.adj[fringe.pop()]:
    #             # visited.add(temp.firstCity)
    #             if routingOption == 'segments':
    #                 minify = temp.segmentLength
    #             if routingOption == 'distance':
    #                 minify = temp.length
    #             if routingOption == 'time':
    #                 minify = temp.time
    #             if routingOption == 'scenic':
    #                 minify = temp.highwayDistance
    #
    #             if(cityMapping[temp.secondCity] not in visited):
    #                 print "lhs",distance[cityMapping[temp.secondCity]]
    #                 print "rhs", distance[currentCityNo[1]] + minify
    #                 if distance[cityMapping[temp.secondCity]] > distance[currentCityNo[1]] + minify:
    #                     distance[cityMapping[temp.secondCity]] = distance[currentCityNo[1]] + minify
    #                     print "path ",temp.firstCity
    #                     path[cityMapping[temp.secondCity]] = temp.firstCity
    #             fringe.append(cityMapping[temp.secondCity])
    #             # x = time.clock()
    #         currentCityNo = self.getMinDistance(distance,visited)
    #         # print time.clock() - x , "seconds"
    #         visited.add(currentCityNo[1])
    #
    #     print path
    #     print distance
    #     self.printPath(path,distance,startCity,endCity)

    # def BfsDjikstra(self,startCity, endCity, routingOption):  #Referred online for Djikstra's algorithm concept. Code implemented without referencing any pseudocode.
    #     path = [None]*noOfCities
    #
    #     distance = [sys.maxint]*noOfCities
    #     distance[cityMapping[startCity]] = 0
    #
    #     visited = set()
    #
    #     currentCityNo = self.getMinDistance(distance,visited)
    #     visited.add(currentCityNo[1])
    #     while (currentCityNo[1] != cityMapping[endCity]):
    #         # while i < no:
    #         neighbours = self.adj[currentCityNo[1]]
    #         for temp in neighbours:
    #             if routingOption == 'segments':
    #                 minify = temp.segmentLength
    #             if routingOption == 'distance':
    #                 minify = temp.length
    #             if routingOption == 'time':
    #                 minify = temp.time
    #             if routingOption == 'scenic':
    #                 minify = temp.highwayDistance
    #
    #             if(cityMapping[temp.secondCity] not in visited):
    #                 if distance[cityMapping[temp.secondCity]] > distance[currentCityNo[1]] + minify:
    #                     distance[cityMapping[temp.secondCity]] = distance[currentCityNo[1]] + minify
    #                     path[cityMapping[temp.secondCity]] = temp.firstCity
    #         currentCityNo = self.getMinDistance(distance,visited)
    #         visited.add(currentCityNo[1])
    #
    #     print path
    #     print distance
    #     self.printPath(path,distance,startCity,endCity)

    def printPath(self,path,startCity,endCity):
        finalPath = []
        ec = endCity
        distanceTravelled = 0
        timeTaken = 0.0
        instructions = []
        while(endCity != startCity):
            finalPath.append(endCity)
            # print "A", endCity
            # print "B", cityMapping[endCity]
            neighbours = self.adj[cityMapping[endCity]]
            for temp in neighbours:
                if temp.secondCity == path[cityMapping[endCity]]:
                    distanceTravelled += temp.length
                    timeTaken += temp.time
                    instructions.append(temp)

                    break

            endCity = path[cityMapping[endCity]]


        finalPath.append(startCity)

        while instructions:
            road = instructions.pop()
            print road.secondCity,"to",road.firstCity,"is",road.length,"miles. Take",road.nameOfHighway,"for",round(road.time,2),"hours"

        print distanceTravelled, timeTaken,
        # print len(finalPath),
        while finalPath:
            print finalPath.pop(),

        return distanceTravelled,startCity,ec  #ony used for qt 5


    # def getMinDistance(self,distance,visited):
    #     min = sys.maxint
    #     # print distance
    #     for i in set(range(0,len(distance))) - visited:
    #         # if i not in visited:
    #         #     min = distance[i]
    #         #     node = i
    #         if distance[i] <= min:
    #             min = distance[i]
    #             node = i
    #
    #     return min, node

    # def Dfs(self,startCity, endCity, routingOption, depth):
    #     path = []
    #     distance = [sys.maxint] * noOfCities
    #     distance[cityMapping[startCity]] = 0
    #     flag = False
    #
    #     tuple = self.DfsHelper(startCity, endCity, routingOption, flag, path, distance,depth)
    #     if tuple[0] == True and tuple[1] == 'found':
    #         print tuple[2]
    #     self.clearVisited()
    #     return tuple
    #
    # def DfsHelper(self,node, endCity, routingOption, flag, path, distance,depth):
    #     self.visited[cityMapping[node]] = 1
    #
    #     path.append(node)
    #     print node
    #     if node == endCity:
    #         return True, 'found', path
    #     if depth <= 0:
    #         return True, 'not found', path
    #
    #     neighbours = self.adj[cityMapping[node]]
    #     # min = sys.maxint
    #     # for s in neighbours:
    #     #     if self.visited[cityMapping[s.secondCity]] == 0 and distance[cityMapping[node]] + s.length < min:
    #     #         min = distance[cityMapping[node]] + s.length
    #
    #     if routingOption == 'distance':
    #         neighbours.sort(key=lambda x: x.length)   # Code snippet for sorting from http://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-in-python-based-on-an-attribute-of-the-objects
    #     if routingOption == 'time':
    #         neighbours.sort(key=lambda x: x.time)
    #     if routingOption == 'scenic':
    #         neighbours.sort(key=lambda x: x.highwayDistance)
    #
    #     for s in neighbours:
    #         if self.visited[cityMapping[s.secondCity]] == 0:
    #             tuple = self.DfsHelper(s.secondCity, endCity, routingOption, flag, path, distance, depth -1 )
    #             if tuple is not None and tuple[0]:
    #                 return tuple



    def Ids(self,startCity, endCity, routingOption, routingAlgorithm):
        for i in range(0,len(citiesList)):
            found = self.BfsDfs(startCity,endCity,routingOption,routingAlgorithm,i)
            if found:
                break
    # def BfsScenic(self,startCity, endCity, routingOption):
    #     path = [None] * noOfCities
    #
    #     distance = [sys.maxint] * noOfCities
    #     distance[cityMapping[startCity]] = 0
    #     distanceHighway = [sys.maxint] * noOfCities
    #
    #     visited = set()
    #
    #     currentCityNo = (0,cityMapping[startCity])
    #     visited.add(cityMapping[startCity])
    #
    #     while (currentCityNo[1] != cityMapping[endCity]):
    #     # while i < no:
    #         neighbours = self.adj[currentCityNo[1]]
    #         for temp in neighbours:
    #             if(cityMapping[temp.secondCity] not in visited):
    #                 if distance[cityMapping[temp.secondCity]] > distance[currentCityNo[1]] + temp.length:
    #                     # if temp.category == 'scenic':
    #                     distance[cityMapping[temp.secondCity]] = distance[currentCityNo[1]] + temp.length
    #                     path[cityMapping[temp.secondCity]] = temp.firstCity
    #         currentCityNo = self.getMinDistance(distance,visited)
    #         visited.add(currentCityNo[1])
    #     self.clearVisited()
    #     print path
    #     print distance
    def astar(self,startCity, endCity, routingOption, routingAlgorithm):  #Algorithm used similar to Djikstra's
        if(startCity == endCity):
            return
        fringe = []
        heapq.heappush(fringe,(0,startCity))
        # fringe.put(0,cityMapping[startCity])
        visited = [0] * noOfCities
        path = [None] * noOfCities
        # visited[cityMapping[startCity]] = 1
        # print heapq.heappop(fringe)
        while (len(fringe))>0:
            optimalNode = heapq.heappop(fringe)
            # if visited[cityMapping[optimalNode[1]]] == 1:
            #     continue
            visited[cityMapping[optimalNode[1]]] = 1

            # print temp[1]
            if cityMapping[optimalNode[1]] == cityMapping[endCity]:
                # print "found"
                tuple = self.printPath(path,startCity,endCity)   #qt 5
                return tuple      #qt 5
            for roadSegment in self.adj[cityMapping[optimalNode[1]]]:
                    exists = False
                    if visited[cityMapping[roadSegment.secondCity]] == 0:
                        for node in fringe:
                            if node[1] == roadSegment.secondCity:
                                exists = True
                                if node[0] > optimalNode[0] + roadSegment.length:
                                    priority = optimalNode[0] + roadSegment.length + self.heuristics(roadSegment.secondCity,endCity,routingOption)
                                    currentNode = roadSegment.secondCity
                                    fringe.remove((node[0],roadSegment.secondCity))
                                    heapq.heappush(fringe,(priority,currentNode))
                                    path[cityMapping[roadSegment.secondCity]] = roadSegment.firstCity
                                    heapq.heapify(fringe)
                                    break
                        if not exists:
                            heapq.heappush(fringe, (optimalNode[0] + roadSegment.length + self.heuristics(roadSegment.secondCity,endCity,routingOption), roadSegment.secondCity))
                            path[cityMapping[roadSegment.secondCity]] = roadSegment.firstCity

    def heuristics(self,city1,city2,routingOption):
        # print citiesList[cityMapping[city1]].name,citiesList[cityMapping[city1]].latitude,citiesList[cityMapping[city1]].longitude
        # print citiesList[cityMapping[city2]].name, citiesList[cityMapping[city2]].latitude, citiesList[cityMapping[city2]].longitude
        distance = self.haversine(citiesList[cityMapping[city1]].latitude,citiesList[cityMapping[city1]].longitude,citiesList[cityMapping[city2]].latitude,citiesList[cityMapping[city2]].longitude)
        if routingOption == 'distance':
            return distance
        if routingOption == 'time':
            return distance/65 #took 65 as it is the max speed limit and will thus give the fastest possible time to reach the destination thus guaranteeing an underestimate of heuristcs
        if routingOption == 'scenic':
            neighbours = self.adj[cityMapping[city1]]
            return min(temp.highwayDistance for temp in neighbours)  #http://stackoverflow.com/questions/2622994/python-finding-lowest-integer
        return distance


    #Code snippet to calculate haversine ditance between two places using lat long taken from
    #http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    def haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 3956  # Radius of earth in kilometers. Use 6371 for km
        return c * r

    def updateLatLonOfJunctions(self):
        for city in citiesList:
            if city.latitude == 0:
                neighbours = self.adj[cityMapping[city.name]]
                if  len(neighbours) == 1:
                    city.latitude = citiesList[cityMapping[neighbours[0].secondCity]].latitude
                    city.longitude = citiesList[cityMapping[neighbours[0].secondCity]].longitude
                    return
                totalX =0.0
                totalY=0.0
                for temp in neighbours:
                    totalX += citiesList[cityMapping[temp.secondCity]].latitude
                    totalY += citiesList[cityMapping[temp.secondCity]].longitude
                AvgX = 0.0
                AvgY = 0.0
                tempX = 0.0
                tempY = 0.0
                for temp in neighbours:
                    tempX += totalX - citiesList[cityMapping[temp.secondCity]].latitude
                    tempY += totalY - citiesList[cityMapping[temp.secondCity]].longitude
                AvgX = tempX / len(neighbours)
                AvgY = tempY / len(neighbours)

                # AvgX = float(sum( citiesList[cityMapping[temp.secondCity]].latitude for temp in neighbours ))/len(neighbours)
                # AvgY = float(sum(citiesList[cityMapping[temp.secondCity]].longitude for temp in neighbours)) / len(neighbours)
                city.latitude = AvgX
                city.longitude = AvgY


def buildGraph(roadSegments):
    map = Map(citiesList)
    for rs in roadSegments:
        map.addEdge(rs)

    return map

map2 = buildGraph(roadSegmentsList)
map2.updateLatLonOfJunctions()


if routingAlgorithm == 'Bfs':
    map2.BfsDfs(startCity, endCity, routingOption, "Bfs", sys.maxint)
if routingAlgorithm == 'Dfs':
    map2.BfsDfs(startCity, endCity, routingOption, "Dfs", sys.maxint)
if routingAlgorithm == 'Ids':
    map2.Ids(startCity, endCity, routingOption, "Ids")
if routingAlgorithm == 'astar':
    map2.astar(startCity, endCity, routingOption, "astar")

# map2.BfsDfs("Seattle,_Washington", "Fort_Lauderdale,_Florida", "segments", "Bfs", sys.maxint)
# map2.BfsDfs("Seattle,_Washington", "Fort_Lauderdale,_Florida", "segments", "Dfs", sys.maxint)
# map2.Ids("Seattle,_Washington", "Fort_Lauderdale,_Florida", "segment", "Ids")
# map2.astar("Seattle,_Washington", "Fort_Lauderdale,_Florida", "segments", "astar")

# map2.BfsDfs("Winnemucca,_Nevada", "Amargosa_Valley,_Nevada", "segments", "Bfs", sys.maxint)
# print ""
# print "-----------------------------------------------------------------------------------------------------------------------------"
# map2.Ids("Winnemucca,_Nevada", "Amargosa_Valley,_Nevada", "segment", "Ids")


###########################Qt 5 code##############################################
# max = 0
# finaltuple = None
#
# print map2.haversine(39.165325,-86.5263857,47.6062095,-122.3320708)
#
# candidateCities = []
# for city in citiesList:
#     if not city.name.startswith("Jct"):
#         d = map2.haversine(39.165325, -86.5263857, city.latitude, city.longitude)
#         if d > 6000:
#             candidateCities.append(city)
#
# print len(candidateCities)
# for city in candidateCities:
#     tuple = map2.astar("Bloomington,_Indiana", city.name, "distance", "astar")
#     if tuple is not None and tuple[0] > max:
#         max = tuple[0]
#         finaltuple = tuple
#
# print finaltuple

#Answer: (4369, 'Bloomington,_Indiana', 'Tete_Jaune_Cache,_British_Columbia')

####################################################################################