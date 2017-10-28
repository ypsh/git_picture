# -*- coding: UTF-8 -*-
import requests
import re
import time
import logging
import json


def dowmloadPic(html):
    url = re.findall(r'src=.*?.jpg', html, re.IGNORECASE)
    logging.info( "this page cotain pic: " + str(url.__len__()) )

    # logging.info(url)
    i = 0
    for each in url:
        each = each.replace("src=\"","")
        # print each
        if each.__len__() < 100 :
            logging.info( "path:  " + each )
            try:
                pic = requests.get(each)
            except requests.exceptions.ConnectionError:
                logging.info("can not download")

            if re.match(".*?.jpg", each, re.IGNORECASE) is not None:
                string = 'meimeimei\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))+ str(i) + '.jpg'
            elif re.match(".*?.png", each, re.IGNORECASE) is not None:
                string = 'meimeimei\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())) + str(i) + '.png'
            elif re.match(".*?.gif", each, re.IGNORECASE) is not None:
                string = 'meimeimei\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())) + str(i) + '.gif'
                # resolve the problem of encode, make sure that chinese name could be store
            fp = open(string.decode('utf-8').encode('cp936'), 'wb')
            fp.write(pic.content)
            fp.close()
            i += 1

def initallog(self,logpath):
        # 设置全局日志
        if logpath != "":
            self.logpath = logpath
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s -- %(funcName)s s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%Y-%M-%d %H:%M:%S',
                                filename='log.log',
                                filemode='w'
                                )  # filemode='w' 模式覆盖原日志

            #################################################################################################
            # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
            #################################################################################################
        else:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s -- %(funcName)s s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%Y-%M-%d %H:%M:%S',
                                filename='log.log',
                                filemode='w'
                                )  # filemode='w' 模式覆盖原日志

            #################################################################################################
            # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
            #################################################################################################


def get_html_url(url):
    htmlsUrl =[]
    while True:
        try:
            result = requests.get(url)
            htmlResult = re.findall(r'"id":.*?\d{4}', result.text, re.IGNORECASE)
            htmls = list(set(htmlResult))
            # print htmls
            break
        except:
            logging.info("timeout")
    for item in htmls:
        if item.__len__()<100:
            htmlsUrl.append(item.replace("\"id\":\"",""))
        # print htmlsUrl
    return htmlsUrl

def writefile(data):
    path = "meimeimei.txt"
    file_object = open(path, 'a')
    file_object.writelines(data)
    file_object.close()
def readfile():
    lines = []
    path = "meimeimei.txt"
    file_object = open(path, 'r')
    line = file_object.readlines()
    file_object.close()
    for item in line:
        lines.append(item.replace("\n",""))
    return lines


if __name__ == '__main__':
    url = "http://m.78seo.com/ajaxlist.php?cate=2&page=2&pagenum=1&pagesize=500"
    initallog("","")
    ID = get_html_url(url)
    basurl = "http://m.78seo.com/n.php?id="
    # logging.info(url)
    htmlsUrl = get_html_url(url)
    # logging.info(htmlsUrl)
    his = readfile()
    for item in ID:
        url = basurl + str(item)
        if his.__contains__(item) == False:
            for a in range(1, 3):
                try:
                    result = requests.get(url)
                    logging.info("requests_time" + str(result.elapsed.microseconds))
                    writefile(item + "\n")
                    logging.info("download:" + url)
                    break
                except:
                    logging.info("countniu:" + str(a))
                    # time.sleep(2)
            string = result.text
            dowmloadPic(string)


    #
    # result = requests.get("http://m.78seo.com/n.php?id=1002")
    # string = result.text
    # dowmloadPic(string)
    # print string
