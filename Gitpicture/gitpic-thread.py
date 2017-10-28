# -*- coding: UTF-8 -*-
# from urllib.request import urlretrieve
import requests
import Queue
import threading
import random
import time
import re
import logging


class download(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que
    def initallog(self, logpath):
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

    def run(self):
        while True:
            i = 0
            if not self.que.empty():
                each = self.que.get()
                his = download("").readfile()
                basurl = 'http://cl.c34u.me/'
                if his.__contains__(each) == False:
                    url = basurl + each
                    try:
                        result = requests.get(url, timeout=10)
                        gifusrls = re.findall(r'http.*?.jpg', result, re.IGNORECASE)
                        for gif in gifusrls:
                            download("").writefile(gif + "\n")
                        break
                    except:
                        logging.info("countniu")


            else:
                break

    def Down(self,items):
        a = items
        que = Queue.Queue()
        threads = []
        for i in a:
            que.put(i)
        for i in range(20):
            d = download(que)
            threads.append(d)
        for i in threads:
            i.start()
        for i in threads:
            i.join()

    def dowmloadPic(self,html):
        print "Start"
        url = re.findall(r'http.*?.gif', html, re.IGNORECASE)
        # url = url + re.findall(r'http.*?.png', html, re.IGNORECASE)
        # url = url + re.findall(r'http.*?.gif', html, re.IGNORECASE)
        i = 0
        for each in url:
            if each.__len__() < 100 & each.find("\\") != -1:
                print "path:  " + each
                try:
                    download("").writefilepath(each + "\n")
                    # pic = requests.get(each, timeout=3)
                except requests.exceptions.ConnectionError:
                    logging.info("can not download")
                    continue
                    # if re.match(".*?.jpg", each, re.IGNORECASE) is not None:
                    #     string = '2048\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())) + '.jpg'
                    # elif re.match(".*?.png", each, re.IGNORECASE) is not None:
                    #     string = '2048\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())) + '.png'
                    # elif re.match(".*?.gif", each, re.IGNORECASE) is not None:
                    #     string = '2048\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())) + '.gif'
                    #     # resolve the problem of encode, make sure that chinese name could be store
                    # fp = open(string.decode('utf-8').encode('cp936'), 'wb')
                    # fp.write(pic.content)
                    # fp.close()
                    # i += 1

    def get_html_url(self,url):
        htmlsUrl = []
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
            htmlsUrl.append(item.replace("href=\"", ""))
            # print htmlsUrl
        return htmlsUrl

    def writefile(self,data):
        path = "history.txt"
        file_object = open(path, 'a')
        file_object.writelines(data)
        file_object.close()

    def writefilepath(self,data):
        path = "gif.txt"
        file_object = open(path, 'a')
        file_object.writelines(data)
        file_object.close()

    def readfile(self):
        lines = []
        path = "history.txt"
        file_object = open(path, 'r')
        line = file_object.readlines()
        file_object.close()
        for item in line:
            lines.append(item.replace("\n", ""))
        return lines

    def allinos(self):
        download("").initallog("")
        for i in range(1, 200):
            url = 'http://cl.c34u.me/thread0806.php?fid=7&search=&page=' + str(i)
            logging.info(url)
            htmlsUrl = download("").get_html_url(url)
            download("").Down(htmlsUrl)





if __name__ == '__main__':
    start = time.time()
    download("").allinos()
    end = time.time()
    print(end - start)
