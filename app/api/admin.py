from flask import render_template, url_for, request, redirect, Response
from flask_classy import FlaskView, route

from app.models.position import Position

import json


class AdminView(FlaskView):

    # 根路由
    def index(self):
        return render_template('admin.html')
