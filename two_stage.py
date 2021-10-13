import json



# with open('stationHallmark.json', 'r') as f:
#     a=json.load(f)
#     for i, item in a.items():
#         if i == '20': break
#         print(type(item[0]))
with open('stationGraph.json', 'r') as f:
    a=json.load(f)
    for i, item in a.items():
        if i == '20': break
        print(type(item[0][0]))
