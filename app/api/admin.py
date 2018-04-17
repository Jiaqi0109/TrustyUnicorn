import os
from werkzeug.utils import secure_filename

from flask import render_template, url_for, request, redirect, Response, current_app, flash
from flask_classy import FlaskView, route

from app.models.position import Position

import json

class AdminView(FlaskView):

    # 根路由
    @route('/', methods=['POST', 'GET'])
    def index(self):
        if request.method == 'POST':
            auth = request.form['auth']
            if auth == current_app.config['ADMIN_AUTH']:
                flash('欢迎 Administrator！')
                return redirect(url_for('AdminView:database'))
            else:
                flash('认证指令错误！')
                return render_template('admin_auth.html')
        return render_template('admin_auth.html')


    @route('/database/', methods=['POST', 'GET'])
    def database(self):
        if request.method == 'POST':
            if request.files['category']:
                f = request.files['category']
                path = os.path.join(current_app.config['UPLOADED_PATH'], 'category.txt')
                f.save(path)
        # 调用爬虫
        return render_template('admin_database.html')

    def deal(self):
        positions = []
        deal = []
        s = []
        positions.append(Position.query.get(11684))
        positions.append(Position.query.get(24629))
        positions.append(Position.query.get(36944))
        positions.append(Position.query.get(111889))
        s.append(Position.query.get(114090))
        deal.append(Position.query.get(117531))
        deal.append(Position.query.get(119814))
        return render_template('admin_deal.html', positions=positions, deal=deal, s=s)
