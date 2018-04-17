from flask import render_template, url_for, request, redirect, Response, flash
from flask_classy import FlaskView, route

from app.models.position import Position
from app.models.detail import Detail
from app.models.company import Company
from app.models.user import User
from app.extensions import db
from datetime import datetime

import json
import time


class UserView(FlaskView):
    route_base = '/'


    @route('/', methods=['POST', 'GET'])
    def index(self):
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
            u = User(uid=uid, name=username, password=password, email=email)
            db.session.add(u)
            db.session.commit()
            flash('欢迎 ' + username + ', 请到个人中心激活账户！')
            return redirect(url_for('HomeView:index'))
        return render_template('register.html')


    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(name=username).first()
            if user:
                if user.password == password:
                    flash('登陆成功！')
                    time.sleep(0.5)
                    return redirect(url_for('HomeView:index'))
            else:
                flash('用户名或密码错误，请重新登陆！')
                time.sleep(0.5)
                return render_template('login.html')
        return render_template('login.html')

    def center(self):
        positions = []
        pids = [42093, 42192, 44349, 67631, 77641]
        for pid in pids:
            position = Position.query.get(pid)
            detail = Detail.query.get(pid)
            company = Company.query.get(position.cid)
            data = {"position": position, "detail": detail, "company": company}
            positions.append(data)
        nums = len(positions)
        return render_template('user_center.html', positions=positions, nums=nums)



    @route('/jobs/<pid>')
    def show_position(self, pid):
        position = Position.query.get(pid)
        detail = Detail.query.get(pid)
        company = Company.query.get(position.cid)
        data = {"position": position, "detail": detail, "company": company}
        description = detail.description.split('\n')
        return render_template('show_position.html', data=data, description=description)

