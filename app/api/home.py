from flask import render_template, url_for, request, redirect, Response
from flask_classy import FlaskView, route
from flask_login import login_required
from sqlalchemy import func

from app.extensions import db
from app.models.company import Company
from app.models.position import Position

import json


class HomeView(FlaskView):

    # 根路由
    @login_required
    def index(self):
        number = db.session.query(func.count(Position.pid)).scalar()
        p_num = int(number / 10000) * 10000
        # category_list = db.session.query(Position.name, func.count('*')).group_by(Position.name).all()
        # print(category_list)
        with open('./app/static/keyword/category.txt', 'r') as f:
            categroy = f.readlines()
        c_num = int(len(categroy) / 10) * 10

        city_list = db.session.query(Position.city, func.count('*')).group_by(Position.city).all()
        city_num = len(city_list)

        company_num = db.session.query(func.count(Company.cid)).scalar()
        company_num = int(company_num / 1000) * 1000

        return render_template('home.html', p_num=p_num, c_num=c_num, city_num=city_num, company_num=company_num)

    def position_json(self):
        data = []
        with open('./app/static/keyword/category.txt', 'r') as f:
            keywords = f.readlines()
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword == 'C++' or keyword == 'C#':
                d_keyword = '\\'.join(keyword)
                num = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword))).count()
            else:
                num = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword))).count()
            data.append({"name": keyword, "value": str(num)})

        data = sorted(data, key=lambda x: int(x["value"]), reverse=False)[-25:]
        datas = {
            'data': data,
        }
        content = json.dumps(datas)
        resp = Response(content)
        return resp

    def city_json(self):
        data = []
        city_list = db.session.query(Position.city, func.count('*')).group_by(Position.city).all()
        for city in city_list:
            data.append({'name': city[0], 'value': str(city[1])})

        data = sorted(data, key=lambda x: int(x["value"]), reverse=True)[:12]
        datas = {
            'data': data,
        }
        content = json.dumps(datas)
        resp = Response(content)
        return resp
