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
    fo.flush()



from Tkinter import *
import os
import tkFileDialog
import tkMessageBox
from tkinter.scrolledtext import ScrolledText

root = Tk() # 初始化Tk()
root.title("entry-test")    # 设置窗口标题
root.geometry("300x200")    # 设置窗口大小 注意：是x 不是*
root.resizable(width=True, height=False) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True




out_path="D:"
input_file=""
out_file=""
fo=None

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
    global out_file
    out_file = input_file+"_out.txt"
    print '输出目录:'
    print out_file
    global fo
    fo = open(out_file,'w')
    #print tkFileDialog.askdirectory()  # 返回目录路径
cnt = 0

'''
def run2():
    filename = input_file+"_out.txt"
    fo = open(filename,'w')
    cnt=1
    def print_process():
        t.insert(END,'抓取个数：'+str(cnt)+'\n')
        t.after(1000, print_process)
    print_process()
    for key in open(input_file):
        key=key.strip()
        key=key.decode('gb2312').encode('utf-8')
        print key
        t.insert(END,"抓取;"+ key+"\n")
        res_list=[]
        get_res(key, res_list)
        save_res(fo, res_list)
        cnt+=1
        if cnt>10: break
    fo.flush()
    fo.close()
    print "save sucess\n"
'''



def run():
    run_btn.config(state='disabled')
    fail_keys=[]
    keys=[]
    seconds=int(process.get())
    print "seconds:"+str(seconds)
    def print_process(i, keys):
        if i>= len(keys):
            t.insert(END,'######### 抓取完成，失败个数：'+str(len(fail_keys))+'\n')
            t.insert(END, '\n'.join(fail_keys))
            t.insert(END, "输出路径:\n")
            t.insert(END, out_file)
            run_btn.config(state='normal')
            return
        key=keys[i]        
        res_list=[]
        try:
            get_res(key, res_list)
            t.insert(END,'序号：'+str(i)+' key:'+key+'\n')
        except:
            fail_keys.append(key)
            t.insert(END,'序号：'+str(i)+' key:'+key+' 抓取失败\n')
        
        save_res(fo, res_list)
        t.after(seconds, print_process, i+1, keys)
    
    for key in open(input_file):
        key=key.strip()
        key=key.decode('gb2312').encode('utf-8')
        keys.append(key)
        #if len(keys)>10: break
    #print keys
    print_process(0, keys)
    fo.flush()
    #fo.close()
    print "save sucess\n"
    
Button(root, text="选择输入文件", command=select_in_path).pack()
#Button(root, text="选择输出路径", command=select_path).pack()
run_btn=Button(root, text="开始抓取", command=run)
run_btn.pack()

text = StringVar()
text.set('每隔几毫秒，抓取一次')
lb = Label(root, textvariable=text)
lb.pack()

process = Variable()
e2 = Entry(root, textvariable=process)
process.set("1000") # 设置文本框中的值
e2.pack()   # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
seconds=int(process.get())
if seconds<100: seconds=100

t = ScrolledText(root,width=20,height=20,background='#ffffff')
#scr = scrolledtext.ScrolledText(win, width=scrolW, height=scrolH, wrap=tk.WORD)  
t.pack(expand=1, fill="both")
root.mainloop() # 进入消息循环
fo.close()
#res_list=[]
#get_res('手持吸尘器', res_list)
#file_name='bbb.txt'
#save_res(file_name, res_list)
