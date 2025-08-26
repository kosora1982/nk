from app import app
from models.models import db, HoroscopeType

with app.app_context():
    types = HoroscopeType.query.all()
    for t in types:
        print(f"id={t.id}, name={t.name}, description={t.description}")
    if not types:
        print('Nema nijednog tipa horoskopa u bazi!')
