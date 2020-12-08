from flask import Flask, render_template, request
import pymysql
from datetime import date


app = Flask(__name__)

# Google Cloud SQL 
db_user = "root"
db_password = "Team007"
db_name = "BookYourBook"
db_connection_name = "bookapp-final:us-central1:bookdatabase"

# Connecting to DB
def open_connection():

    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    
    # conn = pymysql.connect(user=db_user, password=db_password,
    #                         unix_socket=unix_socket, db=db_name,
    #                         cursorclass=pymysql.cursors.DictCursor,
    #                         )

    try:

        conn = pymysql.connect(user=db_user, password=db_password,
                            unix_socket=unix_socket, db=db_name,
                            cursorclass=pymysql.cursors.DictCursor
                            )
        
        print("Connected to DB!")

        return conn

    except pymysql.MySQLError as e:

        print("Failed to connect to the DB!")
        print(e)

@app.route("/")
def main():
    return render_template('homepage.html')

# Store the user id of the user in session
global_userId = 1

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

    return render_template('signin.html')

@app.route('/signIn',methods=['POST', 'GET'])
def signIn(errorMessage="", requestTrigger=True):
 
    if (request.method == 'POST') and requestTrigger:
        return do_signIn()
    return render_template('signin.html', errorMessage=errorMessage) 


def do_signIn():

    email = request.form['inputEmail']
    password = request.form['inputPassword']

    connection = open_connection()

    with connection.cursor() as cursor:
    
        sql = 'SELECT user_id, user_password FROM Users WHERE user_email=%s;'
        cursor.execute(sql, email)
        result = cursor.fetchone()

    connection.close()

    if result == None:
        return signIn("User does not exist!", False)

    if result['user_password'] == password:
        global_userId = result['user_id']
        return render_template('homepageSignedIn.html')
    else:
        return signIn("Invalid Password!", False)


@app.route('/showHomepageSignedIn')
def showHomepageSignedIn():
    return render_template('homepageSignedIn.html')

@app.route('/sortAsc')
def sortAsc():

    connection = open_connection()

    with connection.cursor() as cursor:
        
        cursor.execute('SELECT * FROM Books ORDER BY purchase_price ASC;')
        result = cursor.fetchall()
        cursor.execute('SELECT course_id, AVG(purchase_price) as avgPP, AVG(rental_price) as avgRP FROM Books GROUP BY course_id;')
        result_avgs = cursor.fetchall()
        print(result)
        print(result_avgs)

    connection.close()

    lenBooks = len(result)
    isbns = []
    book_names = []
    course_ids = []
    seller_ids = []
    purchase_prices = []
    rental_prices = []
    quantities = []

    for i in range(lenBooks):

        isbns.append(result[i]["isbn"])
        book_names.append(result[i]["book_name"])
        course_ids.append(result[i]["course_id"])
        seller_ids.append(result[i]["seller_id"])
        purchase_prices.append(result[i]["purchase_price"])
        rental_prices.append(result[i]["rental_price"])
        quantities.append(result[i]["quantity"])
    
    lenCourses = len(result_avgs)
    courseNames = []
    avgPP = []
    avgRP = []

    for i in range(lenCourses):

        courseNames.append(result_avgs[i]['course_id'])
        avgPP.append(result_avgs[i]['avgPP'])
        avgRP.append(result_avgs[i]['avgRP'])


    return render_template('bookList.html', lenBooks=lenBooks, isbns=isbns, book_names=book_names, course_ids=course_ids, seller_ids=seller_ids, 
    purchase_prices=purchase_prices, rental_prices=rental_prices, quantities=quantities, lenCourses=lenCourses, courseNames=courseNames, avgPP=avgPP, avgRP=avgRP)

@app.route('/sortDesc')
def sortDesc():

    connection = open_connection()

    with connection.cursor() as cursor:
        
        cursor.execute('SELECT * FROM Books ORDER BY purchase_price DESC;')
        result = cursor.fetchall()
        cursor.execute('SELECT course_id, AVG(purchase_price) as avgPP, AVG(rental_price) as avgRP FROM Books GROUP BY course_id;')
        result_avgs = cursor.fetchall()
        print(result)
        print(result_avgs)

    connection.close()

    lenBooks = len(result)
    isbns = []
    book_names = []
    course_ids = []
    seller_ids = []
    purchase_prices = []
    rental_prices = []
    quantities = []

    for i in range(lenBooks):

        isbns.append(result[i]["isbn"])
        book_names.append(result[i]["book_name"])
        course_ids.append(result[i]["course_id"])
        seller_ids.append(result[i]["seller_id"])
        purchase_prices.append(result[i]["purchase_price"])
        rental_prices.append(result[i]["rental_price"])
        quantities.append(result[i]["quantity"])
    
    lenCourses = len(result_avgs)
    courseNames = []
    avgPP = []
    avgRP = []

    for i in range(lenCourses):

        courseNames.append(result_avgs[i]['course_id'])
        avgPP.append(result_avgs[i]['avgPP'])
        avgRP.append(result_avgs[i]['avgRP'])


    return render_template('bookList.html', lenBooks=lenBooks, isbns=isbns, book_names=book_names, course_ids=course_ids, seller_ids=seller_ids, 
    purchase_prices=purchase_prices, rental_prices=rental_prices, quantities=quantities, lenCourses=lenCourses, courseNames=courseNames, avgPP=avgPP, avgRP=avgRP)
    
@app.route('/showBookList')
def showBookList():

    connection = open_connection()

    with connection.cursor() as cursor:
        
        cursor.execute('SELECT * FROM Books ORDER BY isbn ASC;')
        result = cursor.fetchall()
        cursor.execute('SELECT course_id, AVG(purchase_price) as avgPP, AVG(rental_price) as avgRP FROM Books GROUP BY course_id;')
        result_avgs = cursor.fetchall()
        print(result)
        print(result_avgs)

    connection.close()

    # Sample result list
    # result = [{
    #     "isbn": 123,
    #     "book_name": "Book1",
    #     "course_id": "Course1",
    #     "seller_id": "Seller1",
    #     "purchase_price": 20,
    #     "rental_price": 10,
    #     "quantity": 2,
    #     },
    #     {
    #     "isbn": 444,
    #     "book_name": "Book2",
    #     "course_id": "Course2",
    #     "seller_id": "Seller2",
    #     "purchase_price": 5,
    #     "rental_price": 10,
    #     "quantity": 3,
    #     },
    # ]

    lenBooks = len(result)
    isbns = []
    book_names = []
    course_ids = []
    seller_ids = []
    purchase_prices = []
    rental_prices = []
    quantities = []

    for i in range(lenBooks):

        isbns.append(result[i]["isbn"])
        book_names.append(result[i]["book_name"])
        course_ids.append(result[i]["course_id"])
        seller_ids.append(result[i]["seller_id"])
        purchase_prices.append(result[i]["purchase_price"])
        rental_prices.append(result[i]["rental_price"])
        quantities.append(result[i]["quantity"])
    
    lenCourses = len(result_avgs)
    courseNames = []
    avgPP = []
    avgRP = []

    for i in range(lenCourses):

        courseNames.append(result_avgs[i]['course_id'])
        avgPP.append(result_avgs[i]['avgPP'])
        avgRP.append(result_avgs[i]['avgRP'])


    return render_template('bookList.html', lenBooks=lenBooks, isbns=isbns, book_names=book_names, course_ids=course_ids, seller_ids=seller_ids, 
    purchase_prices=purchase_prices, rental_prices=rental_prices, quantities=quantities, lenCourses=lenCourses, courseNames=courseNames, avgPP=avgPP, avgRP=avgRP)

@app.route('/bestSellers')
def bestSellers():

    connection = open_connection()

    with connection.cursor() as cursor:
        
        cursor.execute('SELECT book_name, COUNT(*) as cnt FROM Books JOIN Purchases ON (Books.isbn = Purchases.isbn) GROUP BY Books.isbn')
        result = cursor.fetchall()
        print(result)

    connection.close()

    lenBooks = len(result)
    bookNames = []
    bookCounts = []

    for i in range(lenBooks):

        bookNames.append(result[i]["book_name"])
        bookCounts.append(result[i]["cnt"])
        
    return render_template('bestSellers.html', bookNames=bookNames, bookCounts=bookCounts, lenBooks=lenBooks)  

@app.route('/contactSellers')
def contactSellers():

    connection = open_connection()

    with connection.cursor() as cursor:
        
        cursor.execute('SELECT user_name, user_email, book_name FROM Users JOIN Sellers ON (Users.user_id = Sellers.seller_id) JOIN Books on (Sellers.seller_id = Books.seller_id);')
        result = cursor.fetchall()
        print(result)

    connection.close()

    lenUsers = len(result)
    userNames = []
    userEmails = []
    userBooks = []

    for i in range(lenUsers):

        userNames.append(result[i]["user_name"])
        userEmails.append(result[i]["user_email"])
        userBooks.append(result[i]["book_name"])


    return render_template('contactList.html', userNames=userNames, userEmails=userEmails, userBooks=userBooks, lenUsers=lenUsers)
    

@app.route('/buy',methods=['POST', 'GET'])
def buy(errorMessage="", requestTrigger=True):
 
    # read the posted values from the UI
    if (request.method == 'POST') and requestTrigger:
        return do_buy()
    return showBookList()

def do_buy():

    isbn = request.form['inputIsbn']

    try:

        connection = open_connection()

        with connection.cursor() as cursor:

            # Check if book exists
            sql = 'SELECT * FROM Books WHERE isbn=%s;'
            cursor.execute(sql, isbn)
            main_result = cursor.fetchone()

            if main_result == None:

                return buy("Book does not exist!", False)
            
            if main_result['quantity'] > 1:

                # Check for Buyer in the Buyers table
                sql = 'SELECT * FROM Buyers WHERE buyer_id=%s;'
                cursor.execute(sql, global_userId)
                result = cursor.fetchone()

                if result == None:
                    # Insert into Buyers Table
                    sql = 'INSERT INTO Buyers (buyer_id) VALUES (%s);'
                    cursor.execute(sql, (global_userId))

                # Insert into Purchases Table
                sql = 'INSERT INTO Purchases (isbn, buyer_id, seller_id, purchase_price) VALUES (%s, %s, %s, %s);'
                cursor.execute(sql, (isbn, global_userId, main_result['seller_id'], main_result['purchase_price']))

                # Update the quantity in the Books Table
                sql = 'UPDATE Books SET quantity = quantity - 1 WHERE isbn=%s;'
                cursor.execute(sql, isbn)

            else:

                if main_result['quantity'] == 0:
                
                    return buy("Book not available!", False)

                # Check for Buyer in the Buyers table
                sql = 'SELECT * FROM Buyers WHERE buyer_id=%s;'
                cursor.execute(sql, global_userId)
                result = cursor.fetchone()

                if result == None:
                    # Insert into Buyers Table
                    sql = 'INSERT INTO Buyers (buyer_id) VALUES (%s);'
                    cursor.execute(sql, (global_userId)) 

                # Insert into Purchases Table
                sql = 'INSERT INTO Purchases (isbn, buyer_id, seller_id, purchase_price) VALUES (%s, %s, %s, %s);'
                cursor.execute(sql, (isbn, global_userId, main_result['seller_id'], main_result['purchase_price']))

                # Delete from the Books Table
                sql = 'UPDATE Books SET quantity = 0 WHERE isbn=%s;'
                cursor.execute(sql, isbn)

        connection.commit()

        print("Buy done!")

    except pymysql.MySQLError as e:

        print("Failed to buy!")
        print(e)

        connection.rollback()

    finally:

        if (connection.open):

            connection.close()
            print("Connection is closed!")

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
    date_format = endDate.split("-")
    
    today = date.today() 
    year = int(date_format[0])
    month = int(date_format[1])
    day = int(date_format[2])

    rented_duration = date(year,month,day)

    try:

        connection = open_connection()

        with connection.cursor() as cursor:

            # Check if book exists
            sql = 'SELECT * FROM Books WHERE isbn=%s;'
            cursor.execute(sql, isbn)
            main_result = cursor.fetchone()

            if main_result == None:

                return buy("Book does not exist!", False)
            
            if main_result['quantity'] > 1:

                # Check for Buyer in the Buyers table
                sql = 'SELECT * FROM Buyers WHERE buyer_id=%s;'
                cursor.execute(sql, global_userId)
                result = cursor.fetchone()

                if result == None:
                    # Insert into Buyers Table
                    sql = 'INSERT INTO Buyers (buyer_id) VALUES (%s);'
                    cursor.execute(sql, (global_userId))

                # Insert into Rentals Table
                sql = 'INSERT INTO Rentals (isbn, buyer_id, seller_id, rented_period, rental_price) VALUES (%s, %s, %s, %s, %s);'
                cursor.execute(sql, (isbn, global_userId, main_result['seller_id'], rented_duration, main_result['rental_price']))
                
                # Update the quantity in the Books Table
                sql = 'UPDATE Books SET quantity = quantity - 1 WHERE isbn=%s'
                cursor.execute(sql, isbn)

            else:

                if main_result['quantity'] == 0:
                
                    return rent("Book not available!", False)

                # Check for Buyer in the Buyers table
                sql = 'SELECT * FROM Buyers WHERE buyer_id=%s;'
                cursor.execute(sql, global_userId)
                result = cursor.fetchone()

                if result == None:
                    # Insert into Buyers Table
                    sql = 'INSERT INTO Buyers (buyer_id) VALUES (%s);'
                    cursor.execute(sql, (global_userId))

                # Insert into Rentals Table
                sql = 'INSERT INTO Rentals (isbn, buyer_id, seller_id, rented_period, rental_price) VALUES (%s, %s, %s, %s, %s);'
                cursor.execute(sql, (isbn, global_userId, main_result['seller_id'], rented_duration, main_result['rental_price']))

                # Set qunatity to zero when all books bought or rented
                sql = 'UPDATE Books SET quantity = 0 WHERE isbn=%s;'
                cursor.execute(sql, isbn)

        connection.commit()

        print("Rent done!")

    except pymysql.MySQLError as e:

        print("Failed to rent!")
        print(e)

        connection.rollback()

    finally:

        if (connection.open):

            connection.close()
            print("Connection is closed!")
    

    return render_template('homepageSignedIn.html')


@app.route('/sell',methods=['POST', 'GET'])
def sell(errorMessage="", requestTrigger=True):
 
    if (request.method == 'POST') and requestTrigger:
        return do_sell()
    return render_template('sell.html', errorMessage=errorMessage) 

def do_sell():

    isbn = request.form['inputIsbn']
    bookName = request.form['inputBookName']
    course = request.form['inputCourse']
    name = request.form['inputCourseName']
    p_price = request.form['inputPurchasePrice']
    r_price = request.form['inputRentalPrice']

    try:

        connection = open_connection()

        with connection.cursor() as cursor:

            sql = 'SELECT * FROM Books WHERE isbn=%s;'
            cursor.execute(sql, isbn)
            main_result = cursor.fetchone()

            if main_result == None:

                # Check for Seller in Sellers table
                sql = 'SELECT * FROM Sellers WHERE seller_id=%s;'
                cursor.execute(sql, global_userId)
                result = cursor.fetchone()

                if result == None:
                    # Insert into Sellers Table
                    sql = 'INSERT INTO Sellers (seller_id) VALUES (%s);'
                    cursor.execute(sql, (global_userId))

                # Check for Course in Courses table
                sql = 'SELECT * FROM Courses WHERE course_id=%s;'
                cursor.execute(sql, course)
                result = cursor.fetchone()

                if result == None:
                    # Insert into Courses Table
                    sql = 'INSERT INTO Courses (course_id, course_name) VALUES (%s, %s);'
                    cursor.execute(sql, (course, name))

                #Insert into table if book does not exist
                sql = 'INSERT INTO Books (isbn, book_name, course_id, seller_id, purchase_price, rental_price, quantity) VALUES (%s, %s, %s, %s, %s, %s, %s);'
                cursor.execute(sql, (isbn, bookName, course, global_userId, p_price, r_price, 1))

            else:

                #Increment quantity if book already exists
                sql = 'UPDATE Books SET quantity = quantity + 1 WHERE isbn=%s;'
                cursor.execute(sql, isbn)

        connection.commit()

        print("Sell done!")

    except pymysql.MySQLError as e:

        print("Failed to sell!")
        print(e)

        connection.rollback()

    finally:

        if (connection.open):

            connection.close()
            print("Connection is closed!")
        

    return render_template('homepageSignedIn.html')

    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
