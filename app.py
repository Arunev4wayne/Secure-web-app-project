import mysql.connector
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Replace these values with your MySQL database credentials
db_config = {
    'host': 'aws.connect.psdb.cloud',
    'user': '81h0m0e7c2mtn1v9xg1y',
    'password': 'pscale_pw_fWucLL8vsPcpzS6JrpOmmwrcV06GT2QdKWEcjMe0xBI',
    'database': 'swd',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Connect to MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert data into the admin table (replace 'admin' with your actual table name)
        insert_query = (
            "INSERT INTO admin (name, password, email) "
            "VALUES (%s, %s, %s)"
        )
        values = (username, password, email)

        try:
            cursor.execute(insert_query, values)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('admin_login.html'))  # Redirect to admin login page on success
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()
            return "Error occurred during registration."

    return render_template('admin_signup.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form['email']
        password = request.form['password']

        # Connect to MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check login credentials (replace 'admin' with your actual table name)
        select_query = "SELECT * FROM admin WHERE email = %s AND password = %s"
        values = (email, password)

        try:
            cursor.execute(select_query, values)
            result = cursor.fetchone()

            if result:
                # Successful login, you may want to store user session here
                cursor.close()
                connection.close()
                return redirect(url_for('admin_dashboard.html'))  # Redirect to admin dashboard page on success
            else:
                return "Invalid email or password."

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "Error occurred during login."

    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')