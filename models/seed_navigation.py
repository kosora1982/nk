import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models.models import db, Navigation
from datetime import datetime

def seed_navigation():
    with app.app_context():
        # Pocetna
        if not Navigation.query.filter_by(slug='pocetna').first():
            nav = Navigation(
                title='Početna',
                url='/',
                slug='pocetna',
                icon='fa-home',
                order=1,
                is_active=True,
                is_external=False,
                target='_self',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(nav)
            db.session.commit()
            print('Navigation seeded.')
        else:
            print('Navigation already exists.')

        # Horoskop
        horoskop_nav = Navigation.query.filter_by(slug='horoskop').first()
        if not horoskop_nav:
            horoskop_nav = Navigation(
                title='Horoskop',
                url='/horoskop',
                slug='horoskop',
                icon='fa-star',
                order=2,
                is_active=True,
                is_external=False,
                target='_self',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(horoskop_nav)
            db.session.commit()
            print('Horoskop navigation seeded.')
        else:
            print('Horoskop navigation already exists.')

        # Podstavke
        subnavs = [
            ('Dnevni horoskop', '/dnevni-horoskop', 'dnevni-horoskop'),
            ('Nedeljni horoskop', '/nedeljni-horoskop', 'nedeljni-horoskop'),
            ('Mesecni horoskop', '/mesecni-horoskop', 'mesecni-horoskop'),
            ('Godisnji horoskop', '/godisnji-horoskop', 'godisnji-horoskop')
        ]
        for title, url, slug in subnavs:
            if not Navigation.query.filter_by(slug=slug).first():
                subnav = Navigation(
                    title=title,
                    url=url,
                    slug=slug,
                    icon='fa-star',
                    order=1,
                    is_active=True,
                    is_external=False,
                    target='_self',
                    parent_id=horoskop_nav.id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(subnav)
                print(f'{title} navigation seeded.')
            else:
                print(f'{title} navigation already exists.')
        db.session.commit()

if __name__ == '__main__':
    seed_navigation()
