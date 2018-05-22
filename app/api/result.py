import numpy as np
from flask import render_template, url_for, request, redirect, Response, session
from flask_classy import FlaskView, route

from app.models.company import Company
from app.models.position import Position

import json


class ResultView(FlaskView):

    def index(self):

        keyword = session.get('keyword')
        city = session.get('city')
        education = session.get('education')
        workyear = session.get('workyear')


        pt = []
        if keyword == 'C++' or keyword == 'C#':
            d_keyword = '\\'.join(keyword)
            p_query = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword)))
        else:
            p_query = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword)))
        positions = p_query.filter_by(city=city, education=education, workyear=workyear).all()

        for position in positions:
            company = Company.query.get(position.cid)
            data = {"position": position, "company": company}
            pt.append(data)
        nums = len(pt)
        return render_template('result.html', positions=pt, nums=nums, keyword=keyword, city=city, education=education, workyear=workyear)
