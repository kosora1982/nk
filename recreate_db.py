from app import app
from models.models import db

with app.app_context():
    db.drop_all()
    db.create_all()
    print("All tables dropped and recreated according to models.")
