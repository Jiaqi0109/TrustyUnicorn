import json
from flask import render_template, url_for, request, redirect, Response, session
from flask_classy import FlaskView, route

from app.models.position import Position
from app.models.detail import Detail

from app.helpers import *


class CityView(FlaskView):

    @route('/', methods=['GET', 'POST'])
    def index(self):
        keyword = session.get('keyword')
        if request.method == 'POST':
            city = request.form['city']
            session['city'] = city
        else:
            city = session.get('city')
            if not city:
                city = 'XXX'
        return render_template('city.html', city=city, keyword=keyword)


    @route('/json/')
    def city_json(self):

        salaries = []
        educations = []
        workyears = []
        wes = []

        keyword = session.get('keyword')
        city = session.get('city')
        if keyword == 'C++' or keyword == 'C#':
            d_keyword = '\\'.join(keyword)
            positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword))).filter_by(
                city=city).all()
        else:
            positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword))).filter_by(
                city=city).all()

        for position in positions:
            salaries.append(position.salary)
            detail = Detail.query.get(position.pid)
            if detail:
                educations.append(detail.education)
                workyears.append(detail.workyear)
                wes.append({'salary': position.salary, 'education': detail.education, 'workyear': detail.workyear})

        session['wes'] = wes


        salary_data = salary_json(salaries)
        education_data, workyear_data = education_workyear_json(educations, workyears)

        datas = {
            'salary_data': salary_data,
            'education_data': education_data,
            'workyear_data': workyear_data
        }
        content = json.dumps(datas)
        resp = Response(content)
        return resp
