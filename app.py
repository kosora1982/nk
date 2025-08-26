from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, g
from models.models import db, User, Category, Article, Page, Design, Navigation
import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime
import swisseph as swe
import requests
from dotenv import load_dotenv
import os
print('FLASK ENV DEBUG: CWD =', os.getcwd())
print('FLASK ENV DEBUG: .env exists =', os.path.exists('.env'))

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'astro_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///cms.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- BOOTSTRAP TEMA ---
def get_theme():
    design = Design.query.first()
    if design:
        return design.theme
    return 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css'

# --- NATALNA KARTA WIDGET (prethodni kod) ---
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
OPENROUTER_MODEL = os.environ.get('OPENROUTER_MODEL', 'mistralai/mixtral-8x7b-instruct')
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'

PLANETE = {
    'Sunce': swe.SUN,
    'Mesec': swe.MOON,
    'Merkur': swe.MERCURY,
    'Venera': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Uran': swe.URANUS,
    'Neptun': swe.NEPTUNE,
    'Pluton': swe.PLUTO,
}

def julian_day(datum, vreme):
    dt = datetime.datetime.strptime(f"{datum} {vreme}", "%Y-%m-%d %H:%M")
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)

def izracunaj_planete(jd):
    result = {}
    for ime, planet_id in PLANETE.items():
        pos, _ = swe.calc_ut(jd, planet_id)
        result[ime] = f"{pos[0]:.2f}°"
    return result

def izracunaj_asc(jd, lat, lon):
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    asc = ascmc[0]
    return f"{asc:.2f}°"

def generisi_osnovno_tumacenje(ime, planete, asc):
    """Fallback tumačenje kada API nije dostupan"""
    tumacenje = f"""
ASTROLOŠKO TUMACENJE ZA {ime.upper()}

Vaša natalna karta pokazuje sledeće pozicije planeta:

"""
    for planeta, pozicija in planete.items():
        tumacenje += f"• {planeta}: {pozicija}\n"
    
    tumacenje += f"\nAscendent: {asc}\n\n"
    
    tumacenje += """
OSNOVNO TUMACENJE:

Ova natalna karta pokazuje jedinstvenu kombinaciju planetarnih uticaja koji oblikuju vašu ličnost i životni put. Svaka planeta u vašoj karti nosi specifičnu energiju koja utiče na različite aspekte vašeg života.

SUNCE - predstavlja vašu suštinu, ego i životnu energiju
MESEC - pokazuje vašu emotivnu prirodu i instinkte
MERKUR - utiče na način komunikacije i razmišljanja
VENERA - pokazuje vaš pristup ljubavi i lepoti
MARS - predstavlja vašu volju i način delovanja
JUPITER - pokazuje vaše filozofske i religiozne sklonosti
SATURN - predstavlja vaše ograničenja i odgovornosti
URAN - pokazuje vašu originalnost i revolucionarnost
NEPTUN - utiče na vašu duhovnost i intuiciju
PLUTON - predstavlja vašu transformaciju i moć

ASCENDENT - pokazuje kako vas vide drugi i vaš pristup životu

NAPOMENA: Ovo je osnovno tumačenje. Za detaljniju analizu preporučujemo konsultaciju sa profesionalnim astrologom.
"""
    return tumacenje

def generisi_llm_tumacenje(ime, planete, asc):
    """Generiše AI tumačenje koristeći lokalni interpreter"""
    try:
        # Import lokalni AI interpreter
        from local_ai_interpreter import generate_local_ai_interpretation
        
        # Generiši tumačenje koristeći lokalni AI
        return generate_local_ai_interpretation(ime, planete, asc)
        
    except Exception as e:
        print(f"Greška u lokalnom AI tumačenju: {e}")
        # Fallback na osnovno tumačenje
        return generisi_osnovno_tumacenje(ime, planete, asc)

# --- LOGIN SISTEM ---
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = None
    if user_id:
        g.user = User.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Uspešno ste prijavljeni!')
            return redirect(url_for('admin'))
        else:
            flash('Pogrešno korisničko ime ili lozinka!')
    theme = get_theme()
    return render_template('login.html', theme=theme)

@app.route('/logout')
def logout():
    session.clear()
    flash('Uspešno ste odjavljeni!')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if User.query.first():
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Sva polja su obavezna!')
        elif User.query.filter_by(username=username).first():
            flash('Korisničko ime već postoji!')
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Uspešna registracija! Prijavite se.')
            return redirect(url_for('login'))
    theme = get_theme()
    return render_template('register.html', theme=theme)

# --- RUTE ---
@app.route('/')
def index():
    theme = get_theme()
    pages = Page.query.all()
    categories = Category.query.all()
    return render_template('index.html', theme=theme, pages=pages, categories=categories)

from flask import render_template_string

@app.route('/<slug>')
def show_page(slug):
    theme = get_theme()
    page = Page.query.filter_by(slug=slug, published=True).first_or_404()
    pages = Page.query.all()
    categories = Category.query.all()
    # Renderuj widgete
    for widget in page.widgets:
        print('WIDGET CONTENT:', widget.content)
        if "{{" in widget.content:
            widget.content = render_template_string(
                widget.content,
                dnevni_horoskop_widget=dnevni_horoskop_widget,
                nedeljni_horoskop_widget=nedeljni_horoskop_widget,
                mesecni_horoskop_widget=mesecni_horoskop_widget,
                godisnji_horoskop_widget=godisnji_horoskop_widget
            )
        # Ako nema Jinja koda, ostavi content iz baze
    return render_template('page.html', theme=theme, page=page, pages=pages, categories=categories)

@app.route('/kategorija/<int:cat_id>')
def category(cat_id):
    theme = get_theme()
    cat = Category.query.get_or_404(cat_id)
    articles = Article.query.filter_by(category_id=cat.id).all()
    pages = Page.query.all()
    categories = Category.query.all()
    return render_template('category.html', theme=theme, category=cat, articles=articles, pages=pages, categories=categories)

@app.route('/clanak/<int:art_id>')
def article(art_id):
    theme = get_theme()
    art = Article.query.get_or_404(art_id)
    pages = Page.query.all()
    categories = Category.query.all()
    return render_template('article.html', theme=theme, article=art, pages=pages, categories=categories)

# --- ADMIN (osnovni CRUD) ---
@app.route('/admin')
@login_required
def admin():
    theme = get_theme()
    return render_template('admin_dashboard.html', theme=theme)

@app.route('/admin/pages')
@login_required
def admin_pages():
    theme = get_theme()
    pages = Page.query.all()
    return render_template('admin_pages.html', theme=theme, pages=pages)

@app.route('/admin/articles')
@login_required
def admin_articles():
    theme = get_theme()
    articles = Article.query.all()
    return render_template('admin_articles.html', theme=theme, articles=articles)

@app.route('/admin/categories')
@login_required
def admin_categories():
    theme = get_theme()
    categories = Category.query.all()
    return render_template('admin_categories.html', theme=theme, categories=categories)

@app.route('/admin/users')
@login_required
def admin_users():
    theme = get_theme()
    users = User.query.all()
    return render_template('admin_users.html', theme=theme, users=users)

@app.route('/admin/page/edit/<int:pid>', methods=['GET', 'POST'])
@login_required
def edit_page(pid):
    page = Page.query.get_or_404(pid)
    if request.method == 'POST':
        page.title = request.form['title']
        page.content = request.form['content']
        db.session.commit()
        flash('Stranica ažurirana!')
        return redirect(url_for('admin'))
    theme = get_theme()
    return render_template('edit_page.html', theme=theme, page=page)

@app.route('/admin/article/edit/<int:aid>', methods=['GET', 'POST'])
@login_required
def edit_article(aid):
    art = Article.query.get_or_404(aid)
    categories = Category.query.all()
    if request.method == 'POST':
        art.title = request.form['title']
        art.content = request.form['content']
        art.category_id = int(request.form['category_id']) if request.form['category_id'] else None
        db.session.commit()
        flash('Članak ažuriran!')
        return redirect(url_for('admin'))
    theme = get_theme()
    return render_template('edit_article.html', theme=theme, article=art, categories=categories)

@app.route('/admin/design', methods=['GET', 'POST'])
@login_required
def design():
    design = Design.query.first()
    if not design:
        design = Design()
        db.session.add(design)
        db.session.commit()
    if request.method == 'POST':
        design.theme = request.form['theme']
        db.session.commit()
        flash('Dizajn ažuriran!')
        return redirect(url_for('design'))
    theme = get_theme()
    return render_template('admin_design.html', theme=theme, design=design)

@app.route('/admin/navigation')
@login_required
def admin_navigation():
    theme = get_theme()
    # Get root navigation items (parent_id is None)
    root_items = Navigation.query.filter_by(parent_id=None, is_active=True).order_by(Navigation.order).all()
    return render_template('admin_navigation.html', theme=theme, navigation_items=root_items)

@app.route('/admin/navigation/add', methods=['GET', 'POST'])
@login_required
def add_navigation():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form.get('url', '')
        slug = request.form.get('slug', '')
        parent_id = request.form.get('parent_id')
        order = request.form.get('order', 0)
        icon = request.form.get('icon', '')
        description = request.form.get('description', '')
        is_mega_menu = 'is_mega_menu' in request.form
        mega_menu_columns = request.form.get('mega_menu_columns', 1)
        css_class = request.form.get('css_class', '')
        is_external = 'is_external' in request.form
        target = request.form.get('target', '_self')
        
        nav_item = Navigation(
            title=title,
            url=url,
            slug=slug,
            parent_id=int(parent_id) if parent_id else None,
            order=int(order),
            icon=icon,
            description=description,
            is_mega_menu=is_mega_menu,
            mega_menu_columns=int(mega_menu_columns),
            css_class=css_class,
            is_external=is_external,
            target=target
        )
        
        db.session.add(nav_item)
        db.session.commit()
        flash('Navigacija uspešno dodata!')
        return redirect(url_for('admin_navigation'))
    
    theme = get_theme()
    # Get all navigation items for parent selection
    all_items = Navigation.query.filter_by(is_active=True).order_by(Navigation.order).all()
    return render_template('add_navigation.html', theme=theme, navigation_items=all_items)

@app.route('/admin/navigation/edit/<int:nav_id>', methods=['GET', 'POST'])
@login_required
def edit_navigation(nav_id):
    nav_item = Navigation.query.get_or_404(nav_id)
    
    if request.method == 'POST':
        nav_item.title = request.form['title']
        nav_item.url = request.form.get('url', '')
        nav_item.slug = request.form.get('slug', '')
        nav_item.parent_id = int(request.form['parent_id']) if request.form['parent_id'] else None
        nav_item.order = int(request.form.get('order', 0))
        nav_item.icon = request.form.get('icon', '')
        nav_item.description = request.form.get('description', '')
        nav_item.is_mega_menu = 'is_mega_menu' in request.form
        nav_item.mega_menu_columns = int(request.form.get('mega_menu_columns', 1))
        nav_item.css_class = request.form.get('css_class', '')
        nav_item.is_external = 'is_external' in request.form
        nav_item.target = request.form.get('target', '_self')
        
        db.session.commit()
        flash('Navigacija uspešno ažurirana!')
        return redirect(url_for('admin_navigation'))
    
    theme = get_theme()
    # Get all navigation items for parent selection (excluding current item and its children)
    all_items = Navigation.query.filter(
        Navigation.id != nav_id,
        Navigation.is_active == True
    ).order_by(Navigation.order).all()
    
    return render_template('edit_navigation.html', theme=theme, nav_item=nav_item, navigation_items=all_items)

@app.route('/admin/navigation/delete/<int:nav_id>', methods=['POST'])
@login_required
def delete_navigation(nav_id):
    nav_item = Navigation.query.get_or_404(nav_id)
    db.session.delete(nav_item)
    db.session.commit()
    flash('Navigacija uspešno obrisana!')
    return redirect(url_for('admin_navigation'))

@app.route('/admin/navigation/toggle/<int:nav_id>', methods=['POST'])
@login_required
def toggle_navigation(nav_id):
    nav_item = Navigation.query.get_or_404(nav_id)
    nav_item.is_active = not nav_item.is_active
    db.session.commit()
    status = 'aktivirana' if nav_item.is_active else 'deaktivirana'
    flash(f'Navigacija {status}!')
    return redirect(url_for('admin_navigation'))

# --- NATALNA KARTA WIDGET STRANICA ---
@app.route('/astrologija', methods=['GET', 'POST'])
def astrologija():
    print("FLASK ENV DEBUG: API KEY =", repr(OPENROUTER_API_KEY))
    theme = get_theme()
    ai_tumacenje = None
    planete = None
    asc = None
    pages = Page.query.all()
    categories = Category.query.all()
    if request.method == 'POST':
        ime = request.form.get('ime')
        datum = request.form.get('datum')
        vreme = request.form.get('vreme')
        lat = float(request.form.get('lat'))
        lon = float(request.form.get('lon'))
        jd = julian_day(datum, vreme)
        planete = izracunaj_planete(jd)
        asc = izracunaj_asc(jd, lat, lon)
        ai_tumacenje = generisi_llm_tumacenje(ime, planete, asc)
    return render_template('astrologija.html', theme=theme, ai_tumacenje=ai_tumacenje, planete=planete, asc=asc, pages=pages, categories=categories)

@app.route('/test-api')
def test_api():
    """Test route to verify API key is working"""
    print(f"🔍 TEST ROUTE: API Key exists: {bool(OPENROUTER_API_KEY)}")
    print(f"🔍 TEST ROUTE: API Key: {OPENROUTER_API_KEY[:20] if OPENROUTER_API_KEY else 'None'}")
    
    # Test the API directly
    if not OPENROUTER_API_KEY:
        return "❌ No API key found"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": "Hello, test message"}],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return f"✅ API working! Response: {result['choices'][0]['message']['content']}"
        else:
            return f"❌ API error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Exception: {e}"

# --- TEMPLATEI ---
# index.html, page.html, category.html, article.html, admin.html, edit_page.html, edit_article.html, design.html, astrologija.html
# Svi koriste {{ theme }} za Bootstrap i imaju navigaciju po stranicama i kategorijama

def get_navigation():
    """Get active navigation items for public site"""
    return Navigation.query.filter_by(is_active=True).order_by(Navigation.order).all()

@app.context_processor
def inject_navigation():
    """Inject navigation into all templates"""
    return dict(navigation_items=get_navigation())

# --- DNEVNI, NEDELJNI, MESECNI, GODISNJI HOROSKOP WIDGETI ---
from datetime import date, timedelta
from models.models import Horoscope, HoroscopeType

def _horoskop_widget(tip_key, title, icon, badge_fmt):
    danas = date.today()
    znaci = [
        'Ovan', 'Bik', 'Blizanci', 'Rak', 'Lav', 'Devica',
        'Vaga', 'Škorpija', 'Strelac', 'Jarac', 'Vodolija', 'Ribe'
    ]
    # Odredi datum za prikaz
    if tip_key == 'dnevni':
        datum = danas
    elif tip_key == 'nedeljni':
        datum = danas - timedelta(days=danas.weekday())
    elif tip_key == 'mesecni':
        datum = danas.replace(day=1)
    elif tip_key == 'godisnji':
        datum = danas.replace(month=1, day=1)
    else:
        datum = danas
    # Učitaj horoskope iz baze
    tip = HoroscopeType.query.filter_by(name=tip_key).first()
    horoskopi = {h.sign: h.content for h in Horoscope.query.filter_by(type_id=tip.id, date=datum)} if tip else {}
    lines = []
    for znak in znaci:
        opis = horoskopi.get(znak, "Nema podataka za ovaj znak.")
        lines.append(f"{znak}: {opis}")
    return f"{title} ({badge_fmt})\n" + "\n".join(lines)

def dnevni_horoskop_widget():
    danas = date.today()
    return _horoskop_widget('dnevni', 'Dnevni horoskop', 'bi bi-calendar2-day', danas.strftime('%d.%m.%Y.'))

def nedeljni_horoskop_widget():
    danas = date.today()
    monday = danas - timedelta(days=danas.weekday())
    return _horoskop_widget('nedeljni', 'Nedeljni horoskop', 'bi bi-calendar2-week', f"{monday.strftime('%d.%m.%Y.')}")

def mesecni_horoskop_widget():
    danas = date.today()
    first = danas.replace(day=1)
    return _horoskop_widget('mesecni', 'Mesečni horoskop', 'bi bi-calendar2-month', first.strftime('%m.%Y.'))

def godisnji_horoskop_widget():
    danas = date.today()
    first = danas.replace(month=1, day=1)
    return _horoskop_widget('godisnji', 'Godišnji horoskop', 'bi bi-calendar2-range', str(first.year))

app.jinja_env.globals['dnevni_horoskop_widget'] = dnevni_horoskop_widget
app.jinja_env.globals['nedeljni_horoskop_widget'] = nedeljni_horoskop_widget
app.jinja_env.globals['mesecni_horoskop_widget'] = mesecni_horoskop_widget
app.jinja_env.globals['godisnji_horoskop_widget'] = godisnji_horoskop_widget

def seed_db():
    from models.models import Page
    pages = [
        {"slug": "pocetna", "title": "Početna stranica", "content": "<h2>Dobrodošli!</h2>"},
        {"slug": "o-meni", "title": "O meni", "content": "<h2>O meni</h2>"},
        {"slug": "usluge", "title": "Usluge/Konsultacije", "content": "<h2>Usluge i konsultacije</h2>"},
        {"slug": "cenovnik", "title": "Cenovnik", "content": "<h2>Cenovnik</h2>"},
        {"slug": "zakazivanje", "title": "Zakazivanje konsultacija", "content": "<h2>Zakazivanje</h2>"},
        {"slug": "faq", "title": "Najčešća pitanja (FAQ)", "content": "<h2>Najčešća pitanja</h2>"},
        {"slug": "svedocanstva", "title": "Svedočanstva klijenata", "content": "<h2>Svedočanstva klijenata</h2>"},
        {"slug": "blog", "title": "Blog", "content": "<h2>Blog</h2>"},
        {"slug": "kontakt", "title": "Kontakt", "content": "<h2>Kontakt</h2>"},
        {"slug": "pravila-privatnosti", "title": "Pravila privatnosti i Uslovi korišćenja", "content": "<h2>Pravila privatnosti i Uslovi korišćenja</h2>"},
    ]
    for p in pages:
        if not Page.query.filter_by(slug=p["slug"]).first():
            page = Page(slug=p["slug"], title=p["title"], content=p["content"])
            db.session.add(page)
    db.session.commit()
    print("Seeder: Stranice su ubačene u bazu.")

def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    create_tables()
    swe.set_ephe_path('.')
    app.run(debug=True)
