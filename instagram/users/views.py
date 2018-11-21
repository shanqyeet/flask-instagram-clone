from flask import Blueprint, render_template, redirect, request, flash, session, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug import secure_filename
import pdb

from instagram import app, login, db
from instagram.users.forms import SignupForm, EditForm
from instagram.users.models import User

user = Blueprint('user', __name__, template_folder="templates")

@login.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None

@user.route("/protected")
@login_required
def protected():
    return "protected area"

@user.route("/signup", methods=['GET', 'POST'])
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


@user.route("/signin", methods=['GET', 'POST'])
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

@user.route('/users/<id>', methods=['GET'])
@login_required
def show(id):
    user = User.query.get(id)
    print(current_user)
    if current_user == user:
        return render_template('show.html', current_user = current_user)
    else:
        flash('Sorry you are not authorized to access the page')
        return redirect('/')

@user.route('/users/<id>/edit', methods=['GET', 'POST'])
@login_required
def update(id):
    form = EditForm()
    if request.method == "GET":
        return render_template('edit.html', form=form, user=current_user)
    elif request.method == "POST":
        if request.form.get('method') == "PUT":
            if form.validate_on_submit():
                user = User.query.get(id)
                user.username = form.username.data
                user.password = form.password.data
                user.email = form.email.data

                # saving avatar
                # filename = secure_filename(form.avatar.data.filename)
                form.avatar.data.save('/uploads' + form.avatar.data)

                db.session.commit()
                flash('Your profile has been successfully updated')
                redirect({{url_for("show", current_user)}})
            else:
                flash("Form not validated, try again!")
                redirect(request.referrer)

@user.route('/logout', methods=['POST'])
def logout():
    print("in logout??")
    print(current_user)
    print(current_user.is_anonymous)
    logout_user()
    return redirect('/')


