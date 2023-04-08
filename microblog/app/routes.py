#!/usr/bin/env python3

from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Mujico!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'American Psycho movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
