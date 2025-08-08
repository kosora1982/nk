import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models.models import db, Design

def seed_designs():
    with app.app_context():
        if not Design.query.first():
            design = Design(theme='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css')
            db.session.add(design)
            db.session.commit()
            print('Design seeded.')
        else:
            print('Design already exists.')

if __name__ == '__main__':
    seed_designs()
