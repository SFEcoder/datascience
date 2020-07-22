from util.prepareGapRange import *
from Entities.Hill import *
from Entities.User import *
from Entities.Case import *
from util.getTime import *

user_list = []
upload_hill_list = []  # 所有用户的波峰的列表       里面的一个元素代表：一个用户的所有upload波峰
hill_list = []  # 所有用户的波峰的列表     里面的一个元素代表：一个用户的所有case(题目)波峰
upload_list_of_single_user = []  # 一个用户的所有提交


def get_case_hill_by_uploads(single_upload_list):
    # 获取题目波峰
    single_case_list = []
    current_case_id = single_upload_list[0].case.caseId
    time_spent = 0
    max_score = single_upload_list[0].score
    i = 1
    while i < len(single_upload_list):
        while single_upload_list[i].case.caseId == current_case_id:
            max_score = max(max_score, single_upload_list[i].score)
            time_spent += single_upload_list[i].timeGap
            if i == len(single_upload_list) - 1:
                caseE = Case(single_upload_list[i].case.caseId)
                caseE.work_time = time_spent
                caseE.difficulty = single_upload_list[i].case.difficulty
                caseE.score = max_score
                single_case_list.append(caseE)
                return single_case_list[1:]
            i += 1
        current_case_id = single_upload_list[i].case.caseId
        # 把刚刚的case加进列表里
        caseE = Case(single_upload_list[i - 1].case.caseId)
        caseE.work_time = time_spent
        caseE.difficulty = single_upload_list[i].case.difficulty
        caseE.score = max_score
        single_case_list.append(caseE)
        time_spent = 0
        max_score = single_upload_list[i].score

    # 去掉第一个元素，因为无法获取它花费的时间，将其剔除
    return single_case_list[1:]


# dicJsonGot 在prepareGapRange文件里，是json.loads的结果
for userIdKey in dicJsonGot:
    userEntity = User()
    userEntity.id = userIdKey
    user_list.append(userEntity)
    cases = dicJsonGot[userIdKey]['cases']
    upload_list_of_single_user = get_all_uploads_of_one(cases)
    single_hill = []
    upload_hill_list_of_one_person = []
    for upload in upload_list_of_single_user:
        rightLimit = upload_gap_reasonable_ranges[upload.get_difficulty_level()][1]
        leftLimit = 0
        gap_minute = milisecond2minute(upload.timeGap)
        if gap_minute >= leftLimit and gap_minute < rightLimit:
            single_hill.append(upload)
            if upload == upload_list_of_single_user[-1]:
                if len(single_hill) != 0:
                    upload_hill_list_of_one_person.append(single_hill)
        else:
            if len(single_hill) != 0:
                upload_hill_list_of_one_person.append(single_hill)
            single_hill = []

    upload_hill_list.append(upload_hill_list_of_one_person)

    # 清空
    upload_hill_list_of_one_person = []

# 下面获取波峰的题目格式, 结果在hill_list中
user_pointer = 0
for uploadHillsOfOne in upload_hill_list:
    user = user_list[user_pointer]
    caseHillsOfOne = []  # 一个人的case波峰
    for upload_hill in uploadHillsOfOne:
        hill = get_case_hill_by_uploads(upload_hill)
        if len(hill) != 0:
            hillEntity = Hill()
            hillEntity.cases = hill
            # 确定始末时间
            startCaseId = upload_hill[0].case.caseId
            for upload in upload_hill:
                if upload.case.caseId != startCaseId:
                    hillEntity.startTime = upload.get_upload_minute()
                    break
            hillEntity.endtime = upload_hill[-1].get_upload_minute()
            # 确定始末时间
            caseHillsOfOne.append(hillEntity)
    if len(caseHillsOfOne) != 0:
        hill_list.append(caseHillsOfOne)
    user.hills = caseHillsOfOne
    user_pointer += 1


# caseHillsOfOne = user_list[1].hills
# for caseHills in caseHillsOfOne:
#     print("波峰开始时间：", caseHills.startTime)
#     for case in caseHills.cases:
#         print(milisecond2minute(case.work_time), "题目编号：", case.caseId, "最高分", case.score, "题目难度：", case.difficulty)
#     print("波峰结束时间: ", caseHills.endtime)
#     print()
#     print()


