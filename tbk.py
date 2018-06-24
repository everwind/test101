# -*- coding: utf-8 -*-
import requests
import json
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

def get_res(key, res_list):
    url = "http://pub.alimama.com/items/search.json"
    payload = {'q': key, 'queryType':0, 'sortType':9,'toPage':1, 'perPageSize':100 }
    r = requests.get(url, params=payload)
    js = r.json()
    #print js
    pageList = js['data']['pageList']
    for p in pageList:
        res={}
        res['关键字']=key
        res['店铺名称']=p['shopTitle'].encode('utf-8')
        res['图片链接']="https://"+p['pictUrl'].encode('utf-8')
        res['标题']=p['title'].encode('utf-8')
        res['开始日期']=p['couponEffectiveStartTime']
        res['结束日期']=p['couponEffectiveEndTime']
        res['销量']=p['biz30day']
        res['佣金']=p['tkCommFee']
        res['价格']=p['zkPrice']
        res['总佣金']=p['totalFee']
        res['比率']=p['tkRate']
        res['推广量']=p['totalNum']
        res['商品链接']=p['auctionUrl'].encode('utf-8')
        res_list.append(res)

def save_res(fo, res_list):    
    keys = ['关键字', '店铺名称','标题','开始日期','结束日期', '销量','价格', '佣金', '比率','总佣金','推广量', '图片链接', '商品链接']
    fo.write("\t".join(keys)+"\n")
    for res in res_list:
        ss=[ str(res[k]) for k in keys ]
        line="\t".join(ss)
        #print line
        fo.write(line+"\n")




from Tkinter import *
import os
import tkFileDialog
import tkMessageBox


root = Tk() # 初始化Tk()
root.title("entry-test")    # 设置窗口标题
root.geometry("300x200")    # 设置窗口大小 注意：是x 不是*
root.resizable(width=True, height=False) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True




out_path="D:"
input_file=""

def select_path():
    global out_path
    default_dir = r"C:"  # 设置默认打开目录
    out_path = tkFileDialog.askdirectory(title=u"选择输出目录",initialdir=(os.path.expanduser(default_dir)))
    print out_path  # 返回文件全路径
    #print tkFileDialog.askdirectory()  # 返回目录路径

def select_in_path():
    global input_file
    input_file = tkFileDialog.askopenfilename(title=u"选择输入文件")
    print input_file  # 返回文件全路径
    #print tkFileDialog.askdirectory()  # 返回目录路径
cnt = 0

def run():
    filename = input_file+"_out.txt"
    fo = open(filename,'w')
    cnt=1
    for key in open(input_file):
        key=key.strip()
        #key = unicode(key, 'gbk')
        #key=key.encode('utf-8')
        print key
        process.set("抓取;"+ key)
        res_list=[]
        get_res(key, res_list)
        save_res(fo, res_list)
        process.set("完成抓取;"+ key + " 已经抓取个数:"+str(cnt))
        cnt+=1
    fo.flush()
    fo.close()
    process.set("完成抓取,总数:"+str(cnt))
    print "save sucess\n"
    
Button(root, text="选择输入文件", command=select_in_path).pack()
#Button(root, text="选择输出路径", command=select_path).pack()
Button(root, text="开始抓取", command=run).pack()

process = Variable()
e2 = Entry(root, textvariable=process)
process.set("打印进度") # 设置文本框中的值
e2.pack()   # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM

root.mainloop() # 进入消息循环
driver.close()

#res_list=[]
#get_res('手持吸尘器', res_list)
#file_name='bbb.txt'
#save_res(file_name, res_list)
