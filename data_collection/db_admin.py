from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Sequence, VARCHAR, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
import sys
sys.path.append(".")
import settings
import logging
import datetime

log = logging.getLogger()


Base = declarative_base()
engine_url = "mysql://" + settings.config["db_config"].db_config["user"] + \
            ":" + settings.config["db_config"].db_config["passwd"] + "@" + \
            settings.config["db_config"].db_config["host"] + "/" + settings.config["db_config"].db_config["db"]
engine = create_engine(engine_url, encoding=settings.config["db_config"].db_config["charset"], echo=False)


class Zhihu_Hot_List(Base):
    __tablename__ = "zhihu_hot_list"
    question_id = Column(String(10), primary_key=True, default="default")
    title = Column(String(100))
    update_time = Column(DateTime(), default=datetime.datetime.today, onupdate=datetime.datetime.today)
    question_create_time = Column(DateTime())
    first_onrank_time = Column(DateTime())
    answer_count = Column(Integer())
    highest_rank = Column(Integer())
    highest_heat = Column(Integer())
    cancelled = Column(Boolean(), default=False)


class HotList_DB_Admin():
    Session = sessionmaker(bind=engine)

    def query_record_by_id(self, question_id):
        session = self.Session()
        ret = None
        try:
            ret = session.query(Zhihu_Hot_List).filter(Zhihu_Hot_List.question_id == question_id).all()
            if ret:
                ret = ret[0]
        except Exception as e:
            log.error('database query exception')
            log.exception(e)
            session.rollback()
            return None
        except NoResultFound:
            pass
        finally:
            session.close()

        return ret

    def update_record(self, **data):
        session = self.Session()
        try:
            tmp_record = Zhihu_Hot_List(
                question_id=data["question_id"],
                title=data["title"],
                first_onrank_time=data["first_onrank_time"],
                answer_count=data["answer_count"],
                highest_rank=data["highest_rank"],
                highest_heat=data["highest_heat"],
                cancelled=data["cancelled"],
                question_create_time=data["question_create_time"]
            )
            session.merge(tmp_record)
        except Exception as e:
            log.error("update record error")
            log.exception(e)
            session.rollback()
            return False
        else:
            session.commit()
            log.debug("update record [%s] success" % data)
        finally:
            session.close()

        return True

# hotlist_admin = HotList_DB_Admin()
# data = {
#     "question_id": "12345",
#     "title": "test",
#     "first_onrank_time": datetime.datetime.today(),
#     "question_create_time": datetime.datetime.today(),
#     "answer_count": 2343,
#     "highest_rank": 1,
#     "highest_heat": "1233 万热度",
#     "cancelled": True,
# }
# hotlist_admin.update_record(**data)
# Session = sessionmaker(bind=engine)
# session = Session()
# result = session.query(Zhihu_Hot_List).filter((Zhihu_Hot_List.case_id == 119)).all()
# print(result)
# Base.metadata.create_all(engine)
