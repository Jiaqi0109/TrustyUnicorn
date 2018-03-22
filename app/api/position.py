import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from app.models.position import Position
from flask import redirect, render_template, request, url_for
from flask_classy import FlaskView
from pandas import DataFrame, Series


class PositionView(FlaskView):

    # 根路由
    def index(self):
        salary = []
        city = []
        # positions = Position.query.filter_by(city='太原').order_by('publish_time').all()[::-1]
        # 正则匹配数据库
        positions = Position.query.filter(Position.name.op('regexp')(r'(Python)')).order_by('publish_time').all()[::-1]

        num = len(positions)

        for position in positions:
            city.append(position.city)
            salary.append(position.salary)
        
        self.city_pie(city)

        return render_template('position.html', num=num, positions=positions)


    # 城市分布饼图
    def city_pie(self, cities):
        nd_city = np.array(cities)
        another = 0

        # 标签列表
        s_city = list({c for c in nd_city})
        # 各标签的个数
        nums = [np.sum(nd_city == c) for c in s_city]

        # 将小于5个职位的城市合并
        for i in range(len(nums), 0, -1):
            if nums[i-1] <= 5:
                another += nums[i-1]
                s_city.pop(i-1)
                nums.pop(i-1)

        s_city.append('another')
        nums.append(another)

        s_city = np.array(s_city)
        nums = np.array(nums)

        plt.pie(nums, labels=s_city, labeldistance=1.2, autopct='%1.1f%%', shadow=True)
        plt.savefig('./app/static/img/test.png')
