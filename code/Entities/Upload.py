from util.getTime import *


# Upload实体类
class Upload:
    def __init__(self, timeStamp):

        # 提交的时间戳
        self.uploadTimeStamp = timeStamp

        # 提交所属题目
        self.case = {}

        # 上一次提交和此提交的间隔 （毫秒）
        self.timeGap = 0

        # 提交的绝对分钟数
        self.uploadMinute = getMinuteAbsoluteInDay(self.get_upload_time24())

        # 提交的分数
        self.score = 0



    def get_std_upload_time(self):
        # 提交的标准日期，格式： 2020-05-25 19：20
        return getDate(self.uploadTimeStamp)

    def get_upload_date(self):
        # 提交的日期 2020-02-25
        return getDate(self.uploadTimeStamp).split(" ")[0]

    def get_upload_time24(self):
        return getDate(self.uploadTimeStamp).split(" ")[1]

    def get_upload_minute(self):
        return getMinuteAbsoluteInDay(self.get_upload_time24())

    def get_difficulty_level(self):
        return int(self.case.difficulty // 10)