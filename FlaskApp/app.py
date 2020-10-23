from flask import Flask, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Kismish**1'
app.config['MYSQL_DATABASE_DB'] = 'BookYourBook'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('homepage.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

@app.route('/showHomepageSignedIn')
def showHomepageSignedIn():
    return render_template('homepageSignedIn.html')
    
@app.route('/showBookList')
def showBookList():
    return render_template('bookList.html')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')