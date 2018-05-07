import numpy as np
from flask import render_template, url_for, request, redirect, Response, session
from flask_classy import FlaskView, route

from app.models.company import Company
from app.models.detail import Detail
from app.models.position import Position

import json


class ResultView(FlaskView):

    def index(self):

        keyword = session.get('keyword')
        city = session.get('city')
        education = session.get('education')
        workyear = session.get('workyear')

        # l = []
        pids = []
        pt = []
        # positions = Position.query.filter(Position.name.op('regexp')(r'({0})'.format('Python'))).filter_by(city='上海').filter_by(salary='10K-20K').all()
        # for p in positions:
        #     l.append(p.pid)
        # for s in l:
        #     detail = Detail.query.get(s)
        #     if detail.education == '本科及以上' and detail.workyear == '1-3年':
        #         pids.append(s)
        com = session.get('com')
        for c in com:
            pids.append(c['pid'])

        for pid in pids:
            position = Position.query.get(pid)
            detail = Detail.query.get(pid)
            company = Company.query.get(position.cid)
            if position and detail and company:
                data = {"position": position, "detail": detail, "company": company}
                pt.append(data)
        nums = len(pt)
        return render_template('result.html', positions=pt, nums=nums, keyword=keyword, city=city, education=education, workyear=workyear)
