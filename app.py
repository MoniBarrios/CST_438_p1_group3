#https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
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

cur = db.cursor(buffered=True)

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

def valid_username(username): #will make sure that the username is not already in use
  user = users.keys()
  sql = "SELECT * FROM user WHERE username = %(username)s"
  cur.execute(sql,{'username':username})
  for x in cur:
    if x[1] == username:
      return False
  return True

def valid_password(username, password): #makes sure that the password matches with the user who is trying to log in
  sql = "SELECT * FROM user WHERE username = %(username)s" 
  cur.execute(sql,{'username':username})
  for user in cur:
    if user[2] == password:
      return True
  return False

# use decorators to link the function to a url
@app.route('/', methods=['GET', 'POST'])
def create_account():
    error = None
    username = None
    password = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check(password) and valid_username(username): #if the username is not already in use and the password meets min requirements
          sql = "INSERT INTO `user` (`username`, `password`) VALUES (%(username)s, %(password)s);" 
          cur.execute(sql,{"username":username, "password":password}) #both the username and password gets inserted into the database
          db.commit()
          users[username] = password #locally inserts the username and password into a dictionary
          return redirect(url_for('login'))
        elif not valid_username(username): #if username is already in use
          error = "Username already exists."
        else: #username is free to use but the password does not meet min requirements
          error = reason(password)
    return render_template('create_account.html', error=error)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/viewusers', methods=['GET', 'POST'])
def viewusers():

    sql = "SELECT * FROM user"
    cur.execute(sql)

    accounts =[]
    print(cur.description)
    for account in cur:
        print(account)

        hasList = False

        if (account[3]):
            hasList = True

        temp = {
            'id': account[0],
            'username': account[1],
            'password': account[2],
            'hasList': hasList
        }
        accounts.append(temp)

    
    return render_template('admin_viewusers.html', accounts=accounts)

@app.route('/admin/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):

    sql = "SELECT * FROM user WHERE userID = %(userID)s"
    cur.execute(sql, {'userID': user_id})

    for user in cur:
       
        print(user)

        hasList = False

        if (user[3]):
            hasList = True

        userInfo = {
            'id': user[0],
            'username': user[1],
            'password': user[2],
            'hasList': hasList
        }

    return userInfo

@app.route('/admin/delete_user/<user_id>', methods=['GET','POST'])
def deleteUser(user_id):

  sql ="DELETE FROM user WHERE userID = %(userID)s"
  cur.execute(sql, {'userID':user_id}) 
  db.commit()

  x = {'result': 'Success'}

  return x

    
@app.route('/admin/save_user/<user_id>', methods=['GET', 'POST'])
def save_user(user_id):

    sql = "UPDATE user SET username = %(userName)s, password = %(userPass)s WHERE userID = %(user_id)s"

    userName = request.args.get('userName')
    userPass = request.args.get('userPass')

    cur.execute(sql, {'user_id': user_id, 'userName': userName, 'userPass': userPass})
    db.commit()
    x = {'result': 'Success'}

    return x

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    username = None
    password = None
    
    # print(users)
    x = users.keys()
    if request.method == 'POST':
        sql = "SELECT * FROM user WHERE username = %(username)s" 
        name = request.form['username']
        cur.execute(sql,{'username':name}) #pulls the username from the database

        if request.form['username'] == 'admin' and request.form['password'] == 'admin': #if its the admin that is signing in
          return admin()
        else:
          if cur:
            error = "Username does't exist."
            print(error)

          for user in cur: 
            print(user)
            if name == user[1]: #checks that the username in database macthes with what the user typed in
                if request.form['password'] == user[2]: #if the username matches, it checks that the password to that username also matches
                  return redirect(url_for('landing_page', userId=user[0]))
                else:
                  error = "Wrong password."
                  print(error)

    return render_template('login.html', error=error)

@app.route('/landing-page/<userId>', methods = ['GET', 'POST'])
def landing_page(userId):
  return render_template('index.html', user_id = userId)

@app.route('/user/edit_user/<userId>', methods = ['GET', 'POST'])
def user_edit_user(userId):
  error = None
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['old_password']
    new_password = request.form['new_password']

    if valid_password(username, password): #makes sure the username and password matches
      if check(new_password): #if password meets the min requirements
        sql = "UPDATE user SET password = %(userPass)s WHERE username = %(userName)s" 
        cur.execute(sql, {'userPass': new_password, 'userName':username}) #password gets changed in the database
        db.commit()
        users[username] = new_password #password gets changed locally
        return redirect(url_for('landing_page', userId = userId))
      else:
        error = reason(new_password)
    else:
      error = "Username or Password is wrong."
  return render_template('edit_user.html', error=error)


@app.route('/user/delete_account/<user_name>', methods=['GET','POST'])
def userDeleteAccount(user_name):

    if valid_username(user_name):
        sql ="DELETE FROM user WHERE username = %(username)s"
        cur.execute(sql, {'username':user_name}) 
        db.commit()

        return redirect(url_for('landing_page'))

    else:
      error = "Confirm Username"

    return render_template('edit_user.html', error=error)

def hasItems(userId):
  sql = "SELECT * from user where userID = %(userId)s"
  cur.execute(sql, {'userId': userId})

  for user in cur:
    if (user[3]):
      return True
  
  return False

def getItem(item_id):
  sql = "SELECT * FROM item WHERE itemID = %(item_id)s"
  cur.execute(sql, {'item_id': item_id})
  itemInfo = ""
  
  for item in cur:
    itemInfo = {
        'id': item[0],
        'name': item[1],
        'description': item[2],
        'image': item[3],
        'link': item[4]
    }
  
  return itemInfo

@app.route('/wishlist/<userId>', methods = ['GET', 'POST'])
def wishlist(userId):

  wishlistExists = hasItems(userId)
  items = []

  if (wishlistExists):
    sql = "SELECT * FROM wishlist WHERE userID = %(user_id)s"
    cur.execute(sql, {'user_id': userId})
    
    for item in cur.fetchall():
      print(item)
      iID = item[2]
      temp = getItem(iID)
      items.append(temp)
    

  return render_template('listpage.html', wishlist = items, wishlistExists = wishlistExists, userID = userId)



# @app.route('/edit_item/<item_id>', methods = ['GET', 'POST'])
# def edit_item(item_id):

#     sql = "SELECT * FROM item WHERE itemID = %(itemID)s"
#     cur.execute(sql, {'itemID': item_id})
    
#     for item in cur:
#         itemInfo = {
#             'id': item[0],
#             'image': item[3],
#             'name': item[1],
#             'description': item[2],
#             'link': item[4]
#         }


#     return itemInfo

@app.route('/save_item/<item_id>', methods = ['GET', 'POST'])
def save_item(item_id):

  sql = "UPDATE item SET name = %(newName)s, description = %(newDesc)s, ImgUrl = %(newImage)s, itemLink = %(newLink)s WHERE (itemID = %(itemID)s)"
  newImage = request.args.get('newImage')    
  newName = request.args.get('newName')
  newDesc = request.args.get('newDesc')
  newLink = request.args.get('newLink')    
  cur.execute(sql, {'itemID': item_id, 'newName': newName, 'newImage': newImage, 'newDesc': newDesc, 'newLink': newLink})

  db.commit()

  z = {'response': 'success'}

  return z

def checkItem(itemName):
  sql = "SELECT itemID FROM item WHERE name = %(iName)s"
  cur.execute(sql, {'iName': itemName})

  print('itemName:', itemName)
  
  if cur:
    for id in cur:
      print("in for loop", id[0])
      return id[0]

  return 0

def addItem(userId, itemId):
  sql = "INSERT INTO `wishlist` (`userID`, `itemID`) VALUES (%(user_id)s, %(item_id)s)"
  cur.execute(sql, {'user_id': userId, 'item_id': itemId})
  db.commit()
  return

def updateUser(userID, num):
  sql = "UPDATE user SET wishlist = %(num)s WHERE userID = %(user_id)s"
  cur.execute(sql, {'num': num, 'user_id': userID})
  db.commit()
  return

@app.route('/add_item/<user_id>', methods = ['GET', 'POST'])
def add_item(user_id):

  iUrl = request.args.get('addImage')
  iName = request.args.get('addName')
  iDesc = request.args.get('addDesc')
  iLink = request.args.get('addLink')
  response = ""

  itemExists = checkItem(iName)
  print(itemExists)

  if (not itemExists):
    print("in if statement")
    sql = "INSERT INTO `item` (`name`, `description`, `ImgUrl`, `itemLink`) VALUES (%(iName)s, %(iDesc)s, %(iUrl)s, %(iLink)s)"    
    cur.execute(sql, {"iName": iName, "iDesc": iDesc, "iUrl": iUrl, 'iLink': iLink})
    response = {'response': 'Item was added to wishlist.'}
    db.commit()
    newID = cur.lastrowid
    print(newID)
    addItem(int(user_id), newID)
  else:
    addItem(int(user_id), itemExists)
    response = {'response': 'Item already exists. Added to wishlist from database.'}

  updateUser(user_id, 1)


  return response


@app.route('/admin/viewitems', methods = ['GET', 'POST'])
def items():
  sql = "SELECT * FROM item"
  cur.execute(sql)
  items = []

  for item in cur:

    temp = {
      'id': item[0],
      'name': item[1],
      'description': item[2],
      'image': item[3],
      'link': item[4]
    }
    items.append(temp)

  return render_template('admin_viewitems.html', wishlist = items)




@app.route('/admin/edit_item/<item_id>', methods = ['GET', 'POST'])
def admin_edit_item(item_id):

    sql = "SELECT * FROM item WHERE itemID = %(itemID)s"
    cur.execute(sql, {'itemID': item_id})

    for item in cur:
        itemInfo = {
            'id': item[0],
            'image': item[3],
            'name': item[1],
            'description': item[2],
            'link': item[4]
        }


    return itemInfo

@app.route('/admin/save_item/<item_id>', methods = ['GET', 'POST'])
def admin_save_item(item_id):

    sql = "UPDATE item SET name = %(newName)s, description = %(newDesc)s, ImgUrl = %(newImage)s, itemLink = %(newLink)s WHERE (itemID = %(itemID)s)"
    newImage = request.args.get('newImage')    
    newName = request.args.get('newName')
    newDesc = request.args.get('newDesc')
    newLink = request.args.get('newLink')    
    cur.execute(sql, {'itemID': item_id, 'newName': newName, 'newImage': newImage, 'newDesc': newDesc, 'newLink': newLink})

    db.commit()

    z = {'response': 'success'}

    return z

@app.route('/admin/add_item', methods = ['GET', 'POST'])
def admin_add_item():

    sql = "INSERT INTO `item` (`name`, `description`, `ImgUrl`, `itemLink`) VALUES (%(iName)s, %(iDesc)s, %(iUrl)s, %(iLink)s)"
    iUrl = request.args.get('addImage')
    iName = request.args.get('addName')
    iDesc = request.args.get('addDesc')
    iLink = request.args.get('addLink')     
    cur.execute(sql, {"iName": iName, "iDesc": iDesc, "iUrl": iUrl, 'iLink': iLink})

    db.commit()

    y = {'response': 'success'}

    return y


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)