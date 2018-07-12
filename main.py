import json
import threading
from time import sleep
from urllib.parse import urlencode

import requests

# 线程数
thread_num = 10
# 关键字
keyword = '妹子'


class taskThread(threading.Thread):
    def __init__(self, threadID, keyword):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.keyword = keyword

    def run(self):
        global overTask
        params = {
            'q': self.keyword,
            'limit': 20,
            'start': (self.threadID - 1) * 20
        }
        url = 'https://www.douban.com/j/search_photo?' + urlencode(params)
        resp = requests.get(url)
        if resp.status_code == 200:
            # print('图片api成功请求成功' + url)
            parsed_json = json.loads(resp.text)
            array = parsed_json['images']
            for a in array:
                self.download(a['src'])
            overTask.append(self.threadID)

    def download(self, url):
        # print('download 被调用')
        global number
        global threadLock
        ir = requests.get(url, stream=True)
        filename = str.split(url, '/')
        if ir.status_code == 200:
            threadLock.acquire()
            number = number + 1
            # print('线程' + str(self.threadID) + '--开始写入第' + str(number) + "张" + filename[len(filename) - 1])
            with open('mz/' + filename[len(filename) - 1], 'wb') as f:
                for chunk in ir:
                    f.write(chunk)
            f.close()
            print('线程' + str(self.threadID) + '--成功写入第' + str(number) + "张")
            threadLock.release()


threads = []
overTask = []
number = 0
threadLock = threading.Lock()
useTime = 0
while thread_num > 0:
    threads.append(taskThread(thread_num, keyword))
    thread_num = thread_num - 1

for t in threads:
    print('开始线程：' + str(t.threadID))
    t.start()

while True:
    if len(overTask) == thread_num:
        print("总耗时：" + str(useTime) + "s")
        exit(0)
    useTime += 1
    sleep(1)



