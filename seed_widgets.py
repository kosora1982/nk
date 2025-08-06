from models.models import db, Widget
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nk.db'  # Prilagodi po potrebi
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

widgets = [
    Widget(name='Vremenska prognoza', description='Prikazuje trenutnu vremensku prognozu', content='<div>Sunčano, 25°C</div>'),
    Widget(name='Kursna lista', description='Prikazuje aktuelne kurseve valuta', content='<ul><li>EUR: 117.5 RSD</li><li>USD: 108.2 RSD</li></ul>'),
    Widget(name='Citati dana', description='Nasumični inspirativni citat', content='<blockquote>"Sreća prati hrabre."</blockquote>'),
    Widget(name='Astro savet', description='Dnevni astrološki savet', content='<div>Iskoristite dan za nove početke!</div>'),
]

def seed_widgets():
    with app.app_context():
        for w in widgets:
            exists = Widget.query.filter_by(name=w.name).first()
            if not exists:
                db.session.add(w)
        db.session.commit()
        print('Widgeti su uspešno ubačeni!')

if __name__ == '__main__':
    seed_widgets()
