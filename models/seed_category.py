import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models.models import db, Category

def seed_categories():
    with app.app_context():
        if not Category.query.filter_by(slug='opsta').first():
            category = Category(name='Opšta', slug='opsta', description='Opšta kategorija')
            db.session.add(category)
            db.session.commit()
            print('Category seeded.')
        else:
            print('Category already exists.')

if __name__ == '__main__':
    seed_categories()
