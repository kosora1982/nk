import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models.models import db, Article, Category
from datetime import datetime

def seed_articles():
    with app.app_context():
        category = Category.query.filter_by(slug='opsta').first()
        if not category:
            print('Category not found. Run seed_category.py first.')
            return
        if not Article.query.filter_by(title='Prvi članak').first():
            article = Article(
                title='Prvi članak',
                content='Ovo je sadržaj prvog članka.',
                created_at=datetime.utcnow(),
                published=True,
                category_id=category.id
            )
            db.session.add(article)
            db.session.commit()
            print('Article seeded.')
        else:
            print('Article already exists.')

if __name__ == '__main__':
    seed_articles()
