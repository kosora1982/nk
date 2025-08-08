from app import app
from models.models import db, Widget

with app.app_context():
    widgets = Widget.query.all()
    for w in widgets:
        print(f"Widget: {w.name}")
        print("CONTENT:")
        print(w.content)
        print("-"*40)
