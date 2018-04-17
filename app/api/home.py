from flask import render_template, url_for, request, redirect, Response
from flask_classy import FlaskView, route

from app.models.position import Position

import json


class HomeView(FlaskView):

    # 根路由
    def index(self):
        return render_template('home.html')


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
        with open('./app/static/keyword/city.txt', 'r') as f:
            cities = f.readlines()
        for city in cities:
            city = city.strip()
            num = Position.query.filter_by(city=city).count()
            data.append({"name": city, "value": str(num)})

        data = sorted(data, key=lambda x: int(x["value"]), reverse=True)[:12]
        datas = {
            'data': data,
        }
        content = json.dumps(datas)
        resp = Response(content)
        return resp
