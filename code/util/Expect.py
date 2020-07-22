import math

def getExpect(record,divide):
    # 验证是否符合正态分布
    def normal_judge():

        if len(record)<=3:
            return -1
        k = -1
        n = len(record)
        o1 = pow(6 * (n - 2) / ((n + 1) * (n + 3)), 0.5)
        o2 = pow(24 * n * (n - 2) * (n - 3) / ((n + 1) * (n + 1) * (n + 3) * (n + 5)), 0.5)
        u2 = 3 - 6 / (n + 1)

        # 求k阶样本矩
        def helper1(k):
            res = 0
            for i in range(len(record)):
                res += pow(record[i], k)
            return res / len(record)

        # k阶样本矩
        A1 = helper1(1)
        A2 = helper1(2)
        A3 = helper1(3)
        A4 = helper1(4)

        # 样本中心距
        B2 = A2 - A1 * A1
        B3 = A3 - 3 * A2 * A1 + 2 * pow(A1, 3)
        B4 = A4 - 4 * A3 * A1 + 6 * A2 * pow(A1, 2) - 3 * pow(A1, 4)

        # 偏度&峰度
        if B2<=0 or B2 <=0:
            return -1
        g1 = B3 / pow(B2, 1.5)
        g2 = B4 / pow(B2, 2)

        flag_normal = False

        if o1<=0 or o2<=0:
            return -1
        if (abs(g1 / o1) < 1.96 or abs(g2 - u2) / o2 < 1.96):
            flag_normal = True

        # 符合正态分布，利用极大似然估计得出u为一阶样本矩，再求期望
        if (flag_normal):
            return helper1(1)
        else:
            return -1

    # 验证是否为均匀分布
    def uniform_judge():
        if len(record)==0:
            return -1
        k = -1
        # 通过极大似然估计计算a,b
        a = min(record)
        b = max(record)
        n = len(record)
        # 若所有数据值均相同，则直接返回100-a
        if (a == b):
            return a


        fi = []
        for i in range(0, len(divide)-1):
            temp = 0
            for j in record:
                if (i == 0):
                    if (j >= divide[i] and j <= divide[i+1]):
                        temp += 1
                else:
                    if (j > divide[i] and j <= divide[i+1]):
                        temp += 1
            fi.append(temp)
        npi = []
        for i in range(0, len(divide)-1):
            m1 = 0
            m2 = 0
            if divide[i] >= b:
                m1 = 1
            elif divide[i] > a and divide[i] < b:
                m1 = (i * 10 - a) / (b - a)
            if divide[i+1] >= b:
                m2 = 1
            elif divide[i+1] > a and divide[i+1] < b:
                m2 = (divide[i+1] - a) / (b - a)
            npi.append(n * (m2 - m1))
        fi_combine = []
        npi_combine = []
        index = 0
        while index < len(divide)-1:
            fi_temp = 0
            npi_temp = 0
            while index < len(divide)-1 and npi[index] <= 0:
                fi_temp += fi[index]
                index += 1
            npi_temp = npi[index]
            index += 1
            while index < len(divide)-1 and npi[index] <= 0:
                fi_temp += fi[index]
                index += 1
            fi_combine.append(fi_temp)
            npi_combine.append(npi_temp)

        k2 = 0
        for i in range(len(fi_combine)):
            k2 += fi_combine[i] * fi_combine[i] / npi_combine[i]
        k2 -= n
        X_map = {}
        X_map[1] = 2.706
        X_map[2] = 4.605
        X_map[3] = 6.251
        X_map[4] = 7.779
        X_map[5] = 9.236
        X_map[6] = 10.645
        X_map[7] = 12.017
        X_map[8] = 13.362
        X_map[9] = 14.684
        X_map[10] = 15.987
        flag_uniform = False

        if len(fi_combine) - 2 - 1 <= 0:
            return -1
        if k2 < X_map[len(fi_combine) - 2 - 1]:
            flag_uniform = True

        # 符合正态分布，利用极大似然估计得出u为一阶样本矩，再求期望
        if (flag_uniform):
            return (a + b) / 2
        else:
            return -1

    # 验证是否为指数分布
    def index_judge():
        if len(record)==0:
            return -1
        k = -1
        # 通过极大似然估计计算theta
        x = sum(record) / len(record)
        n = len(record)
        fi = []
        for i in range(0, len(divide)-1):
            temp = 0
            for j in record:
                if (i == 0):
                    if (j >= divide[i] and j <= divide[i+1]):
                        temp += 1
                else:
                    if (j > divide[i] and j <= divide[i+1]):
                        temp += 1
            fi.append(temp)
        npi = []
        for i in range(0, len(divide)-1):
            npi.append(n * (math.exp(-divide[i] / x) - math.exp(-divide[i+1] / x)))
        k2 = 0
        for i in range(len(fi)):
            k2 += fi[i] * fi[i] / npi[i]
        k2 -= n
        X_map = {}
        X_map[1] = 2.706
        X_map[2] = 4.605
        X_map[3] = 6.251
        X_map[4] = 7.779
        X_map[5] = 9.236
        X_map[6] = 10.645
        X_map[7] = 12.017
        X_map[8] = 13.362
        X_map[9] = 14.684
        X_map[10] = 15.987
        flag_index = False

        if k2 < X_map[len(fi) - 2 - 1]:
            flag_index = True

        # 符合正态分布，利用极大似然估计得出x为一阶样本矩，再求期望
        if (flag_index):
            return x
        else:
            return -1

    # 当数据不符合上面任何一种分布时
    def directByExpect():
        score_map = {}
        n = len(record)
        for i in record:
            if i not in score_map:
                score_map[i] = 1
            else:
                score_map[i] = score_map[i] + 1
        score = 0
        for i in score_map.keys():
            score += i * score_map[i] / n
        return score

    if normal_judge() != -1:
        return  normal_judge()
    elif uniform_judge() != -1:
        return uniform_judge()
    elif index_judge() != -1:
        return index_judge()
    else:
        return directByExpect()