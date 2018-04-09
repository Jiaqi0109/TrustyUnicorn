import numpy as np
import pandas as pd
from app.models.position import Position
from app.models.detail import Detail
from flask import redirect, render_template, request, url_for, Response
from flask_classy import FlaskView, route
from pandas import DataFrame, Series

from datetime import datetime

import json


keyword = 'XXX'
positions = []
pids = []
salary = []
cities = []


class GeneralView(FlaskView):

    @route('/get/', methods=['POST'])
    def get_query(self):
        global keyword, positions, pids, salary, cities
        keyword = request.form['keyword']

        if keyword == 'C++' or keyword == 'C#':
            d_keyword = '\\'.join(keyword)
            positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword))).order_by('publish_time').all()[::-1]
        else:
            positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword))).order_by('publish_time').all()[::-1]

        for position in positions:
            cities.append(position.city)
            salary.append(position.salary)
            pids.append(position.pid)

        return redirect(url_for('GeneralView:general'))



    @route('/general/')
    def general(self):

        return render_template('general_situation.html')

    @route('/city_json/')
    def city_json(self):
        global keyword, cities, positions

        if not positions:
            return Response()

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

        datas = {
            'data': data,
            'keyword': keyword,
        }

        content = json.dumps(datas)
        resp = Response(content)
        return resp


    @route('/education_workyear_json/')
    def education_workyear_json(self):
        global pids, keyword
        educations = []
        workyears = []
        for pid in pids:
            detail = Detail.query.filter_by(pid=pid).first()
            if detail:
                educations.append(detail.education)
                workyears.append(detail.workyear)
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

        datas = {
            'edu_data': edu_data,
            'work_data': work_data,
            'keyword': keyword
        }

        content = json.dumps(datas)
        resp = Response(content)
        return resp


    @route('/salary_json/')
    def salary_json(self):
        salarys = []
        data = []
        global salary, keyword
        salary_d = [s.replace('k', '').replace('K', '').replace('以上', '-').replace('+', '-') for s in salary]
        for s in salary_d:
            min, max = s.split('-')
            if not max:
                if min == '100':
                    max = '110'
                else:
                    max = int(int(min)*1.5)
            for i in range(int(min), int(max) + 1):
                salarys.append(i)
        nd_salarys = np.array(salarys)
        s_name = list({s for s in nd_salarys})
        s_name = sorted(s_name)
        s_nums = [np.sum(nd_salarys == s) for s in s_name]
        for name, value in zip(s_name, s_nums):
            data.append({"name": str(name * 1000), "value": str(value)})

        datas = {
            'data': data,
            'keyword': keyword
        }
        content = json.dumps(datas)
        resp = Response(content)
        return resp
