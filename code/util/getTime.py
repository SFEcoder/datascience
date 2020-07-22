import time


# 根据时间戳获取时间，返回结果格式： 2020-07-01
def getDate(timeNum):
    timeStamp = float(timeNum / 1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
    return otherStyleTime


# 获取时间对应的当天的分数值（用于进行时间间隔计算）
def getMinuteAbsoluteInDay(timeInput):
    hourAndMin = timeInput.split(":")
    hour = int(hourAndMin[0])
    minute = int(hourAndMin[1])
    return 60 * hour + minute


# 毫秒转分钟
def milisecond2minute(milisecond):

    return milisecond / (1000 * 60)
