from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thaali_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=True)  # User-entered email
    submitted_email = db.Column(db.String(100), nullable=False)  # Auto-captured email
    date_of_feedback = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # New field for overall rating (1-5)
    feedback = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)  # Auto timestamp
