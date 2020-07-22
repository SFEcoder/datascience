
from util.getHill import *
from util.Expect import getExpect

for user in user_list:
    hills=user.hills
    for hill in hills:
        efficiency_list=[]
        max_efficiency=0
        for case in hill.cases:
            if case.work_time>0 and case.difficulty>0:
                # 获取效率
                efficiency_list.append(100*case.score / case.difficulty / milisecond2minute(case.work_time))
                max_efficiency = max(max_efficiency, 100*case.score / case.difficulty / milisecond2minute(case.work_time))
        division=[]
        for i in range(0,11):
            # 划分区间
            division.append(max_efficiency/10*i)
        if len(efficiency_list)>0:
            # 获得效率均值
            efficiency_expect = getExpect(efficiency_list, division)
            hill.efficiency = efficiency_expect
# for user in user_list:
#     for hill in user.hills:
#         print("波峰开始时间：", hill.startTime)
#         print("user_id ", user.id,"efficiency",hill.efficiency)
#         print("波峰结束时间：", hill.endtime)
