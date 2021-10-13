from math import cos
import yaml
import json
from pathlib import Path
from weights import get_distance, distance_weight, time_weight, cost_weight

with open('stationHallmark.json', 'r') as f:
    stationHallmark=json.load(f)
with open('stationGraph.json', 'r') as f:
    stationGraph=json.load(f)

'''
To the neighbor stations in the same line, the center-station should revalue the specific
contents of weights. While to the potential transfer stations to the center-station, it
is need to compute the direct distance and append the legal transfer stations, and revalue
their weights as well.

The first for-loop traverse all the stationGraph(depict connections and weights between
nodes with index). 
The second for-loop traverse all the stationHallmark(depict informationsabout the station
with index). It contents two parts: the former test whether new station belong formed
neighbor stations. If true, refresh weights and mark it to 'continue'. The latter test 
whether new station short enough to be a transfer station. If true, append the new station
with weights.

                    ***stationHallmark***
                { stationIndex : [ stationName, gcj02, wgs84, lineName, lineType ] }
                { "2" : [ 大钟寺, [116.345139, 39.96612], [116.33895, 39.965266], 13, bus ] }
 
                                        ***stationGraph***
                { stationIndex : [ neighbor_stationIndex, distance_weight, time_weight, cost_weight ] }
                {"1": [["2", "w1", "w2", "w3"], 
                       ["1", 0.0, 1.0, 0.01], 
                       ["357", 0.7088378430614288, 13.540214976643721, 1.0], 
                       ["3155", 0.5463313524157696, 12.172666896575539, 0.0], 
                       ["3217", 0.5463313524157696, 12.172666896575539, 0.0]
                      ]}

'''

def weight_build():
    for index_center, center in stationGraph.items():
        for index_new, hallmark in stationHallmark.items():
            pass_hallmark = False
            # for neighbors in center:  #whether new station belong formed neighbor stations
            #     if index_new == neighbors[0]:
            #         pass_hallmark = True
            #         neighbors[1] = distance_weight(index_center, index_new)
            #         neighbors[2] = time_weight(index_center, index_new)
            #         neighbors[3] = cost_weight(index_center, index_new)
            #         break
            if index_new in center.keys():
                pass_hallmark = True
                center[index_new][0]=distance_weight(index_center, index_new)
                center[index_new][1]=time_weight(index_center, index_new)
                center[index_new][2]=cost_weight(index_center, index_new)
            if pass_hallmark:
                continue
            
            if index_new == index_center:
                continue

            long_center, lat_center = stationHallmark[index_center][2]
            long_new, lat_new = hallmark[2]
            if get_distance(long_center, lat_center, long_new, lat_new) < 0.6:
                center[index_new] = []
                center[index_new].append(distance_weight(index_center, index_new))
                center[index_new].append(time_weight(index_center, index_new))
                center[index_new].append(cost_weight(index_center, index_new))

    with open('stationHallmark.json', 'w') as f:
        json.dump(stationHallmark,f)

    with open('stationGraph.json', 'w') as f:
        json.dump(stationGraph, f)    




if __name__=='__main__':
    weight_build()