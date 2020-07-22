# 为难度梯度 1 - 10 的所有题目获取合理的间隔时间范围

import json
from Entities.Case import *
from Entities.Upload import *
from util.calculater import *
from util.difficultyJudge import *
import numpy as np

uploadList = []  # 所有人的所有提交记录
upload_gaps = []  # 某难度梯度下所有提交的间隔
upload_gap_reasonable_ranges = []  # 难度梯度 0 - 10 的范围
cases = []  # 所有json提交


# 获取一个用户的所有提交存到outcome中并返回
# cases_p是从json中获取的一个用户的所有提交记录
def get_all_uploads_of_one(cases_p):
    outcome = []
    for case in cases_p:
        caseEntity = Case(case['case_id'])
        uploads = case['upload_records']
        caseEntity.score = 0
        caseEntity.difficulty = dif_map[caseEntity.caseId]
        for upload in uploads:
            uploadEntity = Upload(upload['upload_time'])
            uploadEntity.case = caseEntity
            uploadEntity.score = upload['score']
            outcome.append(uploadEntity)
    # 给每个提交算上与前一个提交的时间间隔（除了第一个提交，它的时间间隔是0）
    # 按时间排序所有upload
    outcome = sorted(outcome, key=lambda x: x.uploadTimeStamp)
    for i in range(1, len(outcome)):
        outcome[i].timeGap = outcome[i].uploadTimeStamp - outcome[i - 1].uploadTimeStamp

    return outcome


# 根据难度梯度获取合理的花费时间（mu+-3sigma（正态分布））， 该难度梯度下的所有时间间隔放在gap里面
# difficulty是难度梯度
# 返回值是一个二元数组，分别为左边界和右边界
def get_reasonable_range_by_difficulty(difficulty):
    #     难度梯度 0 - 10
    upload_gaps = []  # 某难度梯度下所有提交的间隔

    uploads_matched = []
    gaps = []
    for upload in uploadList:
        if upload.case.difficulty // 10 == difficulty:
            uploads_matched.append(upload)

    for upload in uploads_matched:
        minute = milisecond2minute(upload.timeGap)
        if minute >= difficulty and minute < 180:
            gaps.append(minute)

    if len(gaps) == 0:
        return [0, 0]

    gaps = sorted(gaps)

    # 下面用箱线图初步筛选数据
    # 有效范围是 【Q1 - 1.5IQR, Q3 + 1.5IQR】
    Q1 = get4NumByX(1, gaps)
    Q3 = get4NumByX(3, gaps)
    IQR = Q3 - Q1
    leftBound = Q1 - 1.5 * IQR
    rightBound = Q3 + 1.5 * IQR
    for gap in gaps:
        if gap > leftBound and gap < rightBound:
            upload_gaps.append(gap)

    # print(upload_gaps)
    mu = np.mean(upload_gaps)
    sigma = np.std(upload_gaps)
    if len(gaps) < 50:
        #     对于样本数据过小，小于50的数据，sigma误差太大，不能用正态分布去判断，直接取箱线图的正常范围
        return [0, rightBound]
    # print(gaps)
    return [mu - 3 * sigma, mu + 3 * sigma]
    # 下面计算 mu 和 sigma


# 读取Json文件,所有人的所有提交都放在了uploadList里
f = open('test_data.json', encoding='utf-8')
content = f.read()
dicJsonGot = json.loads(content)
for key in dicJsonGot:
    cases = dicJsonGot[key]['cases']
    uploadList += get_all_uploads_of_one(cases)

for i in range(0, 11):
    upload_gap_reasonable_ranges.append(get_reasonable_range_by_difficulty(i))







