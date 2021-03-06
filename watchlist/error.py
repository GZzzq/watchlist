from watchlist import app
from flask import render_template


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template('error/400.html'), 400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500
