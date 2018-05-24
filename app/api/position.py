import json
from flask import redirect, render_template, request, url_for, Response, session
from flask_classy import FlaskView, route

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

        salaries = []
        cities = []
        educations = []
        workyears = []

        positions = get_positions(keyword)

        for position in positions:
            cities.append(position.city)
            salaries.append(position.salary)
            educations.append(position.education)
            workyears.append(position.workyear)
            
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

    @route('/select_json/', methods=['POST'])
    def select_json(self):
        keyword = session.get('keyword')
        city = request.form['city']

        salaries = []
        educations = []
        workyears = []

        positions = get_positions(keyword, city)

        for position in positions:
            salaries.append(position.salary)
            educations.append(position.education)
            workyears.append(position.workyear)

        salary_data = salary_json(salaries)
        education_data, workyear_data = education_workyear_json(educations, workyears)

        datas = {
            'salary_data': salary_data,
            'education_data': education_data,
            'workyear_data': workyear_data,
        }

        content = json.dumps(datas)
        resp = Response(content)
        return resp
