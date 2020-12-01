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

    if result == None:
        return signIn("User does not exist!", False)

    if result['user_password'] == password:
        return render_template('homepageSignedIn.html')
    else:
        return signIn("Invalid Password!", False)


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

    #Sample result list
    # result = [{
    #     "isbn": 123,
    #     "book_name": "Book1",
    #     "course_id": "Course1",
    #     "seller_id": "Seller1",
    #     "purchase_price": 20,
    #     "rental_price": 10,
    #     },
    #     {
    #     "isbn": 444,
    #     "book_name": "Book2",
    #     "course_id": "Course2",
    #     "seller_id": "Seller2",
    #     "purchase_price": 5,
    #     "rental_price": 10,
    #     }
    # ]

    lenBooks = len(result)
    isbns = []
    book_names = []
    course_ids = []
    seller_ids = []
    purchase_prices = []
    rental_prices = []
    for i in range(lenBooks):
        isbns.append(result[i]["isbn"])
        book_names.append(result[i]["book_name"])
        course_ids.append(result[i]["course_id"])
        seller_ids.append(result[i]["seller_id"])
        purchase_prices.append(result[i]["purchase_price"])
        rental_prices.append(result[i]["rental_price"])
        

    return render_template('bookList.html', lenBooks=lenBooks, isbns=isbns, book_names=book_names, course_ids=course_ids, seller_ids=seller_ids, 
    purchase_prices=purchase_prices, rental_prices=rental_prices)
    
@app.route('/buy',methods=['POST', 'GET'])
def buy(errorMessage="", requestTrigger=True):
 
    # read the posted values from the UI
    if (request.method == 'POST') and requestTrigger:
        return do_buy()
    return showBookList()

def do_buy():
    isbn = request.form['inputIsbn']

    #Fetch necessary values

    #Insert into table

    return render_template('homepageSignedIn.html')


@app.route('/rent',methods=['POST', 'GET'])
def rent(errorMessage="", requestTrigger=True):
 
    # read the posted values from the UI
    if (request.method == 'POST') and requestTrigger:
        return do_rent()
    return showBookList()

def do_rent():
    isbn = request.form['inputIsbn']
    endDate = request.form['inputEndDate']

    #Fetch necessary values

    #Insert into table

    return render_template('homepageSignedIn.html')


@app.route('/sell',methods=['POST'])
def sell(errorMessage="", requestTrigger=True):
 
    if requestTrigger:
        return do_sell()
    return showBookList()

def do_sell():

    print("Sell a book")

    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)