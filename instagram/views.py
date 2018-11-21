from flask import render_template, redirect, request, flash, session, url_for
from flask_login import current_user, login_user, login_required, logout_user

from instagram import app, login
from .users.forms import SignupForm
from .users.models import User


@app.route("/")
def home():
    form = SignupForm()
    return render_template('home.html', form=form)


