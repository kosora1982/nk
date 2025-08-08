import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models.models import db, Page
from datetime import datetime

def seed_pages():
    with app.app_context():
        # Pocetna
        if not Page.query.filter_by(slug='pocetna').first():
            page = Page(
                title='Početna',
                slug='pocetna',
                content='Dobrodošli na početnu stranicu.',
                created_at=datetime.utcnow(),
                published=True
            )
            db.session.add(page)
            db.session.commit()
            print('Page seeded.')
        else:
            print('Page already exists.')

        # Horoskop
        horoskop = Page.query.filter_by(slug='horoskop').first()
        if not horoskop:
            horoskop = Page(
                title='Horoskop',
                slug='horoskop',
                content='Stranica za horoskop.',
                created_at=datetime.utcnow(),
                published=True
            )
            db.session.add(horoskop)
            db.session.commit()
            print('Horoskop page seeded.')
        else:
            print('Horoskop page already exists.')

        # Podstranice
        subpages = [
            ('Dnevni horoskop', 'dnevni-horoskop', 'Dnevni horoskop sadržaj.'),
            ('Nedeljni horoskop', 'nedeljni-horoskop', 'Nedeljni horoskop sadržaj.'),
            ('Mesecni horoskop', 'mesecni-horoskop', 'Mesecni horoskop sadržaj.'),
            ('Godisnji horoskop', 'godisnji-horoskop', 'Godisnji horoskop sadržaj.')
        ]
        for title, slug, content in subpages:
            if not Page.query.filter_by(slug=slug).first():
                subpage = Page(
                    title=title,
                    slug=slug,
                    content=content,
                    created_at=datetime.utcnow(),
                    published=True,
                    parent_id=horoskop.id
                )
                db.session.add(subpage)
                print(f'{title} page seeded.')
            else:
                print(f'{title} page already exists.')
        db.session.commit()

if __name__ == '__main__':
    seed_pages()
