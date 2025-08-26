from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Inicijalizacija baze

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)
    deleted_by = db.Column(db.Integer, nullable=True)

    def soft_delete(self, user_id=None):
        self.deleted_at = datetime.utcnow()
        self.deleted_by = user_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    articles = db.relationship('Article', backref='category', lazy=True)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

# Pomoćna tabela za many-to-many vezu između stranica i widgeta
page_widgets = db.Table('page_widgets',
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True),
    db.Column('widget_id', db.Integer, db.ForeignKey('widget.id'), primary_key=True)
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published = db.Column(db.Boolean, default=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=True)
    children = db.relationship('Page', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    widgets = db.relationship('Widget', secondary=page_widgets, back_populates='pages')

class Design(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(200), default='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css')

class Widget(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    content = db.Column(db.Text, nullable=True)
    pages = db.relationship('Page', secondary='page_widgets', back_populates='widgets')

class Navigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200))
    slug = db.Column(db.String(100), unique=True)
    icon = db.Column(db.String(50))  # FontAwesome icon class
    order = db.Column(db.Integer, default=0)  # For menu ordering
    is_active = db.Column(db.Boolean, default=True)
    is_external = db.Column(db.Boolean, default=False)  # External links
    target = db.Column(db.String(20), default='_self')  # _blank, _self, etc.
    
    # Parent-child relationship for mega menu
    parent_id = db.Column(db.Integer, db.ForeignKey('navigation.id'))
    children = db.relationship('Navigation', 
                             backref=db.backref('parent', remote_side=[id]),
                             lazy='dynamic',
                             cascade='all, delete-orphan')
    
    # Additional fields for mega menu
    description = db.Column(db.Text)  # Description for mega menu items
    image_url = db.Column(db.String(200))  # Image for mega menu
    css_class = db.Column(db.String(100))  # Custom CSS classes
    is_mega_menu = db.Column(db.Boolean, default=False)  # Is this a mega menu item
    mega_menu_columns = db.Column(db.Integer, default=1)  # Number of columns in mega menu
    
    # SEO fields
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Navigation {self.title}>'
    
    def get_children(self):
        """Get all active children ordered by order field"""
        return self.children.filter_by(is_active=True).order_by(Navigation.order).all()
    
    def get_siblings(self):
        """Get all siblings (items with same parent)"""
        if self.parent_id:
            return Navigation.query.filter_by(parent_id=self.parent_id, is_active=True).order_by(Navigation.order).all()
        else:
            return Navigation.query.filter_by(parent_id=None, is_active=True).order_by(Navigation.order).all()
    
    def get_breadcrumbs(self):
        """Get breadcrumb trail from root to current item"""
        breadcrumbs = []
        current = self
        while current:
            breadcrumbs.insert(0, current)
            current = current.parent
        return breadcrumbs
    
    def has_children(self):
        """Check if item has active children"""
        return self.children.filter_by(is_active=True).count() > 0
    
    def is_root(self):
        """Check if item is a root level item"""
        return self.parent_id is None
    
    def get_level(self):
        """Get the depth level of this item (0 = root, 1 = first level, etc.)"""
        level = 0
        current = self
        while current.parent:
            level += 1
            current = current.parent
        return level
    
    def get_all_children_recursive(self):
        """Get all children recursively (for mega menu)"""
        children = []
        for child in self.get_children():
            children.append(child)
            children.extend(child.get_all_children_recursive())
        return children

# --- HOROSCOPE TYPE LOOKUP ---
class HoroscopeType(db.Model):
    __tablename__ = 'horoscope_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # npr. 'dnevni', 'nedeljni', ...
    description = db.Column(db.String(200))
    horoscopes = db.relationship('Horoscope', backref='type', lazy=True)

# --- HOROSCOPE ---
class Horoscope(db.Model):
    __tablename__ = 'horoscope'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('horoscope_type.id'), nullable=False)
    sign = db.Column(db.String(20), nullable=False)  # npr. 'ovan', 'bik', ...
    date = db.Column(db.Date, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
