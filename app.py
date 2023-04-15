from store_backend import app, db

with app.app_context():
    debug=True
    db.create_all()
