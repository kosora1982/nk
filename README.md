# Astrologija CMS

Modern CMS system with astrological features including natal chart calculations and AI-powered interpretations.

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment Variables
```bash
python setup_env.py
```

### 3. Run the Application
```bash
python app.py
```

## 🔧 Environment Configuration

### OpenRouter API Setup (Optional)

For AI-powered astrological interpretations, you'll need an OpenRouter API key:

1. **Get API Key**: 
   - Go to [OpenRouter](https://openrouter.ai/)
   - Sign up for an account
   - Get your API key from the dashboard

2. **Configure API Key**:
   - Edit `.env` file
   - Replace `your-valid-api-key` with your actual API key
   - Example: `OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **Alternative Setup**:
   ```bash
   python setup_env.py
   ```
   This will guide you through the setup process interactively.

## 📁 Project Structure

```
nk/
├── app.py                 # Main Flask application
├── models/               # Database models
├── templates/            # HTML templates
├── static/              # Static files (CSS, JS, images)
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── setup_env.py         # Environment setup script
```

## 🌟 Features

### Admin Panel
- ✅ Bootstrap DataTables with pagination
- ✅ Self-hosted TinyMCE editor
- ✅ User management
- ✅ Content management (pages, articles, categories)
- ✅ Design customization

### Astrological Features
- ✅ Natal chart calculations
- ✅ Planet positions
- ✅ Ascendant calculations
- ✅ AI-powered interpretations (with OpenRouter API)
- ✅ Fallback interpretations (when API unavailable)

### Content Management
- ✅ Rich text editing with TinyMCE
- ✅ Responsive design
- ✅ SEO-friendly URLs
- ✅ Category management

## 🔐 Security

- Environment variables for sensitive data
- SQLAlchemy for database security
- Session-based authentication
- CSRF protection

## 🛠️ Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Database Setup
The database will be created automatically on first run.

### Adding New Features
1. Create models in `models/models.py`
2. Add routes in `app.py`
3. Create templates in `templates/`
4. Update navigation as needed

## 📝 Notes

- The application works without an API key (uses fallback interpretations)
- All astrological calculations are done locally using Swiss Ephemeris
- TinyMCE editor is self-hosted (no external dependencies)
- Bootstrap DataTables provide professional admin interface

## 🆘 Troubleshooting

### 401 API Error
If you see "User not found" errors:
1. Check your OpenRouter API key in `.env`
2. Ensure the API key is valid and has credits
3. The application will work with fallback interpretations

### Database Issues
```bash
# Reset database
rm cms.db
python app.py
```

### Environment Issues
```bash
# Reinstall dependencies
pip install -r requirements.txt
python setup_env.py
``` 