from app import app, db, AdminUser  # Ensure required modules are imported

with app.app_context():
    # Check if an admin already exists to prevent duplicates
    if not AdminUser.query.filter_by(username="admin").first():
        new_admin = AdminUser(username="admin")
        new_admin.set_password("admin_Pnl@72")  # Change this to a strong password
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists.")
