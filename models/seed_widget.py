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

        # Widgeti za sve tipove horoskopa
        widget_defs = [
            {
                "name": "Dnevni horoskop",
                "description": "Automatski generisan dnevni horoskop za sve znakove",
                "content": "{{ dnevni_horoskop_widget() }}",
                "slug": "dnevni-horoskop"
            },
            {
                "name": "Nedeljni horoskop",
                "description": "Automatski generisan nedeljni horoskop za sve znakove",
                "content": "{{ nedeljni_horoskop_widget() }}",
                "slug": "nedeljni-horoskop"
            },
            {
                "name": "Mesecni horoskop",
                "description": "Automatski generisan mesečni horoskop za sve znakove",
                "content": "{{ mesecni_horoskop_widget() }}",
                "slug": "mesecni-horoskop"
            },
            {
                "name": "Godisnji horoskop",
                "description": "Automatski generisan godišnji horoskop za sve znakove",
                "content": "{{ godisnji_horoskop_widget() }}",
                "slug": "godisnji-horoskop"
            }
        ]

        for wdef in widget_defs:
            # Obrisi stari widget ako postoji
            old_widget = Widget.query.filter_by(name=wdef["name"]).first()
            if old_widget:
                for page in old_widget.pages:
                    page.widgets.remove(old_widget)
                db.session.delete(old_widget)
                db.session.commit()
                print(f'Stari {wdef["name"]} widget obrisan.')

            # Kreiraj novi widget
            widget = Widget(
                name=wdef["name"],
                description=wdef["description"],
                content=wdef["content"]
            )
            db.session.add(widget)
            db.session.commit()
            print(f'{wdef["name"]} widget seeded.')

            # Poveži widget sa odgovarajućom stranicom
            page = Page.query.filter_by(slug=wdef["slug"]).first()
            if page and widget not in page.widgets:
                page.widgets.append(widget)
                db.session.commit()
                print(f'{wdef["name"]} widget povezan sa stranicom {wdef["slug"]}.')
            elif not page:
                print(f'Stranica {wdef["slug"]} ne postoji!')
            else:
                print(f'{wdef["name"]} widget već povezan sa stranicom.')

if __name__ == '__main__':
    seed_widgets()
