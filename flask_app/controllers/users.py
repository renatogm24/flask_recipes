from flask import render_template, request, redirect, flash, session
from flask_app.models import user
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
  if 'user_id' in session:
    return redirect("/dashboard")
  return render_template("index.html")

@app.route('/')
def index():
  return render_template("index2.html")

@app.route('/register/user', methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
      return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
      "first_name": request.form['first_name'],
      "last_name": request.form['last_name'],
      "email": request.form['email'],
      "password" : pw_hash
    }

    user_id = user.User.save(data)
    session['user_id'] = user_id
    session['user_name'] = request.form['first_name']
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():

    data = { "email" : request.form["email"] }
    user_in_db = user.User.get_user_by_email(data)

    if not user_in_db:
      flash("Invalid Email/Password","login")
      return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
      flash("Invalid Email/Password","login")
      return redirect('/')
    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.first_name
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
  if 'user_id' not in session:
    return redirect("/")
  id = session["user_id"]
  userSession = user.User.get_user_with_recipes_by_id({"id":id})
  return render_template("dashboard.html",userSession=userSession)

@app.route('/logout')
def logout():
  session.clear()
  return redirect("/")
