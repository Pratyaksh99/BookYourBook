CREATE DATABASE IF NOT EXISTS BookYourBook;

CREATE TABLE IF NOT EXISTS `BookYourBook`.`Users` (

  user_id INTEGER UNIQUE AUTO_INCREMENT,
  user_name VARCHAR(100) NULL,
  user_email VARCHAR(100) NULL,
  user_password VARCHAR(45) NULL,
  PRIMARY KEY (user_id)

);

CREATE TABLE IF NOT EXISTS `BookYourBook`.`Sellers` (

  seller_id INTEGER UNIQUE,
  PRIMARY KEY (seller_id),
  FOREIGN KEY (seller_id) REFERENCES Users(user_id)

);

CREATE TABLE IF NOT EXISTS `BookYourBook`.`Buyers` (

  buyer_id INTEGER UNIQUE AUTO_INCREMENT,
  PRIMARY KEY (buyer_id),
  FOREIGN KEY (buyer_id) REFERENCES Users(user_id)

);

CREATE TABLE IF NOT EXISTS `BookYourBook`.`Courses` (

  course_id VARCHAR(45) UNIQUE,
  course_name VARCHAR(100) NULL,
  PRIMARY KEY (course_id)

);


CREATE TABLE IF NOT EXISTS `BookYourBook`.`Books` (

  isbn INTEGER UNIQUE,
  book_name VARCHAR(100) NULL,
  course_id VARCHAR(45) NULL,
  seller_id INTEGER,
  purchase_price INTEGER,
  rental_price INTEGER,
  quantity INTEGER,
  PRIMARY KEY (isbn),
  FOREIGN KEY (course_id) REFERENCES Courses(course_id),
  FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id)

);


CREATE TABLE IF NOT EXISTS `BookYourBook`.`Purchases` (

  purchase_id INTEGER UNIQUE AUTO_INCREMENT,
  isbn INTEGER,
  buyer_id INTEGER,
  seller_id INTEGER,
  purchase_date DATE,
  purchase_price INTEGER,
  PRIMARY KEY (purchase_id),
  FOREIGN KEY (isbn) REFERENCES Books(isbn),
  FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id),
  FOREIGN KEY (buyer_id) REFERENCES Buyers(buyer_id)

);

CREATE TABLE IF NOT EXISTS `BookYourBook`.`Rentals` (

  rental_id INTEGER UNIQUE AUTO_INCREMENT,
  isbn INTEGER,
  buyer_id INTEGER,
  seller_id INTEGER,
  rental_date DATE,
  rented_period DATE,
  rental_price INTEGER,
  PRIMARY KEY (rental_id),
  FOREIGN KEY (isbn) REFERENCES Books(isbn),
  FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id),
  FOREIGN KEY (buyer_id) REFERENCES Buyers(buyer_id)

);


