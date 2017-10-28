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
            i= 0
            if not self.que.empty():
                each = self.que.get()
                a = random.randint(0, 30)
                each=str.replace(each,"\n","")
                print "path:  " + each
                try:
                    pic = requests.get(each, timeout=30)
                except requests.exceptions.ConnectionError:
                    logging.info("can not download")
                    continue
                if re.match(".*?.jpg", each, re.IGNORECASE) is not None:
                    string = 'gif\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())) + '.jpg'
                elif re.match(".*?.png", each, re.IGNORECASE) is not None:
                    string = 'gif\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())) + '.png'
                elif re.match(".*?.gif", each, re.IGNORECASE) is not None:
                    string = 'gif\\' + time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())) + '.gif'
                    # resolve the problem of encode, make sure that chinese name could be store
                fp = open(string.decode('utf-8').encode('cp936'), 'wb')
                fp.write(pic.content)
                fp.close()
                i += 1
                # urlretrieve(host, '%d.png' % a)
            else:
                break


def Down():
    f = open('F:\code\Gitpicture\gif.txt', 'r')
    a = f.readlines()
    f.close()
    que = Queue.Queue()
    threads = []
    for i in a:
        que.put(i)
    for i in range(500):
        d = download(que)
        threads.append(d)
    for i in threads:
        i.start()
    for i in threads:
        i.join()


if __name__ == '__main__':
    start = time.time()
    Down()
    end = time.time()
    print(end - start)