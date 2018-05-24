from flask import render_template, url_for, request, redirect, Response, flash, session
from flask_classy import FlaskView, route
from flask_login import login_user, logout_user, login_required, current_user

from app.helpers import description_cy
from app.models.position import Position
from app.models.company import Company
from app.models.user import User
from app.models.feedback import Feedback
from app.extensions import db
from datetime import datetime

import json
from wordcloud import WordCloud
from scipy.misc import imread


class UserView(FlaskView):
    route_base = '/'

    @route('/')
    def index(self):
        return redirect(url_for('HomeView:index'))

    @route('/register/', methods=['POST', 'GET'])
    def registers(self):
        if request.method == 'POST':
            uid = datetime.now().strftime('%y%j%f')[:10]
            username = request.form['username']
            if User.query.filter_by(name=username).first():
                flash('用户名已存在！')
                return render_template('register.html')
            password = request.form['password']
            password2 = request.form['password2']
            if password != password2:
                flash('两次输入密码不一致！')
                return render_template('register.html')
            email = request.form['email']
            if User.query.filter_by(email=email).first():
                flash('该邮箱已注册！')
                return render_template('register.html')
            user = User(id=uid, name=username, password=password, email=email, pids='')
            db.session.add(user)
            db.session.commit()

            login_user(user)

            flash('欢迎 ' + username + ', 请到个人中心激活账户！')
            return redirect(url_for('HomeView:index'))
        return render_template('register.html')

    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            remember = request.form.get('remember')
            if not remember:
                remember = False
            else:
                remember = True
            u = User.query.filter_by(name=username).first()
            if u:
                if u.password == password:
                    login_user(u, remember=remember)
                    flash('登陆成功！')
                    next = request.args.get('next')
                    return redirect(next or url_for('HomeView:index'))
            else:
                flash('用户名或密码错误，请重新登陆！')
                return render_template('login.html')
        return render_template('login.html')

    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('UserView:login'))

    # TODO 邮箱激活
    def activate(self):
        user = User.query.get(current_user.id)
        user.activate = True
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('UserView:center'))

    @login_required
    def center(self):
        positions = []
        pids = current_user.pids
        pids = pids.split('-')
        for pid in pids[::-1]:
            position = Position.query.get(pid)
            if position:
                company = Company.query.get(position.cid)
                data = {"position": position, "company": company}
                positions.append(data)
        nums = len(positions)
        return render_template('user_center.html', positions=positions, nums=nums)

    @login_required
    @route('/change_info/', methods=['POST'])
    def change_info(self):
        new_password = request.form['new_password']
        skills = request.form['skills']
        user = User.query.get(current_user.id)
        user.keywords = skills
        if new_password:
            user.password = new_password
            flash('密码已修改，请牢记您的新密码。')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('UserView:center'))


    def skill_cy(self):
        positions = []
        descs = ''
        pids = current_user.pids.split('-')
        for pid in pids:
            if pid:
                position = Position.query.get(pid)
                if position:
                    positions.append(position)
        for position in positions:
            descs += position.description
        wordclouds = description_cy(descs)

        data = {}
        for item in wordclouds:
            data[item[0]] = item[1]

        session['user_skill'] = data

        color_mask = imread('./app/static/img/dear-r.png')
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
        word_cloud.to_file("./app/static/cy_pic/user/" + str(current_user.id) + "_skill.jpg")  # 保存图片

        return redirect(url_for('UserView:center'))



    @route('/jobs/<pid>')
    @login_required
    def show_position(self, pid):
        position = Position.query.get(pid)
        company = Company.query.get(position.cid)
        data = {"position": position, "company": company}
        description = position.description.split('\n')

        u_positions = current_user.pids
        u_positions = u_positions.split('-')
        if pid in u_positions:
            collection = 1
        else:
            collection = 0

        return render_template('show_position.html', data=data, description=description, collection=collection)

    @route('/collection/<pid>')
    @login_required
    def collection_position(self, pid):
        user = User.query.get(current_user.id)
        collection_pids = user.pids
        collection_pids = collection_pids.split('-')
        if pid not in collection_pids:
            collection_pids.append(pid)
        collection_pids = '-'.join(collection_pids)
        user.pids = collection_pids
        db.session.add(user)
        db.session.commit()
        flash('已收藏该职位！')
        return redirect(url_for('UserView:show_position', pid=pid))

    @route('/cancel_collection/<pid>')
    @login_required
    def cancel_collection(self, pid):
        user = User.query.get(current_user.id)
        collection_pids = user.pids
        collection_pids = collection_pids.split('-')
        if pid in collection_pids:
            collection_pids.remove(pid)
        collection_pids = '-'.join(collection_pids)
        user.pids = collection_pids
        db.session.add(user)
        db.session.commit()
        flash('已取消收藏该职位！')
        return redirect(url_for('UserView:show_position', pid=pid))

    @route('/feedback/<pid>')
    @login_required
    def feedback(self, pid):
        feedbacks = Feedback.query.all()
        for feedback in feedbacks:
            if str(feedback.pid) == pid:
                flash('感谢您的反馈，请待管理员处理。')
                return redirect(url_for('UserView:show_position', pid=pid))
        feedback = Feedback()
        feedback.fid = datetime.now().strftime('%y%m%d%f')[:10]
        feedback.uid = current_user.id
        feedback.pid = pid
        db.session.add(feedback)
        db.session.commit()
        flash('感谢您的反馈，请待管理员处理。')
        return redirect(url_for('UserView:show_position', pid=pid))
