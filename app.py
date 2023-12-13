from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from models import db, User
from forms import LoginForm

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        @app.route('/admin', methods=['GET', 'POST'])
        def admin():
            form = LoginForm()
            if form.validate_on_submit():
                user = User.query.filter_by(username=form.username.data).first()
                if user and user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for('admin_dashboard'))
            return render_template('admin.html', form=form)

        @app.route('/admin_dashboard')
        @login_required
        def admin_dashboard():
            return render_template('admin_dashboard.html')

        @app.route('/logout')
        @login_required
        def logout():
            logout_user()
            return redirect(url_for('admin'))

@app.route('/user_login', methods=['POST'])
def user_login():
    username = request.form['login_username']
    password = request.form['login_password']
    if username == 'user' and password == 'password':
        return render_template('user_dashboard.html')
    else:
        return redirect(url_for('home'))

@app.route('/user_management')
def user_management():
    return render_template('user_management.html')

@app.route('/flight_ticket_management')
def flight_ticket_management():
    return render_template('flight_ticket_management.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)