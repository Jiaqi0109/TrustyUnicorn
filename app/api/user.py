from flask import render_template, url_for, request, redirect, Response, flash
from flask_classy import FlaskView, route
from flask_login import login_user, logout_user, login_required, current_user

from app.models.position import Position
from app.models.detail import Detail
from app.models.company import Company
from app.models.user import User
from app.extensions import db
from datetime import datetime

import json


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
            user = User(id=uid, name=username, password=password, email=email)
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
        pids = [42093, 42192, 44349, 67631, 77641]
        for pid in pids:
            position = Position.query.get(pid)
            detail = Detail.query.get(pid)
            company = Company.query.get(position.cid)
            data = {"position": position, "detail": detail, "company": company}
            positions.append(data)
        nums = len(positions)
        print('--------------------')
        print(current_user.id)
        print('--------------------')
        return render_template('user_center.html', positions=positions, nums=nums)



    @route('/jobs/<pid>')
    def show_position(self, pid):
        position = Position.query.get(pid)
        detail = Detail.query.get(pid)
        company = Company.query.get(position.cid)
        data = {"position": position, "detail": detail, "company": company}
        description = detail.description.split('\n')
        return render_template('show_position.html', data=data, description=description)

