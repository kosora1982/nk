import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models.models import db, Widget, Page
from datetime import datetime

def seed_widgets():
    with app.app_context():
        # Vremenska prognoza primer
        if not Widget.query.filter_by(name='Vremenska prognoza').first():
            widget = Widget(name='Vremenska prognoza', description='Prikazuje vremensku prognozu', content='<div>Vreme</div>')
            db.session.add(widget)
            db.session.commit()
            print('Widget seeded.')
        else:
            print('Widget already exists.')

        # Obrisi stari Dnevni horoskop widget ako postoji
        old_widget = Widget.query.filter_by(name='Dnevni horoskop').first()
        if old_widget:
            for page in old_widget.pages:
                page.widgets.remove(old_widget)
            db.session.delete(old_widget)
            db.session.commit()
            print('Stari Dnevni horoskop widget obrisan.')

        # Dnevni horoskop widget - čist HTML
        dnevni_widget = Widget(
            name='Dnevni horoskop',
            description='Automatski generisan dnevni horoskop za sve znakove',
            content='{{ dnevni_horoskop_widget() }}'
        )
        db.session.add(dnevni_widget)
        db.session.commit()
        print('Dnevni horoskop widget seeded.')

        # Poveži widget sa stranicom dnevni-horoskop
        page = Page.query.filter_by(slug='dnevni-horoskop').first()
        if page and dnevni_widget not in page.widgets:
            page.widgets.append(dnevni_widget)
            db.session.commit()
            print('Dnevni horoskop widget povezan sa stranicom dnevni-horoskop.')
        elif not page:
            print('Stranica dnevni-horoskop ne postoji!')
        else:
            print('Dnevni horoskop widget već povezan sa stranicom.')

if __name__ == '__main__':
    seed_widgets()
