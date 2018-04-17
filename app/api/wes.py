import numpy as np
from flask import render_template, url_for, request, redirect, Response
from flask_classy import FlaskView, route

from app.models.detail import Detail
from app.models.position import Position

import json

from .position import GeneralView
from .city import CityView

keyword = 'XXX'
city = 'XXX'
positions = []
wes = []

class WESView(FlaskView):


    @route('/get/')
    def get_query(self):
        global keyword, city, positions
        keyword = GeneralView.get_keyword()
        city = CityView.get_city()
        positions = CityView.get_positions()
        return redirect(url_for('WESView:index'))


    def index(self):
        return render_template('education_workyear_salary.html', city=city, keyword=keyword)


    def es_json(self):
        global wes
        wes = []
        e_salary = []
        e_data = {}
        e_sort = ['学历不限', '大专及以上', '本科及以上', '硕士及以上', '博士及以上']
        w_sort = ['不限', '应届毕业生', '1年以下', '1-3年', '3-5年', '5-10年', '10年以上']
        for position in positions:
            detail = Detail.query.get(position.pid)
            workyear = detail.workyear
            education = detail.education
            salary = position.salary
            wes.append({'salary': salary, 'education': education, 'workyear': workyear})
        for e in e_sort:
            for p in wes:
                if p['education'] == e:
                    e_salary.append(p['salary'])
            e_data[e] = e_salary
            e_salary = []
        print(e_data)
        return Response()


    @route('/wes_json/', methods=['POST'])
    def wes_json(self):
        data = []
        s_data = []
        salarys = []
        workyear = request.form['workyear']
        education = request.form['education']
        for p in wes:
            if p['education'] == education and p['workyear'] == workyear:
                s_data.append(p)
        salary = [s['salary'] for s in s_data]

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
