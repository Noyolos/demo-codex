# demo-codex

This project provides a minimal Flask web application with a homepage and login page. It demonstrates a typical folder structure that separates application code, HTML templates, and static assets.

## Getting Started

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   flask --app app run --debug
   ```

3. Open <http://127.0.0.1:5000> in your browser to view the homepage.

### Demo Credentials
Use the following credentials on the login page:
- **Username:** `admin`
- **Password:** `password123`

## Project Structure
```
app/
├── __init__.py        # Flask application and routes
├── static/
│   └── css/
│       └── style.css  # Global styles for the app
└── templates/
    ├── base.html      # Shared layout
    ├── home.html      # Homepage
    └── login.html     # Login form
```
