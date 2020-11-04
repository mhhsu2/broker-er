import yaml
import os
import constant

from flask import Flask, render_template, request, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

from db import Database


app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = 'my key values'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User login
# TODO: Move to individual file with blueprint registration
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    db = Database()
    if user_id != db.get_user_id(user_id):
        return

    user = User()
    user.id = user_id
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    user_id = request.form['user_id']
    password = request.form['password']

    db = Database()
    if (user_id == db.get_user_id(user_id)) and (password == db.get_user_password(user_id)):
        user = User()
        user.id = user_id
        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for('home'))

#TODO:
@app.route("/register", methods=["GET"])
def register():
    pass

# This is home, probably need to get rid of this and change to show stocks :)
@app.route('/', methods=['GET', 'POST'])
def home():
    db = Database()
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users(username, email, password) VALUES(%s,%s, %s)",(username,email, password))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')

    stockInfo = db.select_stock_with_latest_info()
    return render_template('home.html', stockInfo=stockInfo)

@app.route('/stock/<ticker>', methods=['GET'])
def stock(ticker):
    db = Database()
    stockData = db.select_stock_with_daily_price(ticker)
    return render_template('stock.html', ticker=ticker, stockData=stockData)


@app.route('/watchlist', methods=['GET','POST'])
@login_required
def watchlist():
    # Get current user id with "current_user.id"


    db = Database()
    companyData = db.watchlist_default(current_user.id)
    if request.method == 'POST':

        stockDetails = request.form
        ticker = stockDetails['ticker']

        #SEARCH
        if stockDetails['button'] == 'SEARCH':
            companyData = db.watchlist_search(ticker)

        #INSERT
        elif stockDetails['button'] == 'INSERT':
            db.watchlist_insert(current_user.id, ticker)
            companyData = db.watchlist_default(current_user.id)

        #UPDATE
        elif stockDetails['button'] == 'UPDATE':

            db.watchlist_update(current_user.id,ticker)
            companyData = db.watchlist_default(current_user.id)

        #DELETE
        elif stockDetails['button'] == 'DELETE':

            db.watchlist_delete(current_user.id,ticker)
            companyData = db.watchlist_default(current_user.id)


    return render_template('watchlist.html', companyData = companyData)


if __name__ == '__main__':
    app.run(debug=True)