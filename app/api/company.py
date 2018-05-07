import json
import numpy as np
from flask import render_template, url_for, request, redirect, Response, session
from flask_classy import FlaskView, route
from flask_login import current_user

from app.models.position import Position
from app.models.detail import Detail
from app.models.company import Company

from wordcloud import WordCloud

from app.helpers import *


class CompanyView(FlaskView):

    def index(self):

        return render_template('company.html')


    def finance_json(self):
        finances = []
        salaries = []
        data = []
        f_data = []
        com = session.get('com')
        if com:
            for p in com:
                finances.append(p['finance_stage'])

        n_list = np.array(finances)
        f_sort = ['未融资', '天使轮', 'A轮', 'B轮', 'C轮', 'D轮及以上', '上市公司', '不需要融资']
        f_name = list({w for w in n_list if w})
        f_name = sorted(f_name, key=f_sort.index)
        f_nums = [np.sum(n_list == c) for c in f_name]
        for f in f_name:
            for p in com:
                if p['finance_stage'] == f:
                    salaries.append(p['salary'])
            if salaries:
                s_min, s_max, s_avg = salary_amm(salaries)
                f_data.append({'name': f, 'min': s_min, 'max': s_max, 'avg': s_avg})
                salaries = []

        for name, value in zip(f_name, f_nums):
            data.append({"name": name, "value": str(value)})
        datas = {
            'data': data,
            'f_data': f_data
        }
        content = json.dumps(datas)
        resp = Response(content)
        return resp


    def industry_json(self):
        industrys = []
        salaries = []
        data = []
        i_data = []
        com = session.get('com')
        if com:
            for p in com:
                _data = p['industry'].replace(' ', ',').replace('、', ',')
                for _c in _data.split(','):
                    if _c:
                        industrys.append(_c.strip())

        n_list = np.array(industrys)
        i_name = list({w for w in n_list if w})
        i_nums = [np.sum(n_list == c) for c in i_name]

        for name, value in zip(i_name, i_nums):
            data.append({"name": name, "value": str(value)})
        data = sorted(data, key=lambda x: int(x["value"]), reverse=True)

        s_name = []
        for d in data:
            s_name.append(d['name'])
        for i in s_name:
            for p in com:
                if i in p['industry']:
                    salaries.append(p['salary'])
            if salaries:
                s_min, s_max, s_avg = salary_amm(salaries)
                i_data.append({'name': i, 'min': s_min, 'max': s_max, 'avg': s_avg})
                salaries = []

        datas = {
            'data': data,
            'i_data': i_data
        }
        content = json.dumps(datas)
        resp = Response(content)
        return resp



    # def cy_json(self):
    #     wordcloud_list = []
    #     com = session.get('com')
    #     if com:
    #         for p in com:
    #             _data = p['industry'].replace(' ', ',').replace('、', ',')
    #             for _c in _data.split(','):
    #                 if _c:
    #                     wordcloud_list.append(_c.strip())
    #
    #     n_list = np.array(wordcloud_list)
    #     wl = list({w for w in wordcloud_list})
    #     nums = [np.sum(n_list == c) for c in wl]
    #
    #     data = []
    #     wdata = {}
    #     for name, value in zip(wl, nums):
    #         data.append({"name": name, "value": str(value)})
    #         wdata[name] = value
    #
    #
    #     # wordcloud
    #     wc = WordCloud(
    #         # 设置字体，不指定就会出现乱码
    #         font_path="./app/static/fonts/wqy-microhei.ttc",
    #         # font_path=path.join(d,'simsun.ttc'),
    #         # 设置背景色
    #         background_color='white',
    #         # 词云形状
    #         # mask=color_mask,
    #         # 允许最大词汇
    #         max_words=10000,
    #         # 最大号字体
    #         max_font_size=40
    #     )
    #     word_cloud = wc.generate_from_frequencies(wdata)  # 产生词云
    #     word_cloud.to_file("./app/static/cy_pic/user/" + str(current_user.id) + "_company.jpg")  # 保存图片
    #
    #
    #     datas = {
    #         'data': data
    #     }
    #
    #     content = json.dumps(datas)
    #     resp = Response(content)
    #     return resp
