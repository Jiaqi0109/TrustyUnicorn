import numpy as np


def city_json(cities):
    nd_city = np.array(cities)
    # 标签列表
    s_city = list({c for c in nd_city})
    # 各标签的个数
    nums = [np.sum(nd_city == c) for c in s_city]
    data = []
    for name, value in zip(s_city, nums):
        data.append({"name": name, "value": str(value)})
    # 数据排序
    data = sorted(data, key=lambda x: int(x["value"]), reverse=True)

    return data


def education_workyear_json(educations, workyears):
    nd_educations = np.array(educations)
    nd_workyears = np.array(workyears)

    # 需要排序
    # 排序方法！！
    e_sort = ['学历不限', '大专及以上', '本科及以上', '硕士及以上', '博士及以上']
    w_sort = ['不限', '应届毕业生', '1年以下', '1-3年', '3-5年', '5-10年', '10年以上']

    e_name = list({e for e in nd_educations})
    e_name = sorted(e_name, key=e_sort.index)
    e_nums = [np.sum(nd_educations == e) for e in e_name]

    w_name = list({w for w in nd_workyears})
    w_name = sorted(w_name, key=w_sort.index)
    w_nums = [np.sum(nd_workyears == w) for w in w_name]

    edu_data = []
    work_data = []
    for name, value in zip(e_name, e_nums):
        edu_data.append({"name": name, "value": str(value)})
    for name, value in zip(w_name, w_nums):
        work_data.append({"name": name, "value": str(value)})

    return edu_data, work_data

# TODO 需要处理异常
def salary_json(salaries):
    data = []
    salary = []
    salary_d = [s.replace('k', '').replace('K', '').replace('以上', '-').replace('+', '-') for s in salaries]
    for s in salary_d:
        min, max = s.split('-')[:2]
        if not max:
            if min == '100':
                max = '110'
            else:
                max = int(int(min) * 1.5)
        for i in range(int(min), int(max) + 1):
            salary.append(i)
    nd_salarys = np.array(salary)
    s_name = list({s for s in nd_salarys})
    s_name = sorted(s_name)
    s_nums = [np.sum(nd_salarys == s) for s in s_name]
    for name, value in zip(s_name, s_nums):
        data.append({"name": str(name * 1000), "value": str(value)})

    return data


def salary_amm(salaries):
    salary = []
    salary_d = [s.replace('k', '').replace('K', '').replace('以上', '-').replace('+', '-') for s in salaries]
    for s in salary_d:
        salary += s.split('-')
    salary = [int(s) for s in salary if s]
    s_min = min(salary) * 1000
    s_max = max(salary) * 1000
    s_avg = round((sum(salary) / len(salary)), 3) * 1000
    return s_min, s_max, s_avg
