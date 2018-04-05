import numpy as np
import pandas as pd
from app.models.position import Position
from app.models.detail import Detail
from flask import redirect, render_template, request, url_for, Response
from flask_classy import FlaskView, route
from pandas import DataFrame, Series

from datetime import datetime


import json

# 中文字体显示
from app.helpers import zh_font
zh_hans = zh_font()

position_query = None
keyword = 'lagou'


class PositionView(FlaskView):

    @route('/city/', methods=['POST'])
    def city(self):
        global keyword
        keyword = request.form['keyword']

        # if keyword == 'C++' or keyword == 'C#':
        #     d_keyword = '\\'.join(keyword)
        #     query = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword)))
        # else:
        #     query = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword)))
        #
        # # 全局变量，逐步筛选职位
        # global position_query
        # position_query = query
        # positions = query.order_by('publish_time').all()[::-1]


        # education = []
        # workyear = []
        # for pid in pids:
        #     detail = Detail.query.filter_by(pid=pid).first()
        #     if detail:
        #         education.append(detail.education)
        #         workyear.append(detail.workyear)

        return render_template('city.html')

    @route('/city_json/')
    def city_json(self):
        cities = []
        salary = []
        pids = []

        global keyword

        if keyword == 'C++' or keyword == 'C#':
            d_keyword = '\\'.join(keyword)
            query = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword)))
        else:
            query = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword)))

        global position_query
        position_query = query
        positions = query.order_by('publish_time').all()[::-1]

        num = len(positions)

        for position in positions:
            cities.append(position.city)
            salary.append(position.salary)
            pids.append(position.pid)

        nd_city = np.array(cities)
        # 标签列表
        s_city = list({c for c in nd_city})
        # 各标签的个数
        nums = [np.sum(nd_city == c) for c in s_city]

        data = []
        for name, value in zip(s_city, nums):
            data.append({"name": name, "value": str(value)})
        # 数据排序
        data = sorted(data, key=lambda x: int(x["value"]), reverse=True)

        datas = {
            'data': data,
            'keyword': keyword,
            'num': num
        }

        content = json.dumps(datas)
        resp = Response(content)
        return resp


    @route('/education/', methods=['POST'])
    def education(self):
        global position_query
        city = request.form['city']
        query = position_query.filter_by(city=city)
        # position_query = query
        positions = query.order_by('publish_time').all()[::-1]
        num = len(positions)
        return render_template('education.html', num=num, positions=positions[:50])

    @route('/education_json/')
    def education_json(self):
        pass



    #
    # def salary_bar(self, salary):
    #     import re
    #     salary = [s.replace('k', '').replace('K', '') for s in salary]
    #     data = []
    #     for s in salary:
    #         # 筛选不规范的数据
    #         Chinese_characters = re.compile(r'[\u4e00-\u9fa5]')
    #         char = Chinese_characters.findall(s)
    #         signal = re.compile(r'\+')
    #         sig = signal.findall(s)
    #         if char or sig:
    #             continue
    #         start = int(s.split('-')[0])
    #         stop = int(s.split('-')[1])
    #         for i in range(start, stop + 1):
    #             data.append(i)
    #     fit, ax = plt.subplots()
    #     # bins 共有几条柱
    #     ax.hist(data, bins=15, color='b')
    #     plt.xlabel('薪资(/k)', fontproperties=zh_hans)
    #     plt.ylabel('频度', fontproperties=zh_hans)
    #     plt.title(u'薪资分布', fontproperties=zh_hans)
    #     filename = datetime.now().strftime('%Y%m%d%H%M%S') + '-1'
    #     plt.savefig('./app/static/img/{0}.png'.format(filename))
    #     return filename
    #
    # def education_bar(self, education):
    #     data = education
    #     fit, ax = plt.subplots()
    #     ax.hist(data, color='g')
    #     plt.xticks(fontproperties=zh_hans)
    #     plt.ylabel('职位个数', fontproperties=zh_hans)
    #     plt.title(u'教育程度分布', fontproperties=zh_hans)
    #     filename = datetime.now().strftime('%Y%m%d%H%M%S') + '-2'
    #     plt.savefig('./app/static/img/{0}.png'.format(filename))
    #     return filename
    #
    # def workyear_bar(self, workyear):
    #     data = workyear
    #     fit, ax = plt.subplots()
    #     ax.hist(data, color='r')
    #     plt.xticks(fontproperties=zh_hans)
    #     plt.ylabel('职位个数', fontproperties=zh_hans)
    #     plt.title(u'工作经验分布', fontproperties=zh_hans)
    #     filename = datetime.now().strftime('%Y%m%d%H%M%S') + '-3'
    #     plt.savefig('./app/static/img/{0}.png'.format(filename))
    #     return filename
