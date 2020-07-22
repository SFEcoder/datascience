import json
from util import Expect

with open('test_data.json', 'r', encoding='UTF-8') as file:
    data = json.load(file)
# 所选题目的id
dif_map={}
case_map={}
for key in data:
    # 获取用户所有的提交记录
    cases = data[key]["cases"]
    for i in range(len(cases)):
        case = cases[i]
        case_map[case["case_id"]]=1
divide=[]
for i in range(0,11):
    divide.append(i*10)
for case_id in case_map.keys():
    score_record = []
    for key in data:
        # 获取用户所有的提交记录
        cases = data[key]["cases"]
        for i in range(len(cases)):
            case = cases[i]
            if case["case_id"] == case_id:
                upload_records = case["upload_records"]
                for j in range(len(upload_records)):
                    score_record.append(upload_records[j]["score"])
    dif_map[case_id]= 100 - Expect.getExpect(score_record, divide)

