from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user
from datetime import datetime
import uuid


app = Flask(__name__)
app.config['SECRET_KEY'] = 'application123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.status == 'active':
            print("Username and password matched")
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            print("Username, password, or status mismatch")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match"

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists"

        new_user = User(username=username, status='active')
        new_user.set_password(password)  # Hash the password

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # Redirect to the login page after successful signup

    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    movies = Movie.query.all()

    return render_template('dashboard.html', user=current_user, movies=movies)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    poster_url = db.Column(db.String(200), nullable=False)
    showtimes = db.relationship('Showtime', backref='movie', lazy=True)

class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    time = db.Column(db.String(10), nullable=False)


@app.route('/select_movie', methods=['POST'])
@login_required
def select_movie():
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        # Fetch the selected movie from the database based on movie_id
        selected_movie = Movie.query.get(movie_id)
        if selected_movie:
            print(f"Selected Movie ID: {selected_movie.id}")
            print(f"Selected Movie Title: {selected_movie.title}")
            print(f"Selected Movie Poster URL: {selected_movie.poster_url}")

            # For debugging, you can return JSON data containing the movie details
            return jsonify({
                'movie_id': selected_movie.id,
                'title': selected_movie.title,
                'poster_url': selected_movie.poster_url
            })
        else:
            print("Movie not found")  # Handle the case where the movie doesn't exist

    return redirect(url_for('dashboard'))


@app.route('/book_now', methods=['POST'])
@login_required
def book_now():
    if request.method == 'POST':
        movie_id = request.form.get('movie_id')
        print(f"Booking movie with ID: {movie_id}")

        # Generate a unique confirmation number
        confirmation_number = str(uuid.uuid4())[:5]

        # You can add more booking logic here if needed

        # Create a dictionary with booking details
        booking_details = {
            'movie_id': movie_id,
            'confirmation_number': confirmation_number,
            'booking_date': '2023-09-15',  # Set the booking date
            # Add more booking details as needed
        }

        return render_template('book_now.html', booking_details=booking_details)

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)


