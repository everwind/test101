# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:52:59 2017

@author: GLee
"""
import sys

from selenium import webdriver
#driver = webdriver.Chrome()
driver = webdriver.Firefox()
driver.get('https://shopee.tw/')
ck = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in driver.get_cookies()]) #把從COOKIE抓到的NAME 做成字串,再把結果放到LIST中
tok = [item.get('value') for item in driver.get_cookies() if item.get('name') == 'csrftoken'][0]

import requests
import json

jd = { 'by':'sales', 'keyword': '媽媽包','limit':50, 'match_id':100, 'newest':0, 'order':'desc', 'page_type':'search'}
#發現缺少Header，所以開始加入一些資訊來嘗試
headers = {
    #'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',#判斷是由人來瀏覽網頁
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'x-csrftoken': tok,#用變數代替
    'referer':'https://shopee.tw/search/?category=100&keyword=%E5%AA%BD%E5%AA%BD%E5%8C%85',
    'cookie': ck, #用變數代替
}
#res = requests.post('https://shopee.tw/api/v1/items/', json = jd, headers = headers)
print 'hello world'
res = requests.get('https://shopee.tw/api/v2/search_items/', params = jd, headers = headers)
#print res.json()
#js = json.dumps(res)
js = res.json()
#print js
items = js['items']
f = open("test.csv",'w')
s = ['itemid','brand', 'name', 'price','price_min', 'price_max', 'sold（销量）', 'cmt_count(评论数)','是否商城','浏览次数','image']

prefix = 'https://cfshopeetw-a.akamaihd.net/file/'
ss = ",".join(s)
f.write(ss+"\n")
for p in items:
    name=''
    if p['name']!= None:
        name=p['name'].encode('utf-8')
    brand=''
    if p['brand']!=None:
        brand=p['brand'].encode('utf-8')
    image = prefix+"/"+p['image'].encode('utf-8')
    sold = p['sold']
    rate = p['item_rating']['rating_star']
    cmt_count = p['cmt_count']
    is_official_shop = p['is_official_shop']
    view_count = p['view_count']
    ss = [str(p['itemid']), name, brand, str(p['price']), str(p['price_min']), str(p['price_max']),str(sold),str(cmt_count), str(is_official_shop), str(view_count), image]
    #ss = [ str(p[a]) for a in s]
    #print p
    print p['name'].encode('utf-8')+"\t"+str(p['price'])
    out = ",".join(ss)
    out.decode('utf-8').encode('gb18030')
    f.write(out+"\n")
f.close()
driver.close()
print 'done'
#import pandas
#df = pandas.DataFrame(res.json())
