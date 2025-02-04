import sqlite3
from flask import Flask, request, session, redirect, url_for, render_template, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import functools
from blog import bp as blogbp
from auth import bp as authbp

app = Flask(__name__)

app.config.from_mapping(SECRET_KEY = 'ASDKsaldakdl;213q123aSDK1')

app.register_blueprint(blogbp)
app.register_blueprint(authbp)

app.add_url_rule('/', endpoint='blog.index')
