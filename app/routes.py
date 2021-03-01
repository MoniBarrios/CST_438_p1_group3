from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required

app = Flask(__name__)

# @app.route('/register', methods = ['GET', 'POST'])
# def createAccount():


# @app.route('/login', methods = ['GET', 'POST'])
# def login():


# @app.route('/logout')
# def logout():


# @app.route('/', methods = ['GET', 'POST'])
# @app.route('/home', methods = ['GET', 'POST'])
# # @login_required
# def index():


@app.route('/wishlist', methods = ['GET', 'POST'])
def wishlist():
    return render_template('listpage.html')


if __name__ == '__main__':
    app.run(debug=True)