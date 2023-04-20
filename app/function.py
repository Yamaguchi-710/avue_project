#import
import random
from pathlib import Path
import cv2
import pandas as pd
from . import param as prm
# import param as prm

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
def start_foot_list(border,input_list,name):
    list_start_foot_f = []
    
    for i in range(prm.MAX_NUM(name)):
        if input_list[i][2] >= border[0]:
            list_start_foot_f.append(i)
    return list_start_foot_f


#ルートセット
def route_set(input_sf,input_list,name,list_forms):
    
    list_route_f = [input_list[input_sf]]
    reach = prm.REACH(name)*(list_forms[0]/170)
    distri = 0.3*(list_forms[2]/30)
    border = prm.Border(name)
    border_size = prm.border_size(name)
    hold_size = prm.hold_size(name)
    list_p = []
    list_s = []
    p = 0
    k = 0
    j = 0
    start_flag = 0
    goal_flag = 0
    
    while j <= prm.MAX_NUM(name):
        j = j+1
        for i in range(prm.MAX_NUM(name)):
            h = input_list[i][2]-list_route_f[k][2]
            if h < 0:
                if (start_flag != 1 or input_list[i][3] < border_size[0]) and \
                    (goal_flag != 1 or input_list[i][3] >= border_size[1]):
                    h = h*(-1)
                    r = ((input_list[i][1]-list_route_f[k][1])**2 + h**2)**0.5
                    if r <= reach:
                        if start_flag == 1 :
                            ph = reach*(1+distri) - h
                        else:
                            ph = reach*(1+distri) - abs(h-reach*distri)
                        pr = reach*(1+distri) - abs(r-reach*distri)
                        if list_forms[1] == 4:
                            pa = 1
                        else:
                            if list_forms[1] == 1:
                                base = hold_size[1]+(hold_size[2]-hold_size[1])/2
                            elif list_forms[1] == 2:
                                base = hold_size[2]
                            else:
                                base = hold_size[2]+(hold_size[0]-hold_size[2])/2
                            
                            pa = (hold_size[0]-hold_size[1]) - abs(input_list[i][3]-base)
                            
                        p = p + ph*pr*pa
                        list_temp = [i,p]
                        list_p.append(list_temp)
        rd = random.random()
        for l in range(len(list_p)):
            q = (list_p[l][1])/p
            if rd < q:      
                list_route_f.append(input_list[list_p[l][0]])
                if list_route_f[k][2] <= border[1]:
                    if start_flag == 0:
                        if list_route_f[k][3] < border_size[0]:
                            list_s = [k]
                            start_flag = 1
                        else:
                            list_s = [k,-1]
                            start_flag = 2
                    elif start_flag == 1:
                        list_s.append(k)
                        start_flag = 2
                    else:
                        pass
                k = k+1
                p = 0
                list_p = []
                break
        if list_route_f[k][2] <= border[2]:
            if list_route_f[k][3] >= border_size[1]:
                route_sum = k+1
                break
            else:
                goal_flag = 1
        
    list_route = []
    for i in range(route_sum):
        if (i == list_s[0]) or (i == list_s[1]):
            list_num = list_route_f[i]
            list_num.append(1)
            list_route.append(list_num)
        elif (i == route_sum-1):
            list_num = list_route_f[i]
            list_num.append(2)
            list_route.append(list_num)
        else:
            list_num = list_route_f[i]
            list_num.append(0)
            list_route.append(list_num)
        
    return list_route


# 関数
def make(name, forms):

    list = make_list(prj_path.joinpath('csv/'+name+'/hold_list.csv'),name)
    list = pd.read_csv(prj_path.joinpath('csv/'+name+'/hold_list.csv'),header=None).values.tolist()
    
    list_start_foot = start_foot_list(prm.Border(name),list,name)

    sf = random.choice(list_start_foot)

    list_route = route_set(sf,list,name,forms)
    
    return list_route    


# 描画
def print_prj(list_route,name):
    img = cv2.imread(str(prj_path.joinpath('image/'+name+'/input.png')))

    h, w, _ = img.shape
    resize_rate = 900/h
    wall = cv2.resize(img, (int(w*resize_rate), 900))

    for i in range(len(list_route)):
        x = list_route[i][1]
        y = list_route[i][2]
        if list_route[i][4] ==1:
            cv2.circle(wall, center=(x, y), radius=20, color=(0, 0, 255), thickness=3, lineType=cv2.LINE_4, shift=0)
        elif list_route[i][4] ==2:
            cv2.circle(wall, center=(x, y), radius=30, color=(255, 0, 0), thickness=3, lineType=cv2.LINE_4, shift=0)
        else:
            cv2.circle(wall, center=(x, y), radius=20, color=(0, 255, 0), thickness=3, lineType=cv2.LINE_4, shift=0)

        
    cv2.imwrite(str(prj_path.joinpath('image/'+name+'/output.png')), wall)
    cv2.imwrite(str(prj_path.joinpath('static/media/'+name+'/output.png')), wall)
    