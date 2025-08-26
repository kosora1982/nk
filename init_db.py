from models.models import db
from app import app
from models.seed_horoscope import run_seeder

with app.app_context():
    db.drop_all()
    db.create_all()
    run_seeder()
    print("Baza je kreirana i napunjena horoskop podacima.")
