from flask import render_template, url_for, request, redirect
from flask_classy import FlaskView, route

from app.models.detail import Detail
from app.models.position import Position


class DetailView(FlaskView):

    # 根路由
    @route('/<id>')
    def index(self, id):
        detail = Detail.query.filter_by(pid=id).first()
        position = Position.query.filter_by(pid=id).first()
        return render_template('detail.html', detail=detail, position=position)
