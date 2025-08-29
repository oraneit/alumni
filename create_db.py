import app as app_module
from models import db

# Flask instance is exposed as 'app' in app.py
app = app_module.app

with app.app_context():
    db.create_all()
    print("Tables created.")
