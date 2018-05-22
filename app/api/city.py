import json
from flask import render_template, url_for, request, redirect, Response, session
from flask_classy import FlaskView, route

from app.models.position import Position
from app.models.company import Company

from app.helpers import *

# TODO 做一个详情的词云，留一个薪资图


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

        positions = get_positions(keyword, city=city)

        for position in positions:
            salaries.append(position.salary)
            detail = Detail.query.get(position.pid)
            company = Company.query.get(position.cid)
            if detail and company:
                educations.append(detail.education)
                workyears.append(detail.workyear)
                # TODO 将公司类别做成词云
                wes.append({
                    'pid': position.pid,
                    'salary': position.salary,
                    'education': detail.education,
                    'workyear': detail.workyear,
                    'finance_stage': company.finance_stage,
                    'industry': company.industry
                })

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
