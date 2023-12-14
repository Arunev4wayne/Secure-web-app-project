import mysql.connector
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Replace these values with your MySQL database credentials
db_config = {
    'host': 'aws.connect.psdb.cloud',
    'user': 'g5tl71xefoqn5g0yup87',
    'password': 'pscale_pw_5Knhle7RHw7CKWxMrH0mMsdOEM2KS81ofhDohcIlHxt',
    'database': 'swd',
}

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
            return redirect(url_for('admin.html'))  # Redirect to admin login page on success
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
                return render_template('admin_dashboard.html')  # Redirect to admin dashboard page on success
            else:
                return "Invalid email or password."

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "Error occurred during login."

    return render_template('admin_login.html')

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')