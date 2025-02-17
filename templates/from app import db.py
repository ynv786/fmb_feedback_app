from app import db
with app.app_context():
    db.drop_all()  # ⚠ This deletes all existing data!
    db.create_all()
exit()
