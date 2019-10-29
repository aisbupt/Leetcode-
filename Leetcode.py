# coding:utf-8
import re
import json
import os
import codecs
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
'''
第一次爬取网页代码 By:Tjw Date:2019-06-17:19:01
'''
class Spider:
    def __init__(self,baseUrl,local_path,difficulty):
        self.baseUrl = baseUrl
        self.local_path = local_path
        self.difficulty = difficulty
        self.soup = ""
        self.params = ""
        self.header = ""
        self.r = {}
        self.Q = []
    def GetHtml(self,url,params={},header={}):
        print("打开网页：",self.baseUrl+url)
        self.params = params
        self.header = header
        trueurl = self.baseUrl+url
        try:
            r  = requests.get(trueurl,params = params,headers = header)
            r.raise_for_status()
            self.r = r.json()['stat_status_pairs'];
            return True
        except:
            print('Connection error')
            return False
    def GetMes(self):
        #print(self.r[0])
        for que in self.r:
            question = que['stat']
            if que['difficulty']['level']==self.difficulty:
                self.Q.append({'question_id':question['question_id'],'question__title_slug':question['question__title_slug'],'difficulty':que['difficulty']['level'],'points':0})
                #print(question['question_id'],question['question__title_slug'],que['difficulty']['level'])
        print(len(self.Q))
    def GetPoints(self):
        base = "https://leetcode.com/problems/"
        for title in self.Q:
            url = base+title['question__title_slug']+'/'
            title['points'] = self.get_proble_content(url,title['question__title_slug'])
        self.sort()
    def get_proble_content(self, problemUrl, title):
        #print(problemUrl)
        response = requests.get(problemUrl)
        setCookie = response.headers["Set-Cookie"]
        #print(setCookie)
        '''
        print(setCookie)
        setCookie = json.loads(setCookie)
        print(type(setCookie))
        '''
        try:
            pattern = re.compile("csrftoken=(.*?);.*?", re.S)
            csrftoken = re.search(pattern, setCookie)
            url = "https://leetcode.com/graphql"
            # data = {"operationName": "getQuestionDetail",
            #         "variables": {"titleSlug": title},
            #         "query": "query getQuestionDetail($titleSlug: String!) {\n  isCurrentUserAuthenticated\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    questionTitle\n    translatedTitle\n    questionTitleSlug\n    content\n    translatedContent\n    difficulty\n    stats\n    allowDiscuss\n    contributors\n    similarQuestions\n    mysqlSchemas\n    randomQuestionUrl\n    sessionId\n    categoryTitle\n    submitUrl\n    interpretUrl\n    codeDefinition\n    sampleTestCase\n    enableTestMode\n    metaData\n    enableRunCode\n    enableSubmit\n    judgerAvailable\n    infoVerified\n    envInfo\n    urlManager\n    article\n    questionDetailUrl\n    libraryUrl\n    companyTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    __typename\n  }\n  interviewed {\n    interviewedUrl\n    companies {\n      id\n      name\n      slug\n      __typename\n    }\n    timeOptions {\n      id\n      name\n      __typename\n    }\n    stageOptions {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  subscribeUrl\n  isPremium\n  loginUrl\n}\n"
            #         }
            data = {"operationName": "questionData", "variables": {"titleSlug": title},
                     "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}
            headers = {
                'accept': '* / *',
                'content - type': 'application / json',
                'Sec - Fetch - Mode': 'cors',
                'X - NewRelic - ID': 'UAQDVFVRGwEAXVlbBAg =',
                'x-csrftoken': csrftoken.group(1),
                'referer': problemUrl,
                'content-type': 'application/json',
                'origin': 'https://leetcode.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
            }
            cookies = {'__cfduid': 'd4319e9266fc61827dc9550eeb9cb17271572087587',
                       '_ga': 'GA1.2.5783653.1525271604',
                       '_gid': 'GA1.2.344320119.1533189808',
                       'csrftoken': csrftoken.group(1),
                       ' _gat': '1'}
            # payload表单为json格式

            dumpJsonData = json.dumps(data)
            response = requests.post(url, data=dumpJsonData, headers=headers, cookies=cookies)
            response.raise_for_status()
            print(title,response.json()['data']['question']['likes'])
            return response.json()['data']['question']['likes']
        except Exception as e:
            print("error with：" + problemUrl)
    def sort(self):
        self.Q.sort(key=lambda x:x['points'],reverse=True)#降序
        f = open("D:\LeetCode\leetcode.txt", mode='w')
        f.write("LeetCode Medium problems sorted results")
        for q in self.Q:
            print(q)
            f.write(str(q) + '\r\n')
        f.close()
        print("结果写入完成");
if __name__ == '__main__':
    baseUrl = 'https://leetcode.com/api/problems/all/'
    url_pre = ''
    local_path = "D:\leetcode.txt"#结果文件写入路径
    if not os.path.exists(local_path):
        os.mkdir(local_path)
    headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
               }
    s = Spider(baseUrl=baseUrl,local_path=local_path,difficulty=2)
    if(s.GetHtml(url="", header=headers)):
        s.GetMes()#获取所有题目的id和英文对应名称
        s.GetPoints()#获取点赞数目
    exit()
