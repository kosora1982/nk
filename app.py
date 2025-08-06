from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, g
from models.models import db, User, Category, Article, Page, Design
import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime
import swisseph as swe
import requests

app = Flask(__name__)
app.secret_key = 'astro_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- BOOTSTRAP TEMA ---
def get_theme():
    design = Design.query.first()
    if design:
        return design.theme
    return 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css'

# --- NATALNA KARTA WIDGET (prethodni kod) ---
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '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')
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

def generisi_llm_tumacenje(ime, planete, asc):
    prompt = f"""
Napravi najdetaljnije moguće astrološko tumačenje natalne karte za osobu po imenu {ime}. \nPlanete su na sledećim pozicijama:\n"""
    for planeta, pozicija in planete.items():
        prompt += f"{planeta}: {pozicija}\n"
    prompt += f"Ascendent: {asc}\n"
    prompt += "\nTumačenje napiši na srpskom jeziku, u stilu profesionalnog astrologa, sa posebnim osvrtom na ličnost, potencijale, izazove, karmu, odnose, zdravlje, karijeru i duhovnost. Koristi minimum 800 reči."
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
        "temperature": 0.8
    }
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=180)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            return f"[LLM greška] Status: {response.status_code} - {response.text}"
    except Exception as e:
        return f"[LLM greška] {e}"

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

@app.route('/stranica/<slug>')
def page(slug):
    theme = get_theme()
    page = Page.query.filter_by(slug=slug).first_or_404()
    pages = Page.query.all()
    categories = Category.query.all()
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

# --- NATALNA KARTA WIDGET STRANICA ---
@app.route('/astrologija', methods=['GET', 'POST'])
def astrologija():
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

# --- TEMPLATEI ---
# index.html, page.html, category.html, article.html, admin.html, edit_page.html, edit_article.html, design.html, astrologija.html
# Svi koriste {{ theme }} za Bootstrap i imaju navigaciju po stranicama i kategorijama

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_db()
    swe.set_ephe_path('.')
    app.run(debug=True)
