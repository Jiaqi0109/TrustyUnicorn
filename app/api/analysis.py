from flask import render_template, url_for, request, redirect, Response, session
from flask_classy import FlaskView, route
from flask_login import current_user

from app.models.company import Company

from app.helpers import get_positions, description_cy

from wordcloud import WordCloud
from scipy.misc import imread


class AnalysisView(FlaskView):


    @route('/save_company/', methods=['POST'])
    def save_company(self):
        industry = request.form['industry']
        finance_stage = request.form['finance_stage']

        session['industry'] = industry
        session['finance_stage'] = finance_stage

        return redirect(url_for('AnalysisView:index'))


    def index(self):

        descs = ''

        keyword = session.get('keyword')
        city = session.get('city')
        education = session.get('education')
        workyear = session.get('workyear')

        industry = session.get('industry')
        finance_stage = session.get('finance_stage')

        positions = get_positions(keyword, city, education, workyear)


        ipids = []
        for position in positions:
            company = Company.query.get(position.cid)
            if industry and industry in company.industry:
                ipids.append(position.pid)
        fpids = []
        for position in positions:
            company = Company.query.get(position.cid)
            if finance_stage and finance_stage in company.finance_stage:
                fpids.append(position.pid)
        if ipids and fpids:
            pids = set(ipids) & set(fpids)
        elif ipids:
            pids = ipids
        elif fpids:
            pids=fpids
        else:
            pids = []
        print(pids)


        for position in positions:
            if pids:
                if position.pid in pids:
                    descs += position.description
            else:
                descs += position.description
        wordclouds = description_cy(descs)

        data = {}
        for item in wordclouds:
            data[item[0]] = item[1]

        color_mask = imread('./app/static/img/dear.png')
        wc = WordCloud(
            # 设置字体，不指定就会出现乱码
            font_path="./app/static/fonts/wqy-microhei.ttc",
            # font_path=path.join(d,'simsun.ttc'),
            # 设置背景色
            background_color='#f2f2f2',
            # 词云形状
            mask=color_mask,
            # 允许最大词汇
            max_words=10000,
            # 最大号字体
            max_font_size=100
        )
        word_cloud = wc.generate_from_frequencies(data)  # 产生词云
        word_cloud.to_file("./app/static/cy_pic/user/" + str(current_user.id) + "_position.jpg")  # 保存图片

        user_skill = session.get('user_skill')
        position_skill = data

        d = {}
        n = sum(user_skill.values()) + sum(position_skill.values())
        same_list = set(user_skill.keys()) & set(position_skill.keys())
        for l in same_list:
            d[l] = user_skill[l] + position_skill[l]
        rate = int(sum(d.values()) / n * 100)
        d = sorted(d.items(), key=lambda x: x[1], reverse=True)
        keywords = []
        for i in range(10):
            keywords.append(d[i][0])
        keywords = ';'.join(keywords)

        return render_template('analysis.html', keyword=keyword, city=city, education=education, workyear=workyear, rate=rate, keywords=keywords)
