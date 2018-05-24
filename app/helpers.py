import numpy as np
import jieba
import jieba.analyse
import jieba.posseg as psg

from app.models.company import Company
from app.models.position import Position


def description_cy(detail):
    import re

    lines = []
    keyWords = ['精通', '熟悉', '掌握', '了解', '编写', '开发', '理解', '熟练', '能力', '维护', '负责', '参与', '作品']
    details = detail.split('\n')
    for d in details:
        for key in keyWords:
            if d.find(key) > -1:
                number = re.compile(r'\d')
                nums = number.findall(d)
                if nums:
                    for num in nums:
                        index = d.index(num)
                        if index == 0:
                            if d[index + 1] == '年':
                                continue
                            else:
                                d = d[1:]
                d = d.strip().replace('经验', '').replace('语言', '').replace('技术', '').replace('能力', '').replace('团队', '').title()
                lines.append(d)
    detail = ' '.join(lines)
    # seg_list = jieba.cut(detail, cut_all=True)
    # print(", ".join(seg_list))
    keywords = jieba.analyse.extract_tags(detail, topK=120, withWeight=True, allowPOS=('n', 'eng'))
    # keywords = jieba.analyse.textrank(detail, topK=120, withWeight=True, allowPOS=('n', 'eng'))

    return keywords


def get_positions(keyword, city='全国', education='', workyear=''):
    if keyword == 'C++' or keyword == 'C#':
        d_keyword = '\\'.join(keyword)
        query = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword)))
    else:
        query = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword)))

    if city != '全国':
        query = query.filter_by(city=city)
    if education:
        query = query.filter_by(education=education)
    if workyear:
        query = query.filter_by(workyear=workyear)

    positions = query.all()

    return positions


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
