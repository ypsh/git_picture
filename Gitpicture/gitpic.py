# -*- coding: UTF-8 -*-
import requests
import re
import time
import logging


def dowmloadPic(html):
    print "Start"
    url = re.findall(r'http.*?.jpg', html, re.IGNORECASE)
    url = url + re.findall(r'http.*?.png', html, re.IGNORECASE)
    url = url + re.findall(r'http.*?.png', html, re.IGNORECASE)
    i = 0
    try:
       for each in url:
        if each.__len__() < 100 & each.find("\\") != -1:
            print "path:  " + each
            try:
                writefilepath(each + "\n")
                pic = requests.get(each, timeout=3)
            except requests.exceptions.ConnectionError:
                logging.info("can not download")
                continue
            if re.match(".*?.jpg", each, re.IGNORECASE) is not None:
                string = '1024\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())) + '.jpg'
            elif re.match(".*?.png", each, re.IGNORECASE) is not None:
                string = '1024\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())) + '.png'
            elif re.match(".*?.gif", each, re.IGNORECASE) is not None:
                string = '1024\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())) + '.gif'
                # resolve the problem of encode, make sure that chinese name could be store
            fp = open(string.decode('utf-8').encode('cp936'), 'wb')
            fp.write(pic.content)
            fp.close()
            i += 1
    except requests.exceptions.ConnectionError:
                logging.info("exception")

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
            console.setLevel(logging.DEBUG)
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
            console.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
            #################################################################################################


def get_html_url(url):
    htmlsUrl =[]
    while True:
        try:
            result = requests.get(url)
            htmlResult = re.findall(r'href.*?.html', result.text, re.IGNORECASE)
            htmls = list(set(htmlResult))
            print htmls.__len__()
            break
        except:
            logging.info("timeout")

    for item in htmls:
        htmlsUrl.append(item.replace("href=\"",""))
        # print htmlsUrl
    return htmlsUrl

def writefile(data):
    path = "history.txt"
    file_object = open(path, 'a')
    file_object.writelines(data)
    file_object.close()
def writefilepath(data):
    path = "path.txt"
    file_object = open(path, 'a')
    file_object.writelines(data)
    file_object.close()
def readfile():
    lines = []
    path = "history.txt"
    file_object = open(path, 'r')
    line = file_object.readlines()
    file_object.close()
    for item in line:
        lines.append(item.replace("\n",""))
    return lines


if __name__ == '__main__':
    initallog("","")
    for i in range(1,10):
        url = 'http://cl.c34u.me/thread0806.php?fid=8&search=&page='+ str(i)
        logging.info(url)
        basurl = 'http://cl.c34u.me/'
        htmlsUrl = get_html_url(url)
        his = readfile()
        for item in htmlsUrl:
            if his.__contains__(item) == False:
                url = basurl + item
                for a in range(1,2):
                        try:
                            result = requests.get(url,timeout=3)
                            print result.elapsed.microseconds
                            writefile(item + "\n")
                            break
                        except:
                            logging.info("countniu:" + str(a))
                            continue
                            # time.sleep(2)
                try:
                    string = result.text
                    dowmloadPic(string)
                except:
                    continue
