#https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/

from flask import Flask, render_template, redirect, url_for, request
# import mysql.connector

# create the application object
app = Flask(__name__)

# db = mysql.connector.connect(
#   host="localhost",
#   user="yourusername",
#   password="yourpassword"
# )


# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

@app.route('/admin')
def admin():
    return render_template('admin.html')  # render a template

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            return admin()
        elif request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Please try again.'
    return render_template('login.html', error=error)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)