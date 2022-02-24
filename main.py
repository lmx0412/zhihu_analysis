from spider.zhihu_request import Zhihu_Client
import time

def main():
    while True:
        zhihu_client = Zhihu_Client()
        zhihu_client.request_hot_list()
        time.sleep(5*60)

if __name__ == '__main__':
    main()
