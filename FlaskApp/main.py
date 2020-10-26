from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Google Cloud SQL 
db_user = "root"
db_password = "Team007"
db_name = "BookYourBook"
db_connection_name = "bookapp-final:us-central1:bookdatabase"

# Connecting to DB
def open_connection():

    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    
    conn = pymysql.connect(user=db_user, password=db_password,
                            unix_socket=unix_socket, db=db_name,
                            cursorclass=pymysql.cursors.DictCursor,
                            )

    # try:
    #     conn = pymysql.connect(user=db_user, password=db_password,
    #                         unix_socket=unix_socket, db=db_name,
    #                         cursorclass=pymysql.cursors.DictCursor
    #                         )
    # except pymysql.MySQLError as e:
    #     print(e)

    return conn

@app.route("/")
def main():
    return render_template('homepage.html')

@app.route('/signUp',methods=['POST', 'GET'])
def signUp(errorMessage="", requestTrigger=True):
 
    # read the posted values from the UI
    if (request.method == 'POST') and requestTrigger:
        return do_signUp()
    return render_template('signup.html', errorMessage=errorMessage) 


def do_signUp():

    name = request.form['inputName']
    email = request.form['inputEmail']
    password = request.form['inputPassword']
    print(name)
    connection = open_connection()

    with connection.cursor() as cursor:
        # Create a new record
        sql = 'INSERT INTO Users (user_name, user_email, user_password) VALUES (%s, %s, %s);'
        cursor.execute(sql, (name, email, password))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        
        cursor.execute('SELECT * FROM Users;')
        result = cursor.fetchall()
        print(result)

    connection.close()

    return render_template('homepageSignedIn.html')

@app.route('/signIn',methods=['POST', 'GET'])
def signIn(errorMessage="", requestTrigger=True):
 
    # read the posted values from the UI
    if (request.method == 'POST') and requestTrigger:
        return do_signIn()
    return render_template('signin.html', errorMessage=errorMessage) 


def do_signIn():

    email = request.form['inputEmail']
    password = request.form['inputPassword']

    connection = open_connection()

    with connection.cursor() as cursor:
        # Create a new record
        sql = 'SELECT user_password FROM Users WHERE user_email=%s'
        cursor.execute(sql, email)
        result = cursor.fetchone()

    connection.close()

    if result['user_password'] == password:
        return render_template('homepageSignedIn.html')
    else:
        return render_template('signin.html')


@app.route('/showHomepageSignedIn')
def showHomepageSignedIn():
    return render_template('homepageSignedIn.html')
    
@app.route('/showBookList')
def showBookList():

    connection = open_connection()

    with connection.cursor() as cursor:
        
        cursor.execute('SELECT * FROM Books;')
        result = cursor.fetchall()
        print(result)

    connection.close()

    return render_template('bookList.html', allBooks=result)
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)