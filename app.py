from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from config import Config
from models import db, Feedback

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect users to login page if not authenticated

# Admin User Model
class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
def feedback_form():
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)

    if request.method == "POST":
        thaali_number = request.form["thaali_number"]
        email = request.form["email"]
        feedback_date = datetime.strptime(request.form["date_of_feedback"], "%Y-%m-%d").date()
        rating = request.form.get("rating")  # Get the overall rating

        if feedback_date not in [today, yesterday]:
            flash("Invalid date! You can only submit feedback for today or yesterday.", "danger")
            return redirect("/")

        feedback_text = request.form["feedback"]

        submitted_email = "ynv786@gmail.com"  # Replace with actual login email

        new_feedback = Feedback(
            thaali_number=thaali_number,
            email=email,
            submitted_email=submitted_email,
            date_of_feedback=feedback_date,
            feedback=feedback_text,
            rating=rating  # Store rating in the database
        )
        db.session.add(new_feedback)
        db.session.commit()
        flash("Feedback submitted successfully!", "success")
        return redirect("/")

    return render_template("form.html", today=today, yesterday=yesterday)


# Admin Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = AdminUser.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")

# Admin Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Secure Admin Panel (Only Logged-in Users Can Access)
@app.route("/admin")
@login_required
def admin_dashboard():
    feedbacks = Feedback.query.order_by(Feedback.submitted_at.desc()).all()
    return render_template("admin.html", feedbacks=feedbacks)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database if it doesn’t exist
    app.run(debug=True)
