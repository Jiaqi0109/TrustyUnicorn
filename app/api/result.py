from flask import render_template, url_for, request, redirect, Response, session
from flask_classy import FlaskView, route
from flask_login import current_user

from app.models.company import Company

from app.helpers import get_positions, description_cy
from app.models.position import Position
import copy


class ResultView(FlaskView):

    @route('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            keywords = request.form['keywords']
            session['keywords'] = keywords
        else:
            keywords = session.get('keywords')
        salary = request.args.get('salary')
        sort = request.args.get('sort')
        if not salary:
            salary = '不限'

        keywords = (keywords + ';' + current_user.keywords).replace('；', ';').split(';')


        keyword = session.get('keyword')
        city = session.get('city')
        education = session.get('education')
        workyear = session.get('workyear')

        industry = session.get('industry')
        finance_stage = session.get('finance_stage')

        pt = []
        positions = get_positions(keyword, city, education, workyear)

        # 筛选符合条件的公司的职位id
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


        # 相关度计算
        user_skill = session.get('user_skill')
        us = copy.deepcopy(user_skill)
        # 加入用户自定义关键词的idf值
        if keywords:
            for key in keywords:
                if key:
                    us[key.title()] = 100

        # 筛选不同薪资
        descs = []
        if salary == '不限':
            for position in positions:
                if pids:
                    if position.pid in pids:
                        result = description_cy(position.description)
                        if result:
                            descs.append((position.pid, {r[0]: r[1] for r in result}))
                else:
                    result = description_cy(position.description)
                    if result:
                        descs.append((position.pid, {r[0]: r[1] for r in result}))

        elif salary == '2k以下':
            for position in positions:
                if pids:
                    if position.pid in pids:
                        ps = position.salary.replace('k', '').replace('K', '').replace('以上', '-').replace('+', '-').split('-')
                        if len(ps) == 1 or ps[1] == '':
                            ps[1] = int(ps[0]) * 1.5
                        if int(ps[1]) <= 2:
                            result = description_cy(position.description)
                            if result:
                                descs.append((position.pid, {r[0]: r[1] for r in result}))
                        pass
                else:
                    ps = position.salary.replace('k', '').replace('K', '').replace('以上', '-').replace('+', '-').split('-')
                    if len(ps) == 1 or ps[1] == '':
                        ps[1] = int(ps[0]) * 1.5
                    if int(ps[1]) <= 2:
                        result = description_cy(position.description)
                        if result:
                            descs.append((position.pid, {r[0]: r[1] for r in result}))
        elif salary == '50k以上':
            for position in positions:
                if pids:
                    if position.pid in pids:
                        ps = position.salary.replace('k', '').replace('K', '').replace('以上', '-').replace('+', '-').split('-')
                        if len(ps) == 1 or ps[1] == '':
                            ps[1] = int(ps[0]) * 1.5
                        if int(ps[1]) >= 50:
                            result = description_cy(position.description)
                            if result:
                                descs.append((position.pid, {r[0]: r[1] for r in result}))
                else:
                    ps = position.salary.replace('k', '').replace('K', '').replace('以上', '-').replace('+', '-').split('-')
                    if len(ps) == 1 or ps[1] == '':
                        ps[1] = int(ps[0]) * 1.5
                    if int(ps[1]) >= 50:
                        result = description_cy(position.description)
                        if result:
                            descs.append((position.pid, {r[0]: r[1] for r in result}))
        else:
            for position in positions:
                if pids:
                    if position.pid in pids:
                        ps = position.salary.replace('k', '').replace('K', '').replace('以上', '-').replace('+', '-').split('-')
                        if len(ps) == 1 or ps[1] == '':
                            ps[1] = int(ps[0]) * 1.5
                        min, max = salary.replace('k', '').split('-')
                        if int(ps[0]) >= int(min) and int(ps[0]) < int(max):
                            result = description_cy(position.description)
                            if result:
                                descs.append((position.pid, {r[0]: r[1] for r in result}))
                else:
                    ps = position.salary.replace('k', '').replace('K', '').replace('以上', '-').replace('+', '-').split('-')
                    if len(ps) == 1 or ps[1] == '':
                        ps[1] = int(ps[0]) * 1.5
                    min, max = salary.replace('k', '').split('-')
                    if int(ps[0]) >= int(min) and int(ps[0]) < int(max):
                        result = description_cy(position.description)
                        if result:
                            descs.append((position.pid, {r[0]: r[1] for r in result}))


        data = {}
        # 求相同技术关键词集合
        for desc in descs:
            same_list = set(us.keys()) & set(desc[1].keys())
            similarity = sum([us[s] * desc[1][s] for s in same_list])
            data[desc[0]] = similarity

        # 排序
        if sort == 'new':
            lk = list(data.keys())
            positions = [Position.query.get(d) for d in lk]
        else:
            data = sorted(data.items(), key=lambda x: x[1], reverse=True)
            positions = [Position.query.get(d[0]) for d in data]

        for position in positions:
            company = Company.query.get(position.cid)
            data = {"position": position, "company": company}
            pt.append(data)

        nums = len(pt)

        return render_template('result.html', salary=salary, positions=pt, nums=nums, keyword=keyword, city=city,
                               education=education, industry=industry, finance_stage=finance_stage,
                               workyear=workyear, keywords=(' '.join(keywords) if keywords != [''] else '未指定'))
