# -*- coding:utf-8 -*-
import socket, time, math
import pandas as pd

ip_port = ('192.168.0.3', 8899) #连接对象WiFi小车无线串口的IP和端口
sk = socket.socket()            #建立套接字对象
sk.connect(ip_port)             #建立连接
sk.settimeout(20)               #连接超时20秒

mbsj = pd.read_csv(r'data\dddhzb.csv')   #使用pandas打开csv文件，sj为DataFrame
mbsj_1 = mbsj.tail(1)                    #取出最后一行，类型为Series
mbx = int(mbsj_1['xd'].values)           #通过字段索引转换后得到横坐标
mby = int(mbsj_1['yd'].values)           #得到纵坐标

while True:
    sj = pd.read_csv(r'data\zuobiao.csv')    #使用pandas打开csv文件，sj为DataFrame
    sj_id0 = sj[sj['id'] == 0]               #得到id为0的数据，类型为dataframe
    sj_1 = sj_id0.tail(1)                    #取出最后一行，类型为Series    
    x = int(sj_1['xd'].values)      #通过字段索引转换后得到横坐标
    y = int(sj_1['yd'].values)      #得到纵坐标
    jd = int(sj_1['jiaodu'].values) #得到角度值
    s = math.sqrt((x-mbx)**2+(y-mby)**2)
    theta = math.asin(-(mby-y)/s) #注意y轴反向
    mbjd = int(theta*180/math.pi)
    if mbx >= x:
        if mbjd < 0:
            mbjd = 360 + mbjd
    else:
        mbjd = 180 - mbjd            #以上计算目标坐标以及两点与x轴的夹角

    if s < 5: #两点距离小于5个像素
        sk.send('b'.encode('utf-8'))         #发送停止命令
        break                                #退出循环
    if mbjd - jd >= 10:                      #目标角度减真实角度大于10度
        sk.send('d'.encode('utf-8'))         #发送左急转命令（逆时针）
        continue                             #回到循环起始处
    if jd - mbjd >= 10:                      #真实角度减目标角度大于10度
        sk.send('c'.encode('utf-8'))         #发送右急转命令（顺时针）
        continue                             #回到循环起始处
    zf = chr(80 - (mbjd - jd))
    sk.send(zf.encode('utf-8'))
    
sk.close()