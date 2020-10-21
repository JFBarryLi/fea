#!/usr/bin/env python

from flask import Flask

app = Flask('fea')


@app.route('/')
def homepage():
    return 'fea-app api'


app.run()
