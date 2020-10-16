from flask import Flask, render_template, request, redirect,url_for
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# configure your yaml
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

# This is home, probably need to get rid of this and change to show stocks :)
@app.route('/', methods=['GET', 'POST'])
def home():
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
    return render_template('home.html')


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)


@app.route('/watchlist', methods=['GET','POST'])
def watchlist():

    cur = mysql.connection.cursor()
    cur.execute("SELECT* FROM Watchlist")
    companyData = cur.fetchall()

    if request.method == 'POST':

        stockDetails = request.form

        #SEARCH
        if stockDetails['button'] == 'SEARCH':


            company_name = stockDetails['company_name']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Watchlist WHERE company_name like '%s'" %company_name)
            companyData = cur.fetchall()

        #INSERT
        elif stockDetails['button'] == 'INSERT':

            company_name = stockDetails['company_name']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Watchlist(username, company_name) VALUES(%s, %s)",('max',company_name))
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("SELECT* FROM Watchlist")

        #UPDATE
        if stockDetails['button'] == 'UPDATE':

            company_name = stockDetails['company_name']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Watchlist SET owned = IF (owned,0,1) WHERE company_name like '%s'" %company_name)
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("SELECT* FROM Watchlist")

        #DELETE
        elif stockDetails['button'] == 'DELETE':

            company_name = stockDetails['company_name']
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM Watchlist WHERE company_name like '%s'" %company_name)
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("SELECT* FROM Watchlist")


        companyData = cur.fetchall()
        cur.close()

    return render_template('watchlist.html', companyData = companyData)


if __name__ == '__main__':
    app.run(debug=True)
