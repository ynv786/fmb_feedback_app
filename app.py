from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from config import Config
from models import db, Feedback

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def feedback_form():
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)

    if request.method == "POST":
        thaali_number = request.form["thaali_number"]
        email = request.form["email"]
        feedback_date = datetime.strptime(request.form["date_of_feedback"], "%Y-%m-%d").date()

        if feedback_date not in [today, yesterday]:
            flash("Invalid date! You can only submit feedback for today or yesterday.", "danger")
            return redirect("/")

        start_time = request.form.get("start_time")
        completion_time = request.form.get("completion_time")
        feedback_text = request.form["feedback"]

        submitted_email = "ynv786@gmail.com"  # Replace with actual login email

        new_feedback = Feedback(
            thaali_number=thaali_number,
            email=email,
            submitted_email=submitted_email,
            date_of_feedback=feedback_date,
            start_time=start_time,
            completion_time=completion_time,
            feedback=feedback_text
        )
        db.session.add(new_feedback)
        db.session.commit()
        flash("Feedback submitted successfully!", "success")
        return redirect("/")

    return render_template("form.html", today=today, yesterday=yesterday)

@app.route("/admin")
def admin_dashboard():
    feedbacks = Feedback.query.order_by(Feedback.submitted_at.desc()).all()
    return render_template("admin.html", feedbacks=feedbacks)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database if it doesn’t exist
    app.run(debug=True)