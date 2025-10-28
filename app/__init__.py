from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, flash


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'

    users = {
        'admin': 'password123',
    }

    @app.context_processor
    def inject_year():
        return {'current_year': datetime.utcnow().year}

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            if users.get(username) == password:
                flash('Logged in successfully!', 'success')
                return redirect(url_for('home'))
            error = 'Invalid username or password. Please try again.'
        return render_template('login.html', error=error)

    return app


app = create_app()
