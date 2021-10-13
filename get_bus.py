import json
import requests
import csv
import time
import random

def main(city,keywords):
    key = "1a9f024c919f00351705948cd9e858f6" #高德API key
    url = "https://restapi.amap.com/v3/bus/linename?parameters"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'} #模拟浏览器参数
    keyword = { "extensions": "all", "key": key, "output": "json", "city": city, "offset": "0","keywords": keywords, "platform": "JS"}
    a = requests.get(url, headers=headers, params=keyword)
    html = a.text
    data = json.loads(html)
    with open('apple.json', 'w') as f:
        json.dump(data, f)
    # print(data)
    if data["status"] == "1":
        station(data, keywords)
        print('a success!')
    else:
        print("未查询到{}市的{}信息".format(city,keywords))

def station(html,keywords):
    print("开始抓取{}数据".format(keywords))
    buslines = html["buslines"]
    count = 0
    filename = 'line{}.csv'.format(keywords)
    # for i in buslines:
    count = count+1
    information = []
    busstops = buslines[0]["busstops"]
    for T in busstops:
        cell = []
        lng1 = T["location"].split(",")[0]
        lat1 = T["location"].split(",")[1]
        # lng2 = convert_main(lng1,lat1)[0]
        # lat2 = convert_main(lng1, lat1)[1]
        name = T["name"]
        # cell.append(city)
        cell.append(name)
        cell.append(lng1)
        cell.append(lat1)
        with open(filename, 'a') as f:
            write = csv.writer(f)
            write.writerow(cell)

with open('bus_k.txt', 'r') as f:
    text = f.read()
    text = text.split('\n')
    for line in text:
        main('北京', '{}'.format(line))
        time.sleep(random.randint(1,3))
f.close()

# main('北京', '108')