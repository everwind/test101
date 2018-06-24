#-*- coding: UTF-8 -*-

import sys
from selenium import webdriver
import requests
import json

#driver = webdriver.Chrome()
driver = webdriver.Firefox()
driver.get('https://shopee.tw/')
ck = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in driver.get_cookies()]) #把從COOKIE抓到的NAME 做成字串,再把結果放到LIST中
tok = [item.get('value') for item in driver.get_cookies() if item.get('name') == 'csrftoken'][0]
#發現缺少Header，所以開始加入一些資訊來嘗試
headers = {
    #'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',#判斷是由人來瀏覽網頁
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'x-csrftoken': tok,#用變數代替
    'referer':'https://shopee.tw/search/?category=100&keyword=%E5%AA%BD%E5%AA%BD%E5%8C%85',
    'cookie': ck, #用變數代替
}


def get_product(key, res_list):
    jd = { 'by':'sales', 'keyword': key,'limit':50, 'match_id':100, 'newest':0, 'order':'desc', 'page_type':'search'}
    res = requests.get('https://shopee.tw/api/v2/search_items/', params = jd, headers = headers)
    js = res.json()
    items = js['items']    
    prefix = 'https://cfshopeetw-a.akamaihd.net/file/'
    for p in items:
        res = {}
        res['id'] = p['itemid']
        name=''
        if p['name']!= None: name=p['name'].encode('utf-8')
        image = prefix+"/"+p['image'].encode('utf-8')
        res['名字']=name
        res['图片']=image
        res['销量'] = p['sold']
        res['打分'] = p['item_rating']['rating_star']
        res['评论数'] = p['cmt_count']
        res['商家'] = p['is_official_shop']
        res['浏览数'] = p['view_count']
        res['价格'] = p['price']
        res['最低价格'] = p['price_min']
        res['最高价格'] = p['price_max']
        res_list.append(res)
        #print res

def save_res(res_list,file_name):
        fo=open(file_name,'w')
        keys=['id','名字','价格','最低价格','最高价格','商家','销量','浏览数', '打分','评论数','图片']
        fo.write( "\t".join(keys)+"\n")
        for res in res_list:
            ss=[ str(res[k]) for k in keys]
            #line=",".join(ss).decode('utf-8').encode('ascii')
            line="\t".join(ss)
            fo.write(line+"\n")
        fo.flush()
        fo.close()


from Tkinter import *
import os
import tkFileDialog
import tkMessageBox


root = Tk() # 初始化Tk()
root.title("entry-test")    # 设置窗口标题
root.geometry("300x200")    # 设置窗口大小 注意：是x 不是*
root.resizable(width=True, height=False) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True


var = Variable()
e = Entry(root, textvariable=var)
var.set("输入关键字") # 设置文本框中的值
e.pack()   # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM

out_path="D:"

def select_path():
    global out_path
    default_dir = r"C:"  # 设置默认打开目录
    out_path = tkFileDialog.askdirectory(title=u"选择文件",initialdir=(os.path.expanduser(default_dir)))
    print out_path  # 返回文件全路径
    #print tkFileDialog.askdirectory()  # 返回目录路径

cnt = 0

def run():
    key = var.get().encode('utf-8')
    print "抓取："+ key
    res_list=[]
    get_product(key, res_list)
    process.set("当前已经抓取;"+str(len(res_list)))   
    save_res(res_list, out_path+"//"+var.get()+".txt")

Button(root, text="选择输出路径", command=select_path).pack()
Button(root, text="开始抓取", command=run).pack()

process = Variable()
e2 = Entry(root, textvariable=process)
process.set("打印进度") # 设置文本框中的值
e2.pack()   # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM

root.mainloop() # 进入消息循环
driver.close()
