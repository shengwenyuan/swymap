import json
import math
import yaml
from pathlib import Path
from wgs2km import get_degree_len

root = Path(__file__).resolve().parent
with open(root / 'hyp.yaml', errors='ignore') as f:
    hyp = yaml.safe_load(f)


with open('stationHallmark.json', 'r') as f:
    stationHallmark=json.load(f)


def get_distance(long1, lat1, long2, lat2, direct=True):
    long_degree, lat_degree = get_degree_len(lat1)
    delta_x = long_degree * abs(long1 - long2)  
    delta_y = lat_degree * abs(lat1 - lat2)
    return math.sqrt(delta_x**2 + delta_y**2) if direct else delta_x+delta_y


def distance_weight(stationIndex1, stationIndex2):
    long1, lat1 = stationHallmark[stationIndex1][2]
    long2, lat2 = stationHallmark[stationIndex2][2]
    if stationHallmark[stationIndex1][4] == 'subway':
        if stationHallmark[stationIndex2][4] == 'subway':
            if stationHallmark[stationIndex1][3] != stationHallmark[stationIndex1][3]:#MM-trans
                return hyp['distance_mm_trans']
            else:#MM-go
                return get_distance(long1, lat1, long2, lat2)
        else:#MB-trans
            return get_distance(long1, lat1, long2, lat2, False) + hyp['distance_bm_trans']
    else:
        if stationHallmark[stationIndex2][4] == 'subway':#BM-trans
            return get_distance(long1, lat1, long2, lat2, False) + hyp['distance_bm_trans']
        else:
            if stationHallmark[stationIndex1][3] == stationHallmark[stationIndex2][3]:#BB-go
                return get_distance(long1, lat1, long2, lat2, False)
            else:#BB-trans
                return get_distance(long1, lat1, long2, lat2, False)      
                

def time_weight(stationIndex1, stationIndex2):
    long1, lat1 = stationHallmark[stationIndex1][2]
    long2, lat2 = stationHallmark[stationIndex2][2]
    if stationHallmark[stationIndex1][4] == 'subway':
        if stationHallmark[stationIndex2][4] == 'subway':
            if stationHallmark[stationIndex1][3] != stationHallmark[stationIndex1][3]:#MM-trans
                return hyp['time_mm_trans']
            else:#MM-go
                return get_distance(long1, lat1, long2, lat2) / hyp['velocity_metro'] + hyp['time_mm_go']
        else:#MB-trans
            return get_distance(long1, lat1, long2, lat2, False) / hyp['velocity_feet'] + hyp['time_mb_trans']
    else:
        if stationHallmark[stationIndex2][4] == 'subway':#BM-trans
            return get_distance(long1, lat1, long2, lat2, False) / hyp['velocity_feet'] + hyp['time_bm_trans']
        else:
            if stationHallmark[stationIndex1][3] == stationHallmark[stationIndex2][3]:#BB-go
                return get_distance(long1, lat1, long2, lat2, False) / hyp['velocity_bus'] + hyp['time_bb_go']
            else:#BB-trans
                return get_distance(long1, lat1, long2, lat2, False) / hyp['velocity_feet'] + hyp['time_bb_trans']


def cost_weight(stationIndex1, stationIndex2):
    # long1, lat1 = stationHallmark[stationIndex1][2]
    # long2, lat2 = stationHallmark[stationIndex2][2]
    if stationHallmark[stationIndex1][4] == 'subway':
        if stationHallmark[stationIndex2][4] == 'subway':
            if stationHallmark[stationIndex1][3] != stationHallmark[stationIndex1][3]:#MM-trans
                return hyp['cost_mm_trans']
            else:#MM-go
                return hyp['cost_mm_go']
        else:#MB-trans
            return hyp['cost_mb_trans']
    else:
        if stationHallmark[stationIndex2][4] == 'subway':#BM-trans
            return hyp['cost_bm_trans']
        else:
            if stationHallmark[stationIndex1][3] == stationHallmark[stationIndex2][3]:#BB-go
                return hyp['cost_bb_go']
            else:#BB-trans
                return hyp['cost_bb_trans']



# def future_weight(stationIndex1, stationIndex2):
#     long1, lat1 = stationHallmark[stationIndex1][2]
#     long2, lat2 = stationHallmark[stationIndex2][2]
#     if stationHallmark[stationIndex1][4] == 'subway':
#         if stationHallmark[stationIndex2][4] == 'subway':
#             if stationHallmark[stationIndex1][3] != stationHallmark[stationIndex1][3]:#MM-trans
#                 return 
#             else:#MM-go
#                 return 
#         else:#MB-trans
#             return 
#     else:
#         if stationHallmark[stationIndex2][4] == 'subway':#BM-trans
#             return 
#         else:
#             if stationHallmark[stationIndex1][3] == stationHallmark[stationIndex2][3]:#BB-go
#                 return
#             else:#BB-trans
#                 return

if __name__=='__main__':
    # stationHallmark = stationHallmark[0]
    # print(stationHallmark['1'])
    print(stationHallmark['1'], stationHallmark['2'])
    print(distance_weight('1','2'))
    print(time_weight('1','2'))
    print(cost_weight('1','2'))
