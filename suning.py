'''
@Description: 胸罩分析
@Author: Nick
@Date: 2019-09-16 15:29:46
@LastEditTime: 2019-09-17 13:51:21
@LastEditors: Please set LastEditors
'''
from urllib3 import *
import sqlite3
import json
import re
import os
from bs4 import BeautifulSoup
import requests
from lxml import etree
import json
disable_warnings()

# 创建数据库
dbPath = 'bra.sqlite'
if os.path.exists(dbPath):
    os.remove(dbPath)
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()
cursor.execute('''create table t_sales
            (id integer primary key autoincrement not null,
            color text not null,
            size text not null,
            source text not null,
            discuss mediumtext not null,
            time text not null);''')
conn.commit()

def getOneReviewList(itemIdObj, num):
    url = f'https://review.suning.com/ajax/cluster_review_lists/style--000000000{itemIdObj["prdid"]}-{itemIdObj["shopid"]}-total-{num}-default-10-----reviewList.htm?callback=reviewList'
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

    r = requests.get(url, headers = header)
    c = r.text
    c = c.replace('reviewList(','')
    c = c.replace(')','')
    c = c.replace('false','"false"')
    c = c.replace('true','"true"')
    suningjson = json.loads(c)
    return suningjson['commodityReviews']

def getProductIdList():
    url = 'https://search.suning.com/%E8%83%B8%E7%BD%A9/'
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    r = requests.get(url, headers=header)
    html = etree.HTML(r.text)
    
    sa_data = html.xpath('//a[@class="sellPoint"]/@sa-data')
    return sa_data

# ids = getProductIdList()
# print('ids', ids[0])
# suning = getOneReviewList(eval(ids[0]), 1)
# print('suning', suning['commodityReviews'][0]['bestTag'])
initial = 0
productIdList = getProductIdList()
print(len(productIdList))
while initial < len(productIdList):
      itemIdObj = productIdList[initial]
      rateList = getOneReviewList(eval(itemIdObj), 1)
      n = 0
      while n < len(rateList):
          if ('charaterDesc2' in rateList[n]['commodityInfo']):
              color = rateList[n]['commodityInfo']['charaterDesc2']
          if ('commodityName' in rateList[n]['commodityInfo'] and len(re.split(' ', rateList[n]['commodityInfo']['commodityName'])[2]) < 15 and str.find(re.split(' ', rateList[n]['commodityInfo']['commodityName'])[2], '色') == -1):
              size = re.split(' ', rateList[n]['commodityInfo']['commodityName'])[2]
          elif ('commodityName' in rateList[n]['commodityInfo'] and len(re.split(' ', rateList[n]['commodityInfo']['commodityName'])[2]) >= 15 and str.find(re.split(' ', rateList[n]['commodityInfo']['commodityName'])[2], '色') != -1):
              size = re.split(' ', rateList[n]['commodityInfo']['commodityName'])[3]
          if ('publishTime' in rateList[n]):
               dtime = rateList[n]['publishTime']
          if ('content' in rateList[n]):
               rateContent = rateList[n]['content']
          print('size', size)
          cursor.execute('''insert into t_sales(color,size,source,discuss,time) 
                          values('%s','%s','%s','%s','%s') ''' % (color,size,'苏宁',rateContent,dtime))
          conn.commit()
          n += 1
          
      initial += 1
      print('initial', initial)
conn.close()
