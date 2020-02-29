"""
smarthub.app
~~~~~~~~~~~~~~~

This module implements the primary app configuration for SmartHub.
"""

import os
import json

from flask import Flask, request, session, render_template, redirect, url_for
from flask_sslify import SSLify

import requests
from satellites.s import Security


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = b"\x1fS\xc0\x02\xe7'fl\xa4\xe1:\xe7/.\xa3\x95"
    # sslify = SSLify(app)

    @app.route('/')
    def index():
        appfile = open('static/json/apps.json').read()
        apps = json.loads(appfile)

        return render_template('index.html', apps=apps)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            if request.form['password'] != request.form['confirmation']:
                return render_template('signup.html', mismatch=True)

            data = {
                'first_name': request.form['first'],
                'last_name': request.form['last'],
                'username': request.form['username'],
                'email': request.form['email'],
                'sfid': request.form['sfid'],
                'password': request.form['password']}

            response = requests.post(
                'https://s.satellites.smartian.space/create',
                data=json.dumps(data))
            if response.status_code != 200:
                return render_template('signup.html', error=True)

            return render_template('index.html', confirm=True)

        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            security = Security()
            response = security.authenticate(
                request.form['username'],
                request.form['password'])

            if response.status_code == 200:
                token = response.headers['X-Token']
            else:
                return render_template('login.html', error=True)

            response = security.get_users(
                token, username=request.form['username'])
            user = json.loads(response.text)

            session['token'] = token
            session['sfid'] = user[0]['fields']['sfid']

            return redirect(url_for('index'))

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('token', None)
        return redirect(url_for('index'))

    return app