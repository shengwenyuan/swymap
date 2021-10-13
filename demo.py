import argparse
import json
from algorithms import dijstra

'''
1北工大 2737
2北大 3077
3对外经贸 435
4北师大 1443
5北理 2873
6北交 337
7人大 3074
8中传 2780
'''
campus = {'北工大':'2737', '北大':'3077', '对外经贸':'435', '北师大':'1443', '北理':'2873', '北交':'337', '人大':'3074', '中传':'2780'}

with open('stationHallmark.json', 'r') as f:
    stationHallmark=json.load(f)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fr', type=str, default='北工大', help=\
                        '北工大 北大 对外经贸 北师大 北理 北交 人大 中传')
    parser.add_argument('--to', type=str, default='北大', help=\
                        '北工大 北大 对外经贸 北师大 北理 北交 人大 中传')
    parser.add_argument('--w', type=int, default=0, help=\
                        '0路程最短 1时间最快 2票价最低')
    opt = parser.parse_args()
    return opt




if __name__=='__main__':
    args=parse_opt()
    distance = dijstra(campus[args.fr], args.w)

    print('{}<--'.format(args.to), end='')
    i=campus[args.to]
    while distance[i][1] != campus[args.fr]:
        tmp = distance[i][1]
        name = stationHallmark[tmp][0]
        print('{}<--'.format(name), end='')
        i = tmp
    print(args.fr)