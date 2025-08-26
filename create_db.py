from app import app, db
from models.models import User, Category, Article, Page, Design, Widget, Navigation, HoroscopeType, Horoscope

def create_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create initial data
        create_initial_data()
        print("✅ Initial data created successfully!")

def create_initial_data():
    # Create admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        print("👤 Admin user created")
    
    # Create default design
    design = Design.query.first()
    if not design:
        design = Design()
        db.session.add(design)
        print("🎨 Default design created")
    
    # Create basic navigation
    if not Navigation.query.first():
        nav_items = [
            Navigation(title='Početna', url='/', slug='pocetna', order=1, icon='fas fa-home'),
            Navigation(title='O nama', url='/o-nama', slug='o-nama', order=2, icon='fas fa-info-circle'),
            Navigation(title='Kontakt', url='/kontakt', slug='kontakt', order=3, icon='fas fa-envelope'),
        ]
        for item in nav_items:
            db.session.add(item)
        print("🧭 Basic navigation created")
    
    # Create horoscope types
    horoscope_types = [
        {'name': 'dnevni', 'description': 'Dnevni horoskop'},
        {'name': 'nedeljni', 'description': 'Nedeljni horoskop'},
        {'name': 'mesecni', 'description': 'Mesečni horoskop'},
        {'name': 'godisnji', 'description': 'Godišnji horoskop'},
    ]
    
    for type_data in horoscope_types:
        existing = HoroscopeType.query.filter_by(name=type_data['name']).first()
        if not existing:
            horoscope_type = HoroscopeType(**type_data)
            db.session.add(horoscope_type)
            print(f"🔮 Horoscope type '{type_data['name']}' created")
    
    db.session.commit()
    print("💾 All data saved to database!")

if __name__ == '__main__':
    create_database() 