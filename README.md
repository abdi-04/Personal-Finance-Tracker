# Personal-Finance-Tracker
A school project for the course databases and webprogramming

# Requirements Checklist

## What to do first?

1. Clone the repository to your local machine using the following command:


2. Navigate to the project directory by using the given command and run the flask application:

   ```bash
   cd FinanceTracker
   ```
   



## Each completed item is marked with x.


| # | Criteria | Points | Done |
|---|----------|--------|------|
| 1 | Idea followed | 5 | x |
| 2 | How to Run works | 3 | x |
| 3 | Log in and register users | 5 | x |
| 4 | Example data | 2 | x |
| 5 | JS Form validation | 5 | x |
| 6 | Sort and search in JS | 3 | x |
| 7 | Sort stored | 3 | x |
| 8 | >5 Tables | 6 | x |
| 9 | Complex queries | 3 | x |
| 10 | Insert, Update, delete data | 6 | x |
| 11 | AJAX request used | 5 | x |
| 12 | Dynamic layout | 2 | x |
| 13 | Semantic tags | 2 | x |
| 14 | Code separation | 4 | x |
| 15 | Best practice routes | 5 | x |
| 16 | Server side validation | 4 | x |
| 17 | Errors handled and displayed | 5 | x |
| 18 | Authentication | 4 | x |
| 19 | Access control | 3 | x |

---

## Extra Features


### CSS features

Phone-size responsive layout | 5 | x |

### JS features

Additional AJAX beyond single request | JS | x |
Display of graphs | JS | x |

### Python features

| Flask-Login | Python | x |
| Image storage and validation | Python | x |



---


## How to Run

1. To create the database and populate it with the seeded example data, simply run the Flask application by starting `app.py`.

   When the application starts, it will automatically create the database and all required tables if they do not already exist. It will also insert the example data provided by the seeding functions.

   You can then log in using either the administrator account or the demo user account:

   **Admin User**

   * Email: `admin@financetracker.com`
   * Password: `admin1234`

   **Regular User**

   * Email: `demo@financetracker.com`
   * Password: `demo1234`

---

### How to Insert New Data into the Database

1. To add new seed data, use the `seed.py` file located in the project's root directory. This file contains six Python functions that insert data into their respective tables. To add additional data, simply follow the existing patterns used in these functions. All seeding functions are called from the `seed()` function in `app.py`, which runs when the application starts.

2. If you want to apply changes to the seeded data, you must first delete the existing database tables (using the terminal or another database management tool) and then run the application again. This will trigger the `seed()` function, which will recreate the database and execute all seeding functions in `seed.py`.

   Alternatively, you can modify or add seed data before running the application for the first time, as the database will initially be empty.

3. Additional notes:

   * Database initialization is handled in `database/db.py` by the `init_db()` function, which is called from `app.py` when the application starts.

   * The dashboard uses the external JavaScript library **Chart.js** to display graphs and visualizations. The library is included in the `static` folder and linked through the `base.html` template.

   * For more closer information about insertions, read through the files ( which use other files, primarily from the `database/queries` folder) that are responsible for inserting data into the database, such as `seed.py` and the query files in `database/queries`.
