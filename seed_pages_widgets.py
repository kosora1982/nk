from models.models import db, Page, Widget
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nk.db'  # Prilagodi po potrebi
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def seed_pages_widgets():
    with app.app_context():
        # Kreiraj stranice
        home = Page.query.filter_by(slug='home').first()
        about = Page.query.filter_by(slug='about').first()
        contact = Page.query.filter_by(slug='contact').first()
        if not home:
            home = Page(slug='home', title='Naslovna', content='Dobrodošli na početnu stranicu!')
            db.session.add(home)
        if not about:
            about = Page(slug='about', title='O nama', content='Ovo je stranica o nama.')
            db.session.add(about)
        if not contact:
            contact = Page(slug='contact', title='Kontakt', content='Kontaktirajte nas ovde.')
            db.session.add(contact)
        db.session.commit()

        # Kreiraj widgete
        vremenska = Widget.query.filter_by(name='Vremenska prognoza').first()
        kursna = Widget.query.filter_by(name='Kursna lista').first()
        citati = Widget.query.filter_by(name='Citati dana').first()
        astro = Widget.query.filter_by(name='Astro savet').first()
        if not vremenska:
            vremenska = Widget(name='Vremenska prognoza', description='Prikazuje trenutnu vremensku prognozu', content='<div>Sunčano, 25°C</div>')
            db.session.add(vremenska)
        if not kursna:
            kursna = Widget(name='Kursna lista', description='Prikazuje aktuelne kurseve valuta', content='<ul><li>EUR: 117.5 RSD</li><li>USD: 108.2 RSD</li></ul>')
            db.session.add(kursna)
        if not citati:
            citati = Widget(name='Citati dana', description='Nasumični inspirativni citat', content='<blockquote>"Sreća prati hrabre."</blockquote>')
            db.session.add(citati)
        if not astro:
            astro = Widget(name='Astro savet', description='Dnevni astrološki savet', content='<div>Iskoristite dan za nove početke!</div>')
            db.session.add(astro)
        db.session.commit()

        # Poveži widgete sa stranicama
        home.widgets = [vremenska, kursna]
        about.widgets = [citati]
        contact.widgets = [astro, kursna]
        db.session.commit()
        print('Stranice i widgeti su uspešno ubačeni i povezani!')

if __name__ == '__main__':
    seed_pages_widgets()
