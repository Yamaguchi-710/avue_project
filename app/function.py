#import
import random
from pathlib import Path
import cv2
import pandas as pd
from . import param as prm

prj_path = Path(__file__).resolve().parent

#関数宣言
#ボルトリストの作成 [[num,x,y],[num,x,y],...]
def make_list(filename,name):
    list_csv = pd.read_csv(filename,header=None).values.tolist()
    
    list_f = []
    for i in range(prm.MAX_NUM(name)):
        list_temp = [i]
        list_temp.append(list_csv[i][0])
        list_temp.append(list_csv[i][1])
        list_f.append(list_temp)
    return list_f


#スタート足候補
def start_foot_list(ret,input_list,name):
    list_start_foot_f = []
    for i in range(prm.MAX_NUM(name)):
        if input_list[i][2] >= ret[0]:
            list_start_foot_f.append(i)
    return list_start_foot_f


#ルートセット
def route_set(input_sf,input_list,name):
    list_route_f = [input_list[input_sf]]
    reach = prm.REACH(name)
    ret = prm.Border(name)
    list_p = []
    p = 0
    k = 0
    j = 0
    while j <= prm.MAX_NUM(name):
        j = j+1
        for i in range(prm.MAX_NUM(name)):
            h = input_list[i][2]-list_route_f[k][2]
            if h <= 0:
                h = h*(-1)
                r = ((input_list[i][1]-list_route_f[k][1])**2 + h**2)**0.5
                if r <= reach:
                    ph = reach*0.5*2 - abs(h-reach*0.5)
                    pr = reach*0.5*2 - abs(r-reach*0.5)
                    p = p + ph*pr
                    list_temp = [i,p]
                    list_p.append(list_temp)
        rd = random.random()
        for l in range(len(list_p)):
            q = (list_p[l][1])/p
            if rd < q:      
                list_route_f.append(input_list[list_p[l][0]])
                k = k+1
                p = 0
                list_p = []
                break
        if list_route_f[k][2] <= ret[2]:
            break
    return list_route_f

# 関数
def make(name):
    list = make_list(prj_path.joinpath('csv/'+name+'/hold_list.csv'),name)

    list_start_foot = start_foot_list(prm.Border(name),list,name)

    sf = random.choice(list_start_foot)

    list_route = route_set(sf,list,name)
    
    return list_route    


# 描画
def print_prj(list_route,name):
    img = cv2.imread(str(prj_path.joinpath('image/'+name+'/input.png')))
    ret = prm.Border(name)

    h, w, _ = img.shape
    resize_rate = 900/h
    wall = cv2.resize(img, (int(w*resize_rate), 900))

    start_flag = 0
    for i in range(len(list_route)-1):
        x = list_route[i][1]
        y = list_route[i][2]
        if start_flag ==0:
            if y < ret[1]:
                cv2.circle(wall, center=(x, y), radius=30, color=(0, 0, 255), thickness=3, lineType=cv2.LINE_4, shift=0)
                start_flag = 1         
            else:
                cv2.circle(wall, center=(x, y), radius=20, color=(0, 255, 0), thickness=3, lineType=cv2.LINE_4, shift=0)
        else:
            cv2.circle(wall, center=(x, y), radius=20, color=(0, 255, 0), thickness=3, lineType=cv2.LINE_4, shift=0)

    
    x = list_route[len(list_route)-1][1]
    y = list_route[len(list_route)-1][2]
    cv2.circle(wall, center=(x, y), radius=30, color=(255, 0, 0), thickness=3, lineType=cv2.LINE_4, shift=0)
        
    cv2.imwrite(str(prj_path.joinpath('image/'+name+'/output.png')), wall)
    cv2.imwrite(str(prj_path.joinpath('static/media/'+name+'/output.png')), wall)
    