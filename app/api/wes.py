import numpy as np
from flask import render_template, url_for, request, redirect, Response, session, g
from flask_classy import FlaskView, route

from app.helpers import *
from app.models.detail import Detail
from app.models.position import Position

import json


class WESView(FlaskView):

    def index(self):
        keyword = session.get('keyword')
        city = session.get('city')
        return render_template('education_workyear_salary.html', city=city, keyword=keyword)



    def compare_json(self):

        keyword = session.get('keyword')
        city = session.get('city')

        # if keyword == 'C++' or keyword == 'C#':
        #     d_keyword = '\\'.join(keyword)
        #     positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword))).filter_by(
        #         city=city).all()
        # else:
        #     positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword))).filter_by(
        #         city=city).all()

        # wes = []
        e_salary = []
        w_salary = []
        e_data = []
        w_data = []
        e_sort = ['学历不限', '大专及以上', '本科及以上', '硕士及以上', '博士及以上']
        w_sort = ['不限', '应届毕业生', '1年以下', '1-3年', '3-5年', '5-10年', '10年以上']
        # for position in positions:
        #     detail = Detail.query.get(position.pid)
        #     workyear = detail.workyear
        #     education = detail.education
        #     salary = position.salary
        #     wes.append({'salary': salary, 'education': education, 'workyear': workyear})

        wes = session.get('wes')

        for e in e_sort:
            for p in wes:
                if p['education'] == e:
                    e_salary.append(p['salary'])
            if e_salary:
                s_min, s_max, s_avg = salary_amm(e_salary)
                e_data.append({'name': e, 'min':s_min, 'max':s_max, 'avg':s_avg })
                e_salary = []
        for w in w_sort:
            for p in wes:
                if p['workyear'] == w:
                    w_salary.append(p['salary'])
            if w_salary:
                w_min, w_max, w_avg = salary_amm(w_salary)
                w_data.append({'name': w, 'min':w_min, 'max':w_max, 'avg':w_avg })
                w_salary = []
        # print(e_data)
        # print(w_data)

        datas = {
            'e_data': e_data,
            'w_data': w_data
        }

        content = json.dumps(datas)
        resp = Response(content)
        return resp



    @route('/wes_json/', methods=['POST'])
    def wes_json(self):
        salaries = []
        wes = session.get('wes')
        workyear = request.form['workyear']
        education = request.form['education']
        for p in wes:
            if p['education'] == education and p['workyear'] == workyear:
                salaries.append(p['salary'])
        data = salary_json(salaries)

        datas = {
            'data': data,
        }
        content = json.dumps(datas)
        resp = Response(content)
        return resp



    # def json(self):
    #
    #     keyword = session.get('keyword')
    #     city = session.get('city')
    #
    #     if keyword == 'C++' or keyword == 'C#':
    #         d_keyword = '\\'.join(keyword)
    #         positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword))).filter_by(
    #             city=city).all()
    #     else:
    #         positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword))).filter_by(
    #             city=city).all()
    #
    #     wes = []
    #     e_salary = []
    #     w_salary = []
    #     e_data = []
    #     w_data = []
    #     salaries = []
    #     e_sort = ['学历不限', '大专及以上', '本科及以上', '硕士及以上', '博士及以上']
    #     w_sort = ['不限', '应届毕业生', '1年以下', '1-3年', '3-5年', '5-10年', '10年以上']
    #     for position in positions:
    #         detail = Detail.query.get(position.pid)
    #         workyear = detail.workyear
    #         education = detail.education
    #         salary = position.salary
    #         salaries.append(salary)
    #         wes.append({'salary': salary, 'education': education, 'workyear': workyear})
    #
    #     salary_d = [s.replace('k', '').replace('K', '').replace('以上', '-').replace('+', '-') for s in salaries]
    #     a_s = []
    #     for s in salary_d:
    #         a_s += s.split('-')
    #     a_s = [int(a) for a in a_s]
    #     s_min = min(a_s)
    #     s_max = max(a_s)
    #     if s_max == 100:
    #         s_max = 110
    #     salary_data = [s for s in range(s_min, s_max + 1)]
    #
    #     for e in e_sort:
    #         for p in wes:
    #             if p['education'] == e:
    #                 e_salary.append(p['salary'])
    #         if e_salary:
    #             e_salary = salary2_json(e_salary, salary_data)
    #             e_data.append({'name': e, 'value': e_salary})
    #             e_salary = []
    #     for w in w_sort:
    #         for p in wes:
    #             if p['workyear'] == w:
    #                 w_salary.append(p['salary'])
    #         if w_salary:
    #             w_salary = salary2_json(w_salary, salary_data)
    #             w_data.append({'name': w, 'value': w_salary})
    #             w_salary = []
    #     # print(e_data)
    #     # print(w_data)
    #
    #     datas = {
    #         'salary_data': [str(s * 1000) for s in salary_data],
    #         'e_data': e_data,
    #         'w_data': w_data
    #     }
    #
    #     content = json.dumps(datas)
    #     resp = Response(content)
    #     return resp
