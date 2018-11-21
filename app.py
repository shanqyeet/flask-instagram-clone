from flask import Flask, render_template, redirect, request, flash, session, url_for
from database import db, app, login
from werkzeug.security import generate_password_hash, check_password_hash
from users.forms import SignupForm
from flask_login import  current_user, login_user, login_required, logout_user
from models import User

@login.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None

@app.route("/")
def home():
    form = SignupForm()

    return render_template('home.html', form=form)

@app.route("/protected")
@login_required
def protected():
    return "protected area"

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'GET':
        return render_template('signup.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(username=form.username.data).first():
                return "Username already exists"
            else:
                newuser = User(username=form.username.data, email=form.email.data, password=form.password.data)
                db.session.add(newuser)
                db.session.commit()
                flash("Your account has been successfully created!")
                return redirect('/')
        else:
            return "Form didn't validate"


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = SignupForm()
    if request.method == "GET":
        return render_template("signin.html",form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username = form.username.data).first()
            if user:
                if user.salt_tasting(form.password.data):
                    login_user(user)
                    flash("We have successfully signed you in!")
                    return redirect(f'/users/{user.id}')
                else:
                    flash("Wrong password, access denied")
                    return redirect(request.referrer)
            else:
                flash("User does not exist")
                return redirect(request.referrer)
        else:
            flash("Form not validated")
            return redirect(request.referrer)

@app.route('/users/<id>', methods=['GET'])
def show(id):
    user = User.query.get(id)
    print(current_user)
    if current_user == user:
        return render_template('show.html', current_user = current_user)
    else:
        flash('Sorry you are not authorized to access the page')
        return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    print("in logout??")
    print(current_user)
    print(current_user.is_anonymous)
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run()
