'''
@Description: 拉钩
@Author: Nick
@Date: 2019-09-18 09:54:41
@LastEditTime: 2019-09-18 17:26:42
@LastEditors: Please set LastEditors
'''
import requests
import re
import json
import time
import multiprocessing
import sqlite3
import os
# 创建数据库
dbPath = 'lagou.sqlite'
if os.path.exists(dbPath):
    os.remove(dbPath)
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()
cursor.execute('''create table lagou_data
            (id integer primary key autoincrement not null,
            companyShortName text,
            district text,
            salary text not null,
            positionId integer not null,
            longitude text not null,
            latitude text not null,
            positionName text not null,
            workYear text not null,
            education text not null,
            jobNature text,
            financeStage text,
            companySize text,
            industryField text,
            city text not null,
            positionAdvantage text,
            companyFullName text,
            crawl_date text not null);''')
conn.commit()

class HandleLagou(object):
    def __init__(self):
        #使用session保存cookies信息
        self.lagou_session = requests.session()
        self.header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
        self.city_list = ""

    # 获取城市列表方法
    def handle_city(self):
        # 所有城市
        city_search = re.compile(r'zhaopin/">(.*?)</a>')
        city_url = "https://www.lagou.com/jobs/allCity.html"
        ctiy_result = self.handle_request(method="GET", url=city_url)
        self.city_list = city_search.findall(ctiy_result)
    
        # 所有城市对应的map
        city_map_reg = re.compile(r'global.cityNumMap = (.*?);')
        city_map_url = "https://www.lagou.com/zhaopin/Python/?labelWords=label"
        city_map_result = self.handle_request(method="GET", url=city_map_url)
        
        self.city_map = json.loads(city_map_reg.findall(city_map_result)[0])
        
        # 不清除后面获取不到岗位信息
        self.lagou_session.cookies.clear()
    def handle_city_job(self, city):
        city_num = self.city_map[city]
        first_request_url = f'https://www.lagou.com/jobs/list_web/p-city_{city_num}?px=default'
        first_response = self.handle_request(method="GET", url=first_request_url)
        total_page_reg = re.compile(r'<span class="span totalNum">(\d+)</span>')
        try:
            total_page = total_page_reg.findall(first_response)[0]
        except:
            return
        else:
            for i in range(1, int(total_page)+1):
                data = {
                  "pn": i,
                  "kd": "web"
                }
                page_url = f'https://www.lagou.com/jobs/positionAjax.json?px=default&city={city}&needAddtionalResult=false'
                referer_url = f'https://www.lagou.com/jobs/list_web/p-city_{city_num}?px=default'
                self.header["Referer"] = referer_url.encode()
                response = self.handle_request(method="POST", url=page_url, data=data, info=city_num)
                lagou_data = json.loads(response)
                
                job_list = lagou_data['content']['positionResult']['result']
                for job in job_list:
                    print('job', job["positionName"])
                    cursor.execute('''insert into lagou_data(positionId,longitude,latitude,positionName,workYear,education,jobNature,financeStage,companySize,industryField,city,positionAdvantage,companyShortName,companyFullName,district,salary,crawl_date) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') ''' % (job["positionId"], job["longitude"], job["latitude"], job["positionName"], job["workYear"], job["education"], job["jobNature"], job["financeStage"], job["companySize"], job["industryField"], job["city"], job["positionAdvantage"], job["companyShortName"], job["companyFullName"], job["district"], job["salary"], job["createTime"]))
                    conn.commit()
    # 封装请求
    def handle_request(self, method, url, data=None, info=None):
        while True:
            # 阿布云代理
            proxyinfo = "http://%s:%s@%s:%s" % ('HLW7985B52UH24RD', '284D12A93E103DFD', 'http-dyn.abuyun.com', '9020')
            proxy = {
              "http": proxyinfo,
              "https": proxyinfo
            }
            # 代理不稳定的情况，报错了就让它重新请求
            try:
              if (method == "GET"):
                  response = self.lagou_session.get(url, headers=self.header, proxies=proxy, timeout=6)
              elif (method == "POST"):
                  response = self.lagou_session.post(url, headers=self.header, data=data, proxies=proxy, timeout=6)
            except:
                self.lagou_session.cookies.clear()
                # 再种下cookies
                first_request_url = f'https://www.lagou.com/jobs/list_web/p-city_{info}?px=default'
                self.handle_request(method="GET", url=first_request_url)
                # 睡上10秒钟再次继续
                time.sleep(10)
                continue
            if '频繁' in response.text:
                print('频繁操作', response.text)
                # 遇到频繁请求，先清楚cookie信息
                self.lagou_session.cookies.clear()
                # 再种下cookies
                first_request_url = f'https://www.lagou.com/jobs/list_web/p-city_{info}?px=default'
                self.handle_request(method="GET", url=first_request_url)
                # 睡上10秒钟再次继续
                time.sleep(10)
                continue
            return response.text


if __name__ == "__main__":
    lagou = HandleLagou()
    lagou.handle_city()
    # 创建进程池
    pool = multiprocessing.Pool(2)
    # 引入多进程 加速抓取
    for city in lagou.city_list:
        pool.apply_async(lagou.handle_city_job, args=('杭州',))
        pool.close()
        pool.join()
        break
    conn.close()