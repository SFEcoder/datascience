import numpy as np


# 获取排序号的一组数的第x四分位数
def get4NumByX(x, numss):
    nums = sorted(numss)

    if x == 1:
        raw = 0.25 * (len(nums) + 1)
        if int(raw) == raw:
            return nums[int(raw) - 1]
        return 0.25 * nums[int(raw) - 1] + 0.75 * nums[int(raw)]
    elif x == 2:
        raw = 0.5 * (len(nums) + 1)
        if int(raw) == raw:
            return nums[int(raw) - 1]
        return 0.5 * nums[int(raw) - 1] + 0.5 * nums[1 + int(raw) - 1]
    elif x == 3:
        raw = 0.75 * (len(nums) + 1)
        if raw == int(raw):
            return nums[int(raw) - 1]
        return 0.75 * nums[int(raw) - 1] + 0.25 * nums[int(raw)]
    return -1


