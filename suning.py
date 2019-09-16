'''
@Description: 胸罩分析
@Author: Nick
@Date: 2019-09-16 15:29:46
@LastEditTime: 2019-09-16 17:52:31
@LastEditors: Please set LastEditors
'''
import requests
from lxml import etree
import json

def getOneReviewList():
    url = f'https://review.suning.com/ajax/cluster_review_lists/style--000000000621818808-0070158394-total-1-default-10-----reviewList.htm?callback=reviewList'
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

    r = requests.get(url, headers = header)
    c = r.text
    c = c.replace('reviewList(','')
    c = c.replace(')','')
    c = c.replace('false','"false"')
    c = c.replace('true','"true"')
    suningjson = json.loads(c)
    return suningjson

def getProductIdList():
    url = 'https://search.suning.com/%E8%83%B8%E7%BD%A9/'
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    r = requests.get(url, headers=header)
    # print('html', r.text)
    html = etree.HTML(r.text)
    
    sa_data = html.xpath('//a[@class="sellPoint"]/@sa-data')
    for item in sa_data:
      print('sa_data', item)

# jsonData = getOnePage()
getProductIdList()

# print('jsonData', jsonData)
