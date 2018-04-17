import numpy as np
from flask import render_template, url_for, request, redirect, Response
from flask_classy import FlaskView, route

from app.models.detail import Detail
from app.models.position import Position

import json

from .position import GeneralView

city = 'XXX'
# TODO keyword如何获取
keyword = 'XXX'
positions = []
pids = []
salary = []

class CityView(FlaskView):

    @classmethod
    def get_city(cls):
        global city
        return city

    @classmethod
    def get_positions(cls):
        global positions
        return positions

    @route('/get/', methods=['POST'])
    def get_query(self):
        global city, positions, pids, salary, keyword
        salary = []
        pids = []
        keyword = GeneralView.get_keyword()
        city = request.form['city']
        if keyword == 'C++' or keyword == 'C#':
            d_keyword = '\\'.join(keyword)
            positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword))).filter_by(city=city).all()
        else:
            positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword))).filter_by(city=city).all()

        for position in positions:
            salary.append(position.salary)
            pids.append(position.pid)

        return redirect(url_for('CityView:city'))


    @route('/')
    def city(self):
        return render_template('city.html', city=city, keyword=keyword)


    def education_workyear_json(self):
        global pids
        educations = []
        workyears = []
        for pid in pids:
            detail = Detail.query.get(pid)
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
        }

        content = json.dumps(datas)
        resp = Response(content)
        return resp


    def salary_json(self):
        salarys = []
        data = []
        global salary
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
        }
        content = json.dumps(datas)
        resp = Response(content)
        return resp

