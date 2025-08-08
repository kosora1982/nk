import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models.models import db, User

def seed_users():
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            user = User(username='admin')
            user.set_password('admin123')
            db.session.add(user)
            db.session.commit()
            print('User seeded.')
        else:
            print('User already exists.')

if __name__ == '__main__':
    seed_users()
