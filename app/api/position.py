import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from app.models.position import Position
from app.models.detail import Detail
from flask import redirect, render_template, request, url_for
from flask_classy import FlaskView, route
from pandas import DataFrame, Series

from datetime import datetime

import matplotlib as mpl

# 中文字体显示
from app.helpers import zh_font
zh_hans = zh_font()

position_query = None

class PositionView(FlaskView):

    # 第一个页面
    @route('/', methods=['POST'])
    def index(self):
        salary = []
        cities = []
        pids = []
        keyword = request.form['keyword']

        if keyword == 'C++' or keyword == 'C#':
            d_keyword = '\\'.join(keyword)
            query = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(d_keyword)))
        else:
            query = Position.query.filter(Position.name.op('regexp')(r'({0})'.format(keyword)))
            # positions = Position.query.limit(2000).all()
            # positions = Position.query.filter_by(city=city).all()

        # 全局变量，逐步筛选职位
        global position_query
        position_query = query
        positions = query.order_by('publish_time').all()[::-1]

        num = len(positions)

        for position in positions:
            cities.append(position.city)
            salary.append(position.salary)
            pids.append(position.pid)
        
        city_png = self.city_pie(cities, keyword, num)
        salary_png = self.salary_bar(salary)
        education = []
        workyear = []
        for pid in pids:
            detail = Detail.query.filter_by(pid=pid).first()
            if detail:
                education.append(detail.education)
                workyear.append(detail.workyear)
        education_png = self.education_bar(education)
        workyear_png = self.workyear_bar(workyear)

        return render_template('position_1st.html', num=num, keyword=keyword, workyear_png=workyear_png, education_png=education_png, city_png=city_png, salary_png=salary_png, positions=positions[:20])


    @route('/city/', methods=['POST'])
    def select_city(self):
        global position_query

        city = request.form['city']
        query = position_query.filter_by(city=city)
        position_query = query
        positions = query.order_by('publish_time').all()[::-1]
        num = len(positions)
        return render_template('position_2nd.html', num=num, positions=positions[:50])


    # 城市分布饼图
    def city_pie(self, cities, keyword, num):
        nd_city = np.array(cities)
        another = 0
        _min = num // 100

        # 标签列表
        s_city = list({c for c in nd_city})
        # 各标签的个数
        nums = [np.sum(nd_city == c) for c in s_city]

        # 将小于1%职位的城市合并
        for i in range(len(nums), 0, -1):
            if nums[i-1] <= _min:
                another += nums[i-1]
                s_city.pop(i-1)
                nums.pop(i-1)

        if another > 0:
            s_city.append(u'其他')
            nums.append(another)
        # 解决中文显示问题
        s_city = [u'{0}'.format(city) for city in s_city]

        # 创建子plot，不然图会乱
        fig, ax = plt.subplots()
        # TODO: 饼图 中文显示问题解决方案！
        pie = ax.pie(nums, labels=s_city, labeldistance=1.2, autopct='%1.1f%%')
        for font in pie[1]:
            font.set_fontproperties(mpl.font_manager.FontProperties(
                fname='./app/static/fonts/wqy-microhei.ttc'))

        # 条形图
        # plt.bar(s_city, nums)
        # plt.xticks(s_city,rotation=30, fontproperties=zh_hans)
        plt.title(u'{0}职位城市分布'.format(keyword), fontproperties=zh_hans)
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '-0'
        plt.savefig('./app/static/img/{0}.png'.format(filename))
        return filename


    def salary_bar(self, salary):
        import re
        salary = [s.replace('k', '').replace('K', '') for s in salary]
        data = []
        for s in salary:
            # 筛选不规范的数据
            Chinese_characters = re.compile(r'[\u4e00-\u9fa5]')
            char = Chinese_characters.findall(s)
            signal = re.compile(r'\+')
            sig = signal.findall(s)
            if char or sig:
                continue
            start = int(s.split('-')[0])
            stop = int(s.split('-')[1])
            for i in range(start, stop + 1):
                data.append(i)
        fit, ax = plt.subplots()
        # bins 共有几条柱
        ax.hist(data, bins=15, color='b')
        plt.xlabel('薪资(/k)', fontproperties=zh_hans)
        plt.ylabel('频度', fontproperties=zh_hans)
        plt.title(u'薪资分布', fontproperties=zh_hans)
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '-1'
        plt.savefig('./app/static/img/{0}.png'.format(filename))
        return filename

    def education_bar(self, education):
        data = education
        fit, ax = plt.subplots()
        ax.hist(data, color='g')
        plt.xticks(fontproperties=zh_hans)
        plt.ylabel('职位个数', fontproperties=zh_hans)
        plt.title(u'教育程度分布', fontproperties=zh_hans)
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '-2'
        plt.savefig('./app/static/img/{0}.png'.format(filename))
        return filename

    def workyear_bar(self, workyear):
        data = workyear
        fit, ax = plt.subplots()
        ax.hist(data, color='r')
        plt.xticks(fontproperties=zh_hans)
        plt.ylabel('职位个数', fontproperties=zh_hans)
        plt.title(u'工作经验分布', fontproperties=zh_hans)
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '-3'
        plt.savefig('./app/static/img/{0}.png'.format(filename))
        return filename
