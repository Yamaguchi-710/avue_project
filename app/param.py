from pathlib import Path
import pandas as pd

prj_path = Path(__file__).resolve().parent

#定数
#ホールド全数
def MAX_NUM(name):
    max = sum([1 for _ in open(prj_path.joinpath('csv/'+name+'/hold_list.csv'))])
    return max


#ゴール高さ下限、スタート足高さ上限、スタート高さ下限
def Border(name):
    list_csv1 = pd.read_csv(prj_path.joinpath('csv/'+name+'/border.csv'),header=None).values.tolist()

    y_ave = []
    for i in range(3):
        y1 = list_csv1[i][1]
        y2 = list_csv1[i][3]
        y_ave.append((y1+y2)/2)

    max = y_ave[0]
    min = y_ave[0]
    for i in range(3):
        if y_ave[i] > max:
            max = y_ave[i]
        if y_ave[i] < min:
            min = y_ave[i]

    mid = y_ave[0]
    for i in range(3):
        if y_ave[i] != min and y_ave[i] != max:
            mid = y_ave[i]

    return min, mid, max


#リーチ 
def REACH(name):
    list_csv2 = pd.read_csv(prj_path.joinpath('csv/'+name+'/reach.csv'),header=None).values.tolist()
    reach = ((list_csv2[0][0]-list_csv2[0][2])**2+(list_csv2[0][1]-list_csv2[0][3])**2)**0.5
    return reach


#ゴール高さ,幅取得
def MAX_X(name):
    list_csv = pd.read_csv(prj_path.joinpath('csv/'+name+'/hold_list.csv'),header=None).values.tolist()
    max = 0
    for i in range(MAX_NUM(name)):
        if max < list_csv[i][0]:
            max = list_csv[i][0]
    return max

def MAX_Y(name):
    list_csv = pd.read_csv(prj_path.joinpath('csv/'+name+'/hold_list.csv'),header=None).values.tolist()
    max = 0
    for i in range(MAX_NUM(name)):
        if max < list_csv[i][1]:
            max = list_csv[i][1]
    return max
