import json
Inf = float('inf')

with open('stationGraph.json', 'r') as f:
    stationGraph=json.load(f)

'''
adj: stationGraph   src: startStation   dst: finalStation   n: total station number
dist: distance from startStation to the nowStation
'''

def dijstra(srcStation='2737', w_choice=0):
    distance = {}
    book = {}
    for i in stationGraph.keys():
        book[i] = False
        distance[i] = [Inf, srcStation]
    distance[srcStation][0] = 0
    u = srcStation
    n = len(stationGraph)

    for _ in range(n-1):  #loop n-1 times
        book[u] = True
        next_u, min_road = None, Inf
        for index in stationGraph.keys():
            if index in stationGraph[u].keys():
                weight = stationGraph[u][index][w_choice]
            else:   
                weight = Inf
                continue
            
            if (not book[index]) and ((distance[u][0]+weight) < distance[index][0]):
                distance[index][0] = distance[u][0] + weight
                distance[index][1] = u
        
        for k, v in book.items():
            if not v:
                if distance[k][0] < min_road:
                    next_u, min_road = k, distance[k][0]
        
        u = next_u
    # print(distance)
    return distance



if __name__=='__main__':
    dijstra('2737', 0)
