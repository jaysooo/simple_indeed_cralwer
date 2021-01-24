import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import base64


class IndeedCrawler:
    #    indeed_url = "https://kr.indeed.com/job?q=빅데이터&I=경기도+수원&sort=date"

    def __init__(self):
        self.indeed_org_url = 'https://kr.indeed.com'
        self.ineed_base_url = 'https://kr.indeed.com/jobs?sort=date&I=경기도+수원&q'
        self.info = []
        self.indeed_url = "https://kr.indeed.com/jobs?q=%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0&l=%EA%B2%BD%EA%B8%B0%EB%8F%84+%EC%88%98%EC%9B%90&sort=date"
        self.LIMIT = 10
        pass

    def getBsObjFromURL(self, target_url=""):
        req_result = requests.get(target_url)
        bs = BeautifulSoup(req_result.text, 'html.parser')
        return bs

    def GetJobinfoCrawling(self, page=0, word=''):
        if page == 0:
            url = f"{self.ineed_base_url}={word}"
        else:
            url = f"{self.ineed_base_url}={word}&start={page*self.LIMIT}"
        jobObj = self.getBsObjFromURL(
            target_url=url)
        pageContent = jobObj.find_all(
            'div', class_="jobsearch-SerpJobCard")

        for content in pageContent:
            a = content.find('a', class_="jobtitle")
            data = (a['title'], a['href'], content.find(
                "div", class_="jobsearch-SerpJobCard-footer").find("span").string)

            data2 = {}
            data2["title"] = a['title']
            data2['link'] = self.indeed_org_url+a['href']
            data2['date'] = content.find(
                "div", class_="jobsearch-SerpJobCard-footer").find("span").string

            #print(data)
            self.info.append(data2)

    def allGetJobInfoCrawling(self, word=''):
        last_page = self.getLastPage()
        for i in range(0, last_page):
            self.GetJobinfoCrawling(page=i, word=word)

    def getLastPage(self):
        indeedMain = self.getBsObjFromURL(self.indeed_url)
        pages = indeedMain.find("div", class_="pagination").find_all("a")
        last_pages = pages[-2].get_text(strip=True)
        return int(last_pages)

    def saveInfoToCsv(self, word='job'):
        jsonString = json.dumps(self.info, ensure_ascii=False)
        df = pd.DataFrame.from_records(self.info)
        df.to_csv(f"csv/{word}_info.csv", sep="\t",
                  header=True, encoding='utf-8')
        print(df)

    def getJsonInfo(self):
        return json.dumps(self.info, ensure_ascii=False)

    def getArrayInfo(self):
        return self.info

    def PrintInfo(self):
        for d in self.info:
            print(d)


class Car():

    def __init__(self, **kwargs):

        self.wheel = kwargs.get("wheel", "30")
        self.color = kwargs.get("color", "black")
        self.name = kwargs.get("name", "tesla")

    def __str__(self):

        return "{} : {} : {} ".format(self.name, self.color, self.wheel)


class SpecialCar(Car):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.special_name = kwargs.get("sp", "speical car")

    def __str__(self):
        return "{}:{}".format(self.special_name, self.color)


# myCar = Car(name="bents")
# sp = SpecialCar(sp="my special car")
# print(sp)

#my = IndeedCrawler()
#my.allGetJobInfoCrawling(word='DB')
#my.saveInfo()
#my.PrintInfo()
