from flask import render_template, url_for, request, redirect
from flask_classy import FlaskView

from app.models.position import Position


class PositionView(FlaskView):

    # 根路由
    def index(self):
        positions = Position.query.filter_by(city='太原').order_by('publish_time').all()[::-1]
        num = len(positions)

        return render_template('position.html', num=num, positions=positions)
