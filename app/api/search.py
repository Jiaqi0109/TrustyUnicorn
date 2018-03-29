from flask import render_template, url_for, request, redirect
from flask_classy import FlaskView


class SearchView(FlaskView):
    route_base = '/'

    # 根路由
    def index(self):
        return render_template('search.html')
