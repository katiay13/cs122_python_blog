# The Pythonistas
An IndieWeb-inspired personal blog built with Python.

** Tech Stack:** Flask, Jinja2, SQLAlchemy, SQLite

---

## Setup

### 1. Clone the repo

```bash
git clone <repo-url>
cd <repo-folder-name>
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the app

```bash
flask --app app run --debug
```

Then open []() in your browser.

- '--debug' restarts the server automatically when you save changes and shows error pages
- Stop the server with **Ctrl + C**