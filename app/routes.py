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
# def getWishlist();

#     return wishlist;

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


if __name__ == '__main__':
    app.run(debug=True)