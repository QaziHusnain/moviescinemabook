from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user


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


if __name__ == '__main__':
    app.run(debug=True)
