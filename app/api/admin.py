import os
from werkzeug.utils import secure_filename

from flask import render_template, url_for, request, redirect, Response, current_app, flash
from flask_classy import FlaskView, route

from app.extensions import db
from app.models.feedback import Feedback
from app.models.position import Position

from app.models.user import User


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

    def database(self):
        return render_template('admin_database.html')

    @route('/update_database/', methods=['POST', 'GET'])
    def update_database(self):
        if request.method == 'POST':
            if request.files['category']:
                f = request.files['category']
                path = os.path.join(current_app.config['UPLOADED_PATH'], 'category.txt')
                f.save(path)
        # 调用爬虫
        os.system('./update_database.sh')
        return redirect(url_for('AdminView:database'))

    def deal(self):
        datas = []
        feedbacks = Feedback.query.all()
        for feedback in feedbacks:
            position = Position.query.get(feedback.pid)
            user = User.query.get(feedback.uid)
            fid = str(feedback.fid)
            f_time = '20{0}-{1}-{2}'.format(fid[:2], fid[2:4], fid[4:6])
            datas.append({'position': position, 'user': user, 'f_time': f_time, 'fid': fid})
        return render_template('admin_deal.html', datas=datas)

    @route('/deal_position/<fid>')
    def deal_position(self, fid):
        feedback = Feedback.query.get(fid)
        position = Position.query.get(feedback.pid)
        db.session.delete(position)
        db.session.delete(feedback)
        db.session.commit()
        return redirect(url_for('AdminView:deal'))

    @route('/preserve_position/<fid>')
    def preserve_position(self, fid):
        feedback = Feedback.query.get(fid)
        db.session.delete(feedback)
        db.session.commit()
        return redirect(url_for('AdminView:deal'))
