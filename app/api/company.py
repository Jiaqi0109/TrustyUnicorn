from flask import render_template, url_for, request, redirect
from flask_classy import FlaskView

from app.models.company import Company


class CompanyView(FlaskView):

    # 根路由
    def index(self):
        return render_template('company.html')
