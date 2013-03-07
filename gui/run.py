#!/usr/bin/env python
"""
AJAX IOIO
"""

import logging
logging.basicConfig(level=logging.DEBUG)
import webbrowser

import flask
import gevent
import gevent.monkey
import gevent.wsgi

import flask_ajaxify
import ioio

port = '/dev/ttyACM0'
timeout = 0.01

board = ioio.open(port, timeout=timeout)


def update():
    while True:
        board.update()
        gevent.sleep(timeout)

app = flask.Flask('IOIO')
gevent.monkey.patch_all()
gevent.Greenlet.spawn(update)
_, app = flask_ajaxify.make_blueprint(board, register=True, app=app)


@app.route('/')
def default():
    return flask.render_template("default.html")


@app.route('/t/<template>')
def template(template):
    return flask.render_template(template)


def run(host='127.0.0.1', port=5000):
    def show_browser():
        gevent.sleep(1)
        webbrowser.open('http://%s:%s' % (host, port))
    gevent.Greenlet.spawn(show_browser)
    gevent.wsgi.WSGIServer((host, port), app).serve_forever()


if __name__ == '__main__':
    run()
