#https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/

from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import mysql.connector

# create the application object
app = Flask(__name__)

users = {
    "admin" : "admin"
}

db = mysql.connector.connect(
  host="pxukqohrckdfo4ty.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
  user="shp71ch2pepxhw20",
  password="x86b1di398unqos5",
  database="hsmokzpr63mftd01"
 )

cur = db.cursor()

def check(password): #will check if password from user is valid
  length = False
  special = False
  if len(password) >= 6:
    length = True

  for x in password:
    if x == '@' or x == '!' or x == '?' or x == '#':
      special = True
  
  return length and special


def reason(password): #will tell you what you need to fix in password
  length = False
  special = False

  if len(password) >= 6:
    length = True

  for x in password:
    if x == '@' or x == '!' or x == '?' or x == '#':
      special = True

  if not special and not length:
    return "Password must contain speacial characters [@, !, ?, #].\nPassword must be longer than 6 characters."
  if not special:
    return "Password must contain speacial characters [@, !, ?, #]."
  if not length:
    return "Password must be longer than 6 characters."

# use decorators to link the function to a url
@app.route('/', methods=['GET', 'POST'])
def create_account():
    error = None
    username = None
    password = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check(password) :
            users[username] = password
            return redirect(url_for('login'))
        else:
            error = reason(password)
    return render_template('create_account.html', error=error)

@app.route('/admin')
def admin():
    return render_template('admin.html')  # render a template

@app.route('/admin/viewusers', methods=['GET', 'POST'])
def viewusers():
    users =[
        {
            'id': 2,
            'username': 'antPerez',
            'password': '$ky1234',
            'hasList': True
        },
        {
            'id': 48,
            'username': 'jayZep',
            'password': 'Pa$$1234',
            'hasList': False
        }
    ]
    return render_template('admin_viewusers.html', users=users)

@app.route('/admin/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):

    user = {
        'username': 'antPerez',
        'password': '$ky1234',
        'hasList': True
    }

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    username = None
    password = None
    
    print(users)
    x = users.keys()
    if request.method == 'POST':
        sql = "SELECT * FROM user WHERE username = %(username)s"
        name = request.form['username']
        cur.execute(sql,{'username':name})

        rows = cur.fetchone()
        if request.form['username'] == rows[0] and request.form['password'] == rows[1]:
          return admin()
        else: #request.form['username'] != 'admin' or request.form['password'] != 'admin':
            for user in x:
                if request.form['username'] == user:
                    if request.form['password'] == users.get(request.form['username']):
                        return redirect(url_for('wishlist'))
                    else:
                        error = "Wrong password."
                else:
                    error = "No user with that username exists"
    return render_template('login.html', error=error)


@app.route('/wishlist', methods = ['GET', 'POST'])
def wishlist():

    items = [
        {
            'id': 1,
            'image': 'https://i.pinimg.com/originals/d3/c4/2a/d3c42a5fafa640f90c4c3746f9fb2c22.jpg',
            'name': 'mountains',
            'description': 'beautiful mountains and lake of who knows where',
            'links': 'google.com'
        },
        {
            'id': 2,
            'image': 'https://cdn1.matadornetwork.com/blogs/1/2019/10/seljalandsfoss-most-instagrammed-waterfalls-world-1200x855.jpg',
            'name': 'waterfall',
            'description': 'beautiful waterfall of unknown area',
            'links': 'amazon.com'
        }
    ]

    return render_template('listpage.html', wishlist = items)

# @app.route('/getWishlist', methods = ['GET', 'POST'])
# def getWishlist():

#     return wishlist

@app.route('/edit_item/<item_id>', methods = ['GET', 'POST'])
def edit_item(item_id):

    item = {
            'id': '1',
            'image': 'https://i.pinimg.com/originals/d3/c4/2a/d3c42a5fafa640f90c4c3746f9fb2c22.jpg',
            'name': 'mountains',
            'description': 'beautiful mountains and lake of who knows where',
            'links': 'google.com'
        }

    return item

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)