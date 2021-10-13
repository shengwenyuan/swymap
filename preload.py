import yaml
import os
import random
import time
import glob
import json
from pathlib import Path
from coordinate import gcj02towgs84

def loading():
    stationHallmark = {}
    stationGraph = {}
    stationIndex = 0
    root = Path(__file__).resolve().parent

    subway=(root/'data'/'subwayLines/').glob('line*')
    bus=(root/'data'/'busLines/').glob('line*')
    s1=[i for i in bus]
    s2=[i for i in subway]
    s=s1+s2

    for i, file in enumerate(s):
        # if i>=1: break
        with open(file, 'r') as oneline:
            ln = str(file.name).strip('line地铁.csv')
            tmp = -1
            for i, station in enumerate(oneline):
                '''
                                    ***stationHallmark***
                { stationIndex : [ stationName, gcj02, wgs84, lineName, lineType ] }
                { 2 : [ 大钟寺, [116.345139, 39.96612], [116.33895, 39.965266], 13, bus ] }
                '''
                
                if ((file.name == 'line地铁2号线') | (file.name == 'line地铁10号线')) \
                  & (i == 0):
                    tmp = stationIndex
                stationHallmark[stationIndex] = []
                s = station.strip().split(',')
                stationHallmark[stationIndex].append(s[0])
                stationHallmark[stationIndex].append([float(s[1]), float(s[2])])
                wgs84 = gcj02towgs84(float(s[1]), float(s[2]))
                stationHallmark[stationIndex].append(wgs84)
                stationHallmark[stationIndex].append(ln)
                if file.name.endswith('.csv'): 
                    stationHallmark[stationIndex].append('bus')
                else:   stationHallmark[stationIndex].append('subway')
                #**********station hallmark done**********

                '''
                                        ***stationGraph***
                { stationIndex : { neighbor_stationIndex : [distance_weight, time_weight, cost_weight] } 
                                 { neighbor_stationIndex : [distance_weight, time_weight, cost_weight] }
                                 { neighbor_stationIndex : [distance_weight, time_weight, cost_weight] } }

                '''
                if i == 0:
                    stationGraph[stationIndex] = {}
                    stationGraph[stationIndex][str(stationIndex+1)] = ['w1', 'w2', 'w3']
                else:
                    stationGraph[stationIndex] = {}
                    stationGraph[stationIndex][str(stationIndex-1)] = ['w1', 'w2', 'w3']
                    stationGraph[stationIndex][str(stationIndex+1)] = ['w1', 'w2', 'w3']
                
                stationIndex += 1

            stationIndex -= 1
            del(stationGraph[stationIndex][str(stationIndex+1)])
            if tmp > 0: #环线特殊连接
                stationGraph[stationIndex][str(tmp)] = ['t1', 'w2', 'w3']
                stationGraph[tmp][str(stationIndex)] = ['t1', 'w2', 'w3']
                    


    with open('stationHallmark.json', 'w') as f:
        json.dump(stationHallmark,f)

    with open('stationGraph.json', 'w') as f:
        json.dump(stationGraph, f)


    # with open('stationHallmark.json', 'r') as f:
    #     a=json.load(f)
    #     for item in a.items():
    #         print(item)

    # with open('stationGraph.json', 'r') as f:
    #     a=json.load(f)
    #     for item in a.items():
    #         print(item)


loading()