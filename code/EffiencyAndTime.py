from Entities.User import *
from util.Expect import *
from util.getTime import *
from util.getHill import *
from util.getEffciency import *


def get_hill_length(start, end):
    # start是开始的分钟戳， end是结束分钟戳
    if end >= start:
        return end - start
    else:
        #  比如 23:00（分钟戳23 * 60)   开始， 1：00（分钟戳60）结束
        return 24 * 60 - start + end


def sum_two_dimision(nums):
    outcome = 0
    for i in nums:
        outcome += i[0]
    return outcome


def get_left_right_bound_of_max_sum(nums, length):
    max_index = 0
    max_sum = 0
    for i in range(0, len(nums) - length + 1):
        _sum = sum_two_dimision(nums[i:i + length])
        if _sum > max_sum:
            max_sum = _sum
            max_index = i

    return [max_index, max_index + length - 1]


def add_effiency_by_minute(hill, eff_list_before_alter):
    # eff_list_before_alter 是一个二维数组， 每一个元素是一个二元数组，第一个元素是期望，第二个是个数
    # eff_list_before_alter 未经过转变，分钟数据从 0 升序排到 1440 - 1， （从第0小时排到23小时）
    _startTime = hill.startTime
    _endTime = hill.endtime
    eff = hill.efficiency
    _range = []
    if _startTime <= _endTime:
        _range = [i for i in range(_startTime, _endTime + 1)]

    else:
        #         start: 1439   end 3
        _range = [i for i in range(_startTime, 1440)] + [j for j in range(0, _endTime + 1)]

    for i in _range:
        mean = eff_list_before_alter[i][0]
        count = eff_list_before_alter[i][1]
        eff_list_before_alter[i][0] = (mean * count + eff) / (count + 1)
        eff_list_before_alter[i][1] += 1
    return eff_list_before_alter


for user in user_list:

    # 最佳编程效率时长
    besteff_time_length = 0

    # 1440个分钟的效率, (转换之前的，排序是 0 1 2 .。。 23
    effiencies_by_minute_before_alter = [[0, 0] for i in range(0, 1440)]

    # 获取用户的最佳编程效率时长（求期望）
    time_lengths = []

    # 波峰小于等于一个，数据太少了,计算误差太大
    if len(user.hills) <= 1:
        user.startTime = "提交数据不足"
        user.endTime = "需要更多提交"
        continue

    for hill in user.hills:
        time_lengths.append(get_hill_length(hill.startTime, hill.endtime))
        effiencies_by_minute_before_alter = add_effiency_by_minute(hill, effiencies_by_minute_before_alter)

    # 如果没有波峰就算了
    if len(time_lengths) == 0:
        continue

    #     用于区间拟合检验， 获取最佳编程效率时间长度
    #      getEffiency的divide
    division = []
    for i in range(0, 11):
        division.append(max(time_lengths) / 10 * i)

    #  最佳编程效率时间长度
    besteff_time_length = round(getExpect(time_lengths, division))

    # 转变分钟数组 ， 从五点开始,便于跨天计算
    effiencies_by_minute = effiencies_by_minute_before_alter[300:] + effiencies_by_minute_before_alter[:300]
    best_eff_range = get_left_right_bound_of_max_sum(effiencies_by_minute, besteff_time_length)
    best_startTime = best_eff_range[0]
    best_endTime = best_eff_range[1]
    best_startTime = (best_startTime + 300) % 1440
    best_endTime = (best_endTime + 300) % 1440
    user.startTime = best_startTime
    user.endTime = best_endTime


def tr(time):
    if type(time) == str:
        return time
    hour = str(time // 60)
    if len(str(hour)) == 1:
        hour = '0' + hour
    minute = str(time % 60)
    if len(str(minute)) == 1:
        minute = '0' + minute
    return hour + " : " + minute


for user in user_list:
    print("用户编号", user.id, "最佳时间段: ", tr(user.startTime), " —— ", tr(user.endTime))
