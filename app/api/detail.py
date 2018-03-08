from flask import render_template, url_for, request, redirect
from flask_classy import FlaskView

from app.models.detail import Detail


class DetailView(FlaskView):

    # 根路由
    def index(self):
        return render_template('detail.html')
