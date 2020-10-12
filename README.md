# BookYourBook

# Team Bond -  Group Members 

-> Angela Bansal - bansal34@purdue.edu
-> Dhruv Ramanujan - dramanu@purdue.edu
-> Kaushik Ramachandran - ramach10@purdue.edu
-> Pratyaksh Motwani - pmotwani@purdue.edu


# Project Description

Book Your Book is a service that allows students a centralised portal to exchange and purchase course material for their courses. The main features that the service provides can be broken down into three major faces - Allow students to buy course material from the system, List books that they no longer require to be sold and allow for renting of books for fixed duration. The primary aim of this application is to simplify the process of getting students their course material and removing third party intervention by directly linking the buyer and the seller.

# Users on the Platform can do the following: 

-> Add listing for a book they would like to sell (Book is added to the common book listing page and available with the buy option) <br />
-> Purchase/Rent a book from a seller through the common book listing page (List of books provided by sellers and the rent duration if applicable) <br />
-> Add a listing for the book they would like to rent  out (Book is added to the common listing page with renting option) <br />

# Database Items

According to the current project planning, we plan to have the following tables and specified attributes as part of our database infrastructure:

-> Buyers(buyer_id, name, email)
-> Sellers(seller_id, name, email)
-> Courses(course_id, course_name)
-> Books(isbn, book_name, course_id, seller_id, price, quantity)
-> Purchases(purchase_id, isbn, buyer_id, seller_id, date, price)
-> Rentals(rental_id, isbn, buyer_id, seller_id, date, time_period, price)

The above tables will support add, edit and delete operations and our project would require additional implementation of complex queries to successfully record purchase and rental transactions.

