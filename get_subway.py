import json

def parse_page():
    f = open('info_subway.txt', 'r', encoding='utf-8')
    text = f.read()
    f.close()
    lines_list = json.loads(text).get('l')
    # 地铁线路信息表
    lineInfo_list = []
    for line in lines_list:
        #每条线的信息集合
        lineInfo = {}
        lineInfo['ln'] = line.get('ln')
        print(lineInfo['ln'])

        #线路站点列表
        station_list = []
        st_list = line.get('st')
        for st in st_list:
            station_dict = {}
            station_dict['name'] = st.get('n')
            coord = st.get('sl')
            station_dict['lat'] = coord.split(',')[0]
            station_dict['lon'] = coord.split(',')[-1]
            print("站名称:", station_dict['name'])
            print("经度：", station_dict['lat'])
            print("纬度：", station_dict['lon'])
            station_list.append(station_dict)
            #pass
        print('-----------------------------------')
        lineInfo['st'] = station_list
        lineInfo['kn'] = line.get('kn')
        lineInfo['ls'] = line.get('ls')
        lineInfo['cl'] = line.get('cl')
        lineInfo_list.append(lineInfo)
    #返回各线路信息列表
    return lineInfo_list

def save_file(lineInfo_list):
    print("开始写入文件......")
    for index, lineInfo in enumerate(lineInfo_list):
        filename = 'line{}'.format(lineInfo['kn'])
        with open(filename, 'a', encoding='utf-8') as f:
            for st in lineInfo['st']:
                f.write(st['name'] + "," + st['lat'] + "," + st['lon'] + "\n")
    print("写入文件完成！")



save_file(parse_page())