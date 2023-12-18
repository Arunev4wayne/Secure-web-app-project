import mysql.connector
from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'secretkey'

db_config = {
    'host': 'eu-west.connect.psdb.cloud',
    'user': 'dsis161qa17e6ojjy41w',
    'password': 'pscale_pw_7V9GBZruXMw8Kv2tZUtlStSdWMT3Vpz3osUthNCHVEp',
    'database': 'swd',
}


def execute_query(query, values=None):
  # Connect to MySQL database
  connection = mysql.connector.connect(**db_config)
  cursor = connection.cursor(
      dictionary=True
  )  # Use dictionary=True to get results as a list of dictionaries

  # Execute the provided query and fetch all results
  if values:
    cursor.execute(query, values)
  else:
    cursor.execute(query)

  result = cursor.fetchall()

  cursor.close()
  connection.close()

  return result


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
    insert_query = ("INSERT INTO admin (name, password, email) "
                    "VALUES (%s, %s, %s)")
    values = (username, password, email)

    try:
      cursor.execute(insert_query, values)
      connection.commit()
      cursor.close()
      connection.close()
      return redirect(url_for(
          'admin_login.html'))  # Redirect to admin login page on success
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
        return redirect(url_for(
            'admin_dashboard'))  # Redirect to admin dashboard page on success
      else:
        return "Invalid email or password."

    except mysql.connector.Error as err:
      print(f"Error: {err}")
      return "Error occurred during login."

  return render_template('admin_login.html')


@app.route('/index/signup', methods=['GET', 'POST'])
def user_signup():
  if request.method == 'POST':
    # Retrieve form data
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # Connect to MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Insert data into the admin table (replace 'admin' with your actual table name)
    insert_query = ("INSERT INTO users (username, password, email) "
                    "VALUES (%s, %s, %s)")
    values = (username, password, email)

    try:
      cursor.execute(insert_query, values)
      connection.commit()
      cursor.close()
      connection.close()
      return redirect(
          url_for('index'))  # Redirect to admin login page on success
    except mysql.connector.Error as err:
      print(f"Error: {err}")
      connection.rollback()
      return "Error occurred during registration."

  return render_template('index.html')


@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
  if request.method == 'POST':
    # Retrieve form data
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # Connect to MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Insert data into the admin table (replace 'admin' with your actual table name)
    insert_query = ("INSERT INTO users (username, password, email) "
                    "VALUES (%s, %s, %s)")
    values = (username, password, email)

    try:
      cursor.execute(insert_query, values)
      connection.commit()
      cursor.close()
      connection.close()
      return redirect(url_for(
          'user_management'))  # Redirect to admin login page on success
    except mysql.connector.Error as err:
      print(f"Error: {err}")
      connection.rollback()
      return "Error occurred during registration."

  return render_template('user_management.html')


@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
  # Connect to MySQL database
  connection = mysql.connector.connect(**db_config)
  cursor = connection.cursor()

  # Delete the flight from the database by id
  delete_query = "DELETE FROM users WHERE id = %s"

  try:
    cursor.execute(delete_query, (id, ))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('user_management')
                    )  # Redirect to the flight management page on success
  except mysql.connector.Error as err:
    print(f"Error: {err}")
    connection.rollback()
    return "Error occurred during flight deletion."


@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
  # Connect to MySQL database
  connection = mysql.connector.connect(**db_config)
  cursor = connection.cursor(dictionary=True)

  if request.method == 'GET':
    # Select the flight from the database by id to pre-populate the form
    try:
      cursor.execute("SELECT * FROM users WHERE id = %s", (id, ))
      user = cursor.fetchone()
      cursor.close()
      connection.close()

      if user:
        return render_template('user_update.html', user=user, id=id)
      else:
        return "User not found!", 404
    except mysql.connector.Error as err:
      cursor.close()
      connection.close()
      print(f"Error: {err}")
      return "Database error occurred while retrieving flight details.", 500
  elif request.method == 'POST':
    # Process form submission and update the flight details in the database
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']

    # Update the flight details in the database
    update_query = (
        "UPDATE users SET username=%s, email=%s, phone=%s, password=%s WHERE id=%s"
    )
    values = (username, email, phone, password, id)

    try:
      cursor.execute(update_query, values)
      connection.commit()
      cursor.close()
      connection.close()
      return redirect(url_for('user_management')
                      )  # Redirect to the flight management page on success
    except mysql.connector.Error as err:
      print(f"Error: {err}")
      connection.rollback()
      return "Error occurred during user update."

  # If not a POST request, simply display the page as a fallback.
  return render_template('user_management.html')


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
  if request.method == 'POST':
    # Retrieve form data
    email = request.form['email']
    password = request.form['password']

    # Connect to MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Check login credentials (replace 'admin' with your actual table name)
    select_query = "SELECT username, id, email FROM users WHERE email = %s AND password = %s"
    values = (email, password)

    try:
      cursor.execute(select_query, values)
      result = cursor.fetchone()

      if result:
        session['id'] = result[1]
        session['username'] = result[0]
        session['email'] = result[2]
        id = result[1]
        username = result[0]
        email = result[2]
        cursor.close()
        connection.close()
        return redirect(url_for(
            'user_dashboard',id=id, username=username, email=email))  # Redirect to admin dashboard page on success
      else:
        return "Invalid email or password."

    except mysql.connector.Error as err:
      print(f"Error: {err}")
      return "Error occurred during login."

  return render_template('index.html')


@app.route('/get_user_details/<int:id>', methods=['GET'])
def get_user_details(id):
  user_query = "SELECT * FROM users WHERE id = %s"
  user = execute_query(user_query, (id, ))

  # Assuming only one result is expected
  if user:
    return jsonify(user[0])
  else:
    return jsonify(error="User not found"), 404


@app.route('/user_management')
def user_display():
  users_query = "SELECT * FROM users"
  users = execute_query(users_query)

  return render_template('user_management.html', users=users)


@app.route('/admin/fligt_management', methods=['GET', 'POST'])
def add_flight():
  if request.method == 'POST':
    # Retrieve form data
    flightName = request.form['flightName']
    flightNumber = request.form['flightNumber']
    origin = request.form['origin']
    destination = request.form['destination']
    flightStatus = request.form['flightStatus']

    # Connect to MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    check_query = "SELECT * FROM flights WHERE flightNumber = %s"
    cursor.execute(check_query, (flightNumber, ))
    if cursor.fetchone():
      cursor.close()
      connection.close()
      return "Flight number already exists."
    # Insert data into the admin table (replace 'admin' with your actual table name)
    insert_query = (
        "INSERT INTO flights (flightName, flightNumber, origin, destination, flightStatus) "
        "VALUES (%s, %s, %s, %s, %s)")
    values = (flightName, flightNumber, origin, destination, flightStatus)

    try:
      cursor.execute(insert_query, values)
      connection.commit()
      cursor.close()
      connection.close()
      return redirect(url_for('flight_ticket_management')
                      )  # Redirect to admin login page on success
    except mysql.connector.Error as err:
      print(f"Error: {err}")
      connection.rollback()
      return "Error occurred during registration."

  return render_template('admin_dashboard.html')


@app.route('/get_flight_details/<int:flight_id>', methods=['GET'])
def get_flight_details(flight_id):
  flight_query = "SELECT * FROM flights WHERE id = %s"
  flight = execute_query(flight_query, (flight_id, ))

  # Assuming only one result is expected
  if flight:
    return jsonify(flight[0])
  else:
    return jsonify(error="Flight not found"), 404


@app.route('/flight_ticket_management')
def flight_ticket_management_display():
  flights_query = "SELECT * FROM flights"
  flights = execute_query(flights_query)

  return render_template('flight_ticket_management.html', flights=flights)


@app.route('/user_dashboard/')
def flight_display():
    # Retrieve user ID from session
    user_id = session.get('id')
    user_name = session.get('username')
    user_email = session.get('email')

    if user_id is not None:
        # Connect to MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Query flights from the database
        flights_query = "SELECT * FROM flights"
        flights = execute_query(flights_query)

        # Close the database connection
        cursor.close()
        connection.close()

        # Render the template with the flights data
        return render_template('user_dashboard.html', flights=flights, user_id=user_id, user_name=user_name, user_email=user_email)
    else:
        # Redirect to login if user ID is not in session
        return redirect(url_for('user_login'))

@app.route('/user_dashboard/')
def ticket_display():
    # Retrieve user ID from session
    user_id = session.get('id')

    if user_id is not None:
        # Connect to MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Query booked flight tickets for the user
        tickets_query = "SELECT * FROM ticket_bookings WHERE user_id = %s"
        cursor.execute(tickets_query, (user_id,))
        tickets = cursor.fetchall()

        # Close the database connection
        cursor.close()
        connection.close()

        # Render the template with the booked flight tickets data
        return render_template('booked_tickets.html', tickets=tickets, user_id=user_id)
    else:
        # Redirect to login if user ID is not in session
        return redirect(url_for('user_login'))


@app.route('/update_flight/<int:id>', methods=['GET', 'POST'])
def update_flight(id):
  # Connect to MySQL database
  connection = mysql.connector.connect(**db_config)
  cursor = connection.cursor(dictionary=True)

  if request.method == 'GET':
    # Select the flight from the database by id to pre-populate the form
    try:
      cursor.execute("SELECT * FROM flights WHERE id = %s", (id, ))
      flight = cursor.fetchone()
      cursor.close()
      connection.close()

      if flight:
        return render_template('flight_update.html', flight=flight, id=id)
      else:
        return "Flight not found!", 404
    except mysql.connector.Error as err:
      cursor.close()
      connection.close()
      print(f"Error: {err}")
      return "Database error occurred while retrieving flight details.", 500
  elif request.method == 'POST':
    # Process form submission and update the flight details in the database
    flight_name = request.form['flightName']
    flight_number = request.form['flightNumber']
    origin = request.form['origin']
    destination = request.form['destination']
    flight_status = request.form['status']

    # Update the flight details in the database
    update_query = (
        "UPDATE flights SET flightName=%s, flightNumber=%s, origin=%s, destination=%s, flightStatus=%s WHERE id=%s"
    )
    values = (flight_name, flight_number, origin, destination, flight_status,
              id)

    try:
      cursor.execute(update_query, values)
      connection.commit()
      cursor.close()
      connection.close()
      return redirect(url_for('flight_ticket_management')
                      )  # Redirect to the flight management page on success
    except mysql.connector.Error as err:
      print(f"Error: {err}")
      connection.rollback()
      return "Error occurred during flight update."

  # If not a POST request, simply display the page as a fallback.
  return render_template('flight_update.html')


@app.route('/delete_flight/<int:id>', methods=['GET', 'POST'])
def delete_flight(id):
  # Connect to MySQL database
  connection = mysql.connector.connect(**db_config)
  cursor = connection.cursor()

  # Delete the flight from the database by id
  delete_query = "DELETE FROM flights WHERE id = %s"

  try:
    cursor.execute(delete_query, (id, ))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('flight_ticket_management')
                    )  # Redirect to the flight management page on success
  except mysql.connector.Error as err:
    print(f"Error: {err}")
    connection.rollback()
    return "Error occurred during flight deletion."

@app.route('/user/book_ticket', methods=['GET', 'POST'])
def book_ticket():
  if request.method == 'POST':
    # Retrieve form data
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    user_email = request.form['user_email']
    flight_id = request.form['flight_id']
    flight_name = request.form['flight_name']
    flight_number = request.form['flight_number']
    flight_origin = request.form['origin']
    flight_destination = request.form['destination']
    flight_status = request.form['flight_status']
    ticket_status = request.form['ticket_status']

    # Connect to MySQL database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Insert data into the admin table (replace 'admin' with your actual table name)
    insert_query = ("INSERT INTO ticket_bookings (user_id, user_name, user_email, flight_id, flight_name, flight_number, origin, destination, flight_status, ticket_status) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    values = (user_id, user_name, user_email, flight_id, flight_name, flight_number, flight_origin, flight_destination, flight_status, ticket_status)


    try:
      cursor.execute(insert_query, values)
      connection.commit()
      cursor.close()
      connection.close()
      return redirect(url_for(
          'user_dashboard'))  # Redirect to admin login page on success
    except mysql.connector.Error as err:
      print(f"Error: {err}")
      connection.rollback()
      return "Error occurred during registration."

  return render_template('user_dashboard.html')


@app.route('/user/booked_tickets/<int:ticket_id>', methods=['GET', 'POST'])
def cancel_ticket(ticket_id):
  # Connect to MySQL database
  connection = mysql.connector.connect(**db_config)
  cursor = connection.cursor(dictionary=True)

  if request.method == 'POST':
    # Process form submission and update the ticket status in the database
    ticket_status = request.form['ticket_status']

    # Update the ticket status in the database
    update_query = (
        "UPDATE ticket_bookings SET ticket_status=%s WHERE id=%s"
    )
    values = (ticket_status, ticket_id,)  # Ensure the values are passed as a tuple

    try:
      # Pass the 'values' as a second argument which represents parameters for the placeholder in 'update_query'
      cursor.execute(update_query, values)
      connection.commit()
      cursor.close()
      connection.close()
      return redirect(url_for('booked_tickets', user_id=session['id']))
    except mysql.connector.Error as err:
      print(f"Error: {err}")
      connection.rollback()
      cursor.close()
      connection.close()
      return "Error occurred during cancellation."

  # If not a POST request or if the ticket is not found, redirect to the booked tickets view
  return redirect(url_for('booked_tickets', user_id=session['id']))

@app.route('/admin/booked_tickets/<int:ticket_id>', methods=['GET', 'POST'])
def admin_cancel_ticket(ticket_id):
  # Connect to MySQL database
  connection = mysql.connector.connect(**db_config)
  cursor = connection.cursor(dictionary=True)

  if request.method == 'POST':
    # Process form submission and update the ticket status in the database
    ticket_status = request.form['ticket_status']

    # Update the ticket status in the database
    update_query = (
        "UPDATE ticket_bookings SET ticket_status=%s WHERE id=%s"
    )
    values = (ticket_status, ticket_id,)  # Ensure the values are passed as a tuple

    try:
      # Pass the 'values' as a second argument which represents parameters for the placeholder in 'update_query'
      cursor.execute(update_query, values)
      connection.commit()
      cursor.close()
      connection.close()
      return redirect(url_for('booked_tickets_admin'))
    except mysql.connector.Error as err:
      print(f"Error: {err}")
      connection.rollback()
      cursor.close()
      connection.close()
      return "Error occurred during cancellation."

  # If not a POST request or if the ticket is not found, redirect to the booked tickets view
  return redirect(url_for('booked_tickets_admin'))

@app.route('/user/update_profile/<int:user_id>', methods=['GET', 'POST'])
def update_profile(user_id):
  # Connect to MySQL database
  connection = mysql.connector.connect(**db_config)
  cursor = connection.cursor(dictionary=True)

  if request.method == 'POST':
    # Process form submission and update the user status in the database
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Update the user status in the database
    update_query = "UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s"
    values = (username, email, password, user_id)

    try:
      cursor.execute(update_query, values)
      connection.commit()
    except mysql.connector.Error as err:
      print(f"Error: {err}")
      connection.rollback()
    finally:
      cursor.close()
      connection.close()

    return redirect(url_for('user_dashboard'))
  else:
    # Render user details for GET request
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
      return render_template('update_profile.html', user=user, user_id=user_id)
    else:
      return "User not found", 404



@app.route('/admin/dashboard')
def admin_dashboard():
  return render_template('admin_dashboard.html')


@app.route('/user_management')
def user_management():
  return render_template('user_management.html')


@app.route('/user_dashboard/')
def user_dashboard():
  return render_template('user_dashboard.html')


@app.route('/flight_ticket_management')
def flight_ticket_management():
  return render_template('flight_ticket_management.html')


@app.route('/flight_update')
def flight_update():
  return render_template('flight_update.html')

@app.route('/booked_tickets/<int:user_id>')
def booked_tickets(user_id):
  tickets_query = "SELECT * FROM ticket_bookings WHERE user_id = %s"
  tickets = execute_query(tickets_query, (user_id,))

  return render_template('booked_tickets.html', user_id=user_id, tickets=tickets)

@app.route('/booked_tickets_admin/')
def booked_tickets_admin():
  tickets_query = "SELECT * FROM ticket_bookings "
  tickets = execute_query(tickets_query)

  return render_template('booked_tickets_admin.html', tickets=tickets)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
