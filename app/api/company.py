import json
import numpy as np
from flask import render_template, url_for, request, redirect, Response, session
from flask_classy import FlaskView, route
from flask_login import current_user

from app.models.position import Position
from app.models.company import Company


from app.helpers import *


class CompanyView(FlaskView):

    @route('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            education = request.form['education']
            workyear = request.form['workyear']
            session['education'] = education
            session['workyear'] = workyear

        keyword = session.get('keyword')
        city = session.get('city')

        return render_template('company.html', keyword=keyword, city=city)


    def finance_json(self):

        keyword = session.get('keyword')
        city = session.get('city')
        education = session.get('education')
        workyear = session.get('workyear')

        positions = get_positions(keyword=keyword, city=city, education=education, workyear=workyear)

        finances = []
        salaries = []
        data = []
        f_data = []

        com = []
        for position in positions:
            company = Company.query.get(position.cid)
            if company:
                finances.append(company.finance_stage)
                com.append({'finance_stage': company.finance_stage, 'industry':company.industry, 'salary': position.salary})

        n_list = np.array(finances)
        f_sort = ['未融资', '天使轮', 'A轮', 'B轮', 'C轮', 'D轮及以上', '上市公司', '不需要融资']
        f_name = list({w for w in n_list if w})
        f_name = sorted(f_name, key=f_sort.index)
        f_nums = [np.sum(n_list == c) for c in f_name]
        for f in f_name:
            for c in com:
                if c['finance_stage'] == f:
                    salaries.append(c['salary'])
            if salaries:
                s_min, s_max, s_avg = salary_amm(salaries)
                f_data.append({
                    'name': f,
                    'min': s_min,
                    'max': s_max,
                    'avg': s_avg
                })
                salaries = []

        for name, value in zip(f_name, f_nums):
            data.append({"name": name, "value": str(value)})
        datas = {'data': data, 'f_data': f_data}
        content = json.dumps(datas)
        resp = Response(content)
        return resp


    def industry_json(self):
        keyword = session.get('keyword')
        city = session.get('city')
        education = session.get('education')
        workyear = session.get('workyear')

        positions = get_positions(keyword, city=city, education=education, workyear=workyear)

        industrys = []
        salaries = []
        data = []
        i_data = []

        com = []
        for position in positions:
            company = Company.query.get(position.cid)
            if company:
                com.append({'finance_stage': company.finance_stage, 'industry': company.industry, 'salary': position.salary})

        for p in com:
            _data = p['industry'].replace(' ', ',').replace('、', ',')
            for _c in _data.split(','):
                if _c:
                    industrys.append(_c.strip())

        n_list = np.array(industrys)
        i_name = list({w for w in n_list if w})
        i_nums = [np.sum(n_list == c) for c in i_name]

        for name, value in zip(i_name, i_nums):
            data.append({"name": name, "value": str(value)})
        data = sorted(data, key=lambda x: int(x["value"]), reverse=True)

        s_name = []
        for d in data:
            s_name.append(d['name'])
        for i in s_name:
            for p in com:
                if i in p['industry']:
                    salaries.append(p['salary'])
            if salaries:
                s_min, s_max, s_avg = salary_amm(salaries)
                i_data.append({
                    'name': i,
                    'min': s_min,
                    'max': s_max,
                    'avg': s_avg
                })
                salaries = []

        datas = {'data': data, 'i_data': i_data}
        content = json.dumps(datas)
        resp = Response(content)
        return resp

