import requests
import json
import datetime
import time
import logging
import sys
sys.path.append(".")
import settings
from data_collection.db_admin import HotList_DB_Admin

log = logging.getLogger()


class Hot_List_Data():
    question_id = None
    title = None
    answer_count = None
    heat = None
    create_time = None

class Zhihu_Client():
    hot_list_url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
    question_url = "https://www.zhihu.com/question/"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }

    def request_hot_list(self):
            try:
                res = requests.get(self.hot_list_url, headers=self.headers)
                data = res.json()["data"]
            except Exception as e:
                log.error(e)
                log.error("request failed")
                return

            hot_list_result = []
            for item in data:
                try:
                    hot_list_data = Hot_List_Data()
                    hot_list_data.title = item["target"]["title"]
                    if "热度" in item["detail_text"]:
                        hot_list_data.heat = int(round(float(item["detail_text"].replace(" ", "").split("万热度")[0])))
                    else:
                        hot_list_data.heat = 0
                    hot_list_data.answer_count = item["target"]["answer_count"]
                    hot_list_data.question_id = item['target']['url'].split("questions/")[-1]
                    hot_list_data.create_time = item['target']['created']
                    hot_list_result.append(hot_list_data)
                except Exception as e:
                    log.error("assemble data error")
                    log.exception(e)
            # log.debug(hot_list_result)
            self.save_data(hot_list_result)

    def request_question(self, question_id):
        res = requests.get(self.question_url + str(question_id), headers=self.headers)
        if res.status_code == 404:
            log.info("【404】question %s not found", self.question_url + question_id)
            return False
        return True

    def save_data(self, hot_list_result):
        for index, tmp_data in enumerate(hot_list_result):
            try:
                data = {}
                record = HotList_DB_Admin().query_record_by_id(question_id=tmp_data.question_id)
                # 组装question_id
                data["question_id"] = tmp_data.question_id
                # 组装title
                data["title"] = tmp_data.title
                # 组装first_onrank_time
                if record and record.first_onrank_time:
                    data["first_onrank_time"] = record.first_onrank_time
                else:
                    data["first_onrank_time"] = datetime.datetime.today()
                # 组装answer_count
                data["answer_count"] = tmp_data.answer_count
                # 组装highest_rank
                if record and record.highest_rank and record.highest_rank <= index + 1:
                    data["highest_rank"] = record.highest_rank
                else:
                    data["highest_rank"] = index + 1
                # 组装highest_heat
                if record and record.highest_heat and record.highest_heat >= tmp_data.heat:
                    data["highest_heat"] = record.highest_heat
                else:
                    data["highest_heat"] = tmp_data.heat
                # 组装cancelled
                if record and record.cancelled == 1:
                    data["cancelled"] = 1
                else:
                    data["cancelled"] = 0
                # 组装question_create_time
                data["question_create_time"] = datetime.datetime.fromtimestamp(tmp_data.create_time)
                HotList_DB_Admin().update_record(**data)
            except Exception as e:
                log.error("save hot list data error")
                log.exception(e)

        log.info("save hot list data done at %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

def main():
    zhihu_client = Zhihu_Client()
    zhihu_client.request_hot_list()
    # zhihu_client.request_question(question_id="517793282")
    # url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
    # headers = {
    #     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    # }
    # # sess = requests.Session()
    # # res = sess.get(url, headers=headers)
    # res = requests.get(url, headers=headers)
    # data = res.json()["data"]
    # hot_list = []
    # for item in data:
    #     # id = item["target"]["id"]
    #     title = item["target"]["title"]
    #     hot_list.append(title)

    # print(hot_list)


if __name__ == '__main__':
    main()
