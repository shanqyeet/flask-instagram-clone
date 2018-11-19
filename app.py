from flask import Flask, render_template, redirect, request, flash, session, url_for
from database import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from models import User


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/sign_up", methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route("/users/new", methods=['POST'])
def create():
    messages = {}
    username = request.form.get('username')
    password = request.form.get('password')

    if not username:
        messages["username"] = "username must exist"

    if not password:
        messages["password"] = "password must exist"

    if len(messages) > 0:
        flash(messages)
        return render_template('signup.html',messages=messages)
    else:
        hashed_password = generate_password_hash(password)
        new_user = User(username, hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("congrats!  your account has been created")
        return redirect('/')

@app.route('/users/<id>', methods=['GET'])
def show(id):
    current_user = User.query.get(id)
    if current_user and session.get('id') and current_user.id == session['id']:
        return render_template('show.html', current_user = current_user)
    else:
        flash('Sorry you are not authorized to access the page')
        return redirect('/')

@app.route("/sign_in", methods=['GET'])
def signin():
    if session.get('logged_in') and session['logged_in'] == True:
        return redirect(f"/users/{session['id']}")
    else:
        return render_template('signin.html')

@app.route("/sessions", methods=["POST"])
def sessions():
    method = request.form.get('_method')
    if method and method == "DELETE":
        session.pop('id', None)
        session.pop('logged_in', None)
        flash('Successfully Logged Out!')
        return redirect('/')
    else:
        current_user_username = request.form.get('username')
        current_user_password = request.form.get('password')
        current_user = User.query.filter_by(username= current_user_username).first()
        if  current_user:
            session['id'] = current_user.id
        else:
            flash("user doesn't exist")
            return redirect('/')

        result = check_password_hash(current_user.password, current_user_password)
        if result:
            session['logged_in'] = True
            flash('Hey, we have successfully logged you in!')
            return redirect(f'/users/{current_user.id}')
        else:
            flash('Password given is wrong, access denied')
            return redirect('/')

if __name__ == '__main__':
    app.run()
