'''
@Description: 猫眼
@Author: Nick
@Date: 2019-09-05 15:14:18
@LastEditTime: 2019-09-05 18:05:28
@LastEditors: Please set LastEditors
'''

import requests
from lxml import etree
import json

def getOnePage(page):
    url = f'https://maoyan.com/board/4?offset={(page - 1) * 10}'
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

    r = requests.get(url, headers=header)
    return r.text



def parse(text):
    html = etree.HTML(text)
    #names 返回的是列表
    names = html.xpath('//div[@class="movie-item-info"]/p[@class="name"]/a/@title')
    releasetimes = html.xpath('//p[@class="releasetime"]/text()')
    print(names, releasetimes)
    item = {} # 字典
    for name, releasetime in zip(names, releasetimes):
      item['name'] = name
      item['releasetime'] = releasetime

      # 生成器
      yield item

def save2File(data):
    with open('movie.json', 'a', encoding='utf-8') as f:
        data = json.dumps(data, ensure_ascii=False) + ',\n'
        f.write(data)


def run():
    for n in range(1, 11):
        items = parse(getOnePage(n))
        for item in items:
            save2File(item)
if __name__ == "__main__":
    run()