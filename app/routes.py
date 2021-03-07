
#https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/

from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required


# create the application object
app = Flask(__name__)

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


@app.route('/wishlist', methods = ['GET', 'POST'])
def wishlist():

    items = [
        {
            'id': '1',
            'image': 'https://i.pinimg.com/originals/d3/c4/2a/d3c42a5fafa640f90c4c3746f9fb2c22.jpg',
            'name': 'mountains',
            'description': 'beautiful mountains and lake of who knows where',
            'links': 'google.com'
        },
        {
            'id': '2',
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