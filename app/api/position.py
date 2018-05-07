import json
from flask import redirect, render_template, request, url_for, Response, session
from flask_classy import FlaskView, route
from sqlalchemy import func

from app.extensions import db
from app.models.position import Position
from app.models.detail import Detail

from app.helpers import *


class PositionView(FlaskView):

    @route('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            keyword = request.form['keyword']
            session['keyword'] = keyword
        else:
            keyword = session.get('keyword')
            if not keyword:
                keyword = 'XXX'
        return render_template('position.html', keyword=keyword)

    @route('/json/')
    def position_json(self):
        keyword = session.get('keyword')

        pids = []
        salaries = []
        cities = []
        educations = []
        workyears = []

        if keyword == 'C++' or keyword == 'C#':
            d_keyword = '\\'.join(keyword)
            positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword))).all()
        else:
            positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword))).all()

        for position in positions:
            cities.append(position.city)
            salaries.append(position.salary)
            pids.append(position.pid)

        for pid in pids:
            detail = Detail.query.get(pid)
            if detail:
                educations.append(detail.education)
                workyears.append(detail.workyear)

        city_data = city_json(cities)
        city_most = '、'.join(c['name'] for c in city_data[:2])

        salary_data = salary_json(salaries)
        salary_ave = str(int(salary_amm(salaries)[2]))

        education_data, workyear_data = education_workyear_json(educations, workyears)
        ed = sorted(education_data, key=lambda x: int(x["value"]), reverse=True)[0]['name']
        wd = sorted(workyear_data, key=lambda x: int(x["value"]), reverse=True)[0]['name']

        datas = {
            'city_data': city_data,
            'salary_data': salary_data,
            'education_data': education_data,
            'workyear_data': workyear_data,

            'city_most': city_most,
            'salary_avg': salary_ave,
            'ed': ed,
            'wd': wd
        }
        content = json.dumps(datas)
        resp = Response(content)
        return resp
