from app import app, db, AdminUser

with app.app_context():
    admin = AdminUser.query.first()
    if admin:
        print(f"Admin user exists: {admin.username}")
    else:
        print("No admin user found.")

