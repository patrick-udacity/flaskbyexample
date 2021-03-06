from flask import Flask, render_template
from flask_login import LoginManager
from flask_login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask import redirect
from flask import request
from flask import url_for

from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper
from user import User

DB = DBHelper()
PH = PasswordHelper()

app = Flask(__name__)
app.secret_key = ('nAfgjUZtY5A8GShkhksmiTi+QNeL7+eo4eUkLp' + 
    '3KyNbHmL6QbtNq0+82Y56FhIQmmXj9glzYdAKX1K26I8NpRepExqhibO52jGX')
login_manager = LoginManager(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/account")
@login_required
def account():
    return "You are logged in"

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user_password = DB.get_user(email)
    stored_user = DB.get_user(email)
    if stored_user and PH.validate_password(password,
            stored_user['salt'], stored_user['hashed']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    return home()

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for('home'))
    if DB.get_user(email):
        return redirect(url_for('home'))
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)