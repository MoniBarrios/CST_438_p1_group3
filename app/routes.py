#https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/

from flask import Flask, render_template, redirect, url_for, request

# create the application object
app = Flask(__name__)

users = [
]

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

@app.route('/admin')
def admin():
    return render_template('admin.html')  # render a template

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    username = None
    password = None
    if request.method == 'POST':
      if request.form['username'] == 'admin' and request.form['password'] == 'admin':
          return admin()
      else: #request.form['username'] != 'admin' or request.form['password'] != 'admin':
          for username in users:
            if request.form['username'] == users.key():
              if request.form['pssword'] == users[request.form['username']]:
                return admin()
    return render_template('login.html', error=error)

@app.route('/', methods=['GET', 'POST'])
def create_account():
    error = None
    username = None
    password = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check(password):
            users[username] = password
            return login()
        else:
            error = reason(password)
    return render_template('create_account.html', error=error)



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)