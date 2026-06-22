# Personal Finance Tracker

A personal finance tracking web application built with Flask and MySQL. Users can manage expenses, monitor their financial activity, and visualize financial data through interactive charts and dashboards.

Developed as part of **DAT130: Databases and Web Programming** at the **University of Stavanger**.

---

## Features

* User registration and authentication
* Role-based access control
* Expense and financial data management
* Client-side and server-side validation
* Search and sorting functionality
* AJAX-powered dynamic updates
* Responsive design for mobile devices
* Interactive charts and data visualizations using Chart.js
* Image upload and validation
* MySQL database with multiple relational tables
* Error handling and user feedback

---

## Tech Stack

### Backend

* Python
* Flask
* Flask-Login

### Frontend

* HTML
* CSS
* JavaScript

### Database

* MySQL

### Libraries

* Chart.js

---


## Installation

### Clone the Repository

```bash
git clone https://github.com/abdi-04/Personal-Finance-Tracker.git
```


### Run the Application

```bash
python app.py
```

The application will automatically:

* Create the database if it does not already exist
* Create all required tables
* Insert example data through the seeding functions

---

## Demo Accounts

### Administrator Account

**Email:** `admin@financetracker.com`

**Password:** `admin1234`

### Demo User Account

**Email:** `demo@financetracker.com`

**Password:** `demo1234`

---



## Database Seeding

Example data is generated through the `seed.py` file.

The seeding process is automatically executed when the application starts for the first time. The application checks whether the database exists and creates all required tables and example data if necessary.

To modify the seeded data:

1. Edit the relevant functions in `seed.py`
2. Delete the existing database tables or database
3. Restart the application

The database initialization process is handled by the `init_db()` function located in:

```text
database/db.py
```

---

## Notable Technical Features

### Authentication and Authorization

* Secure user registration and login
* Session management using Flask-Login
* Protected routes and access control

### Database Design

* Multiple relational database tables
* CRUD operations (Create, Read, Update, Delete)
* Complex SQL queries
* Structured query separation through dedicated query files

### Frontend Functionality

* Client-side form validation
* Search and sorting features
* Responsive design
* Dynamic updates through AJAX

### Data Visualization

The application uses Chart.js to display financial data through interactive charts and graphs.

---

## Academic Context

This project was developed as part of the course:

**DAT130 – Databases and Web Programming**

at the **University of Stavanger**.

The project fulfilled all required criteria and additional bonus features and was awarded the grade **A**.

---


## License

This project is published for portfolio purposes.
