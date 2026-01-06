# Contributing / Setup Guide

This document explains how to get the project running locally from a fresh machine. It includes exact commands for creating a virtual environment named `myvenv`, activating it, installing dependencies, building Tailwind CSS, and starting both frontend and backend for development.

> Note: you named your venv `myvenv`. If contributors choose a different name, replace `myvenv` in the commands below accordingly.

---

## Prerequisites

- Python 3.10+ (make sure `python` is in PATH)
- Node.js + npm (Node 16+ recommended)
- Git

---

## Step-by-step (Windows - PowerShell)

1. Clone the repo and change directory:

```powershell
git clone <repo-url>
cd PG-Manager
```

2. Create a Python virtual environment named `myvenv`:

```powershell
python -m venv myvenv
```

3. Activate the virtual environment (PowerShell):

```powershell
# If script execution is blocked, allow it for the session:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Activate
.\myvenv\Scripts\Activate.ps1
```

4. Upgrade pip and install Python deps:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

5. Install Node dependencies (Tailwind CLI, concurrently, ...):

```powershell
npm install
```

6. Build Tailwind CSS once (creates compiled CSS):

```powershell
npm run build:css
```

7. Development (one terminal):

```powershell
# Make sure myvenv is activated (so `python` is the venv's python)
npm run dev
```

This runs both the Tailwind watcher and the Flask server concurrently. Open `http://127.0.0.1:5000/` to view the app.

If you prefer separate terminals:
- Terminal A: `npm run watch:css`
- Terminal B: `python run.py` (or `.\


#for psycopg2'
'''
pip install psycopg2
'''
 









































































Tell me which of those you'd like next.- Add a sample GitHub Actions workflow that runs `npm run build:css` and `python -m pip install -r requirements.txt` and tests the Flask app.- Make `npm run dev` work without activating the venv (auto-detect or explicit path)If you'd like, I can:---- If you add files that are build artifacts, consider adding them to `.gitignore`.- Compiled Tailwind CSS (`app/static/css/tailwind.css`) is ignored (it's generated). Ensure `npm run build:css` or `npm run dev` runs in your CI or deploy pipeline.- Do **not** commit secrets or `.env` to the repo. `.env` is listed in `.gitignore`.## Other notes---If you want a single `npm run dev` command to work without activation, tell me and I can update the `watch:flask` script to reference the project venv automatically (it can look for `myvenv` or `.venv` / `venv`).```.\myvenv\Scripts\python.exe run.py.\myvenv\Scripts\python.exe -m pip install -r requirements.txt```powershellYou can call the venv python directly without activation. Example (Windows):## If you don't want to activate the venv---```# python run.py# npm run watch:css# or separately:npm run dev   # runs both watch:css and the flask server```bash5. Run the Flask app (while venv is active):```npm run watch:css   # or run npm run dev after activationnpm run build:css   # one-timenpm install```bash4. Install Node deps & build/watch Tailwind:```python -m pip install -r requirements.txtpython -m pip install --upgrade pip```bash3. Upgrade pip & install Python deps:```source myvenv/bin/activatepython3 -m venv myvenv```bash2. Create & activate venv (named `myvenv`):```cd PG-Managergit clone <repo-url>```bash1. Clone & cd:## Step-by-step (macOS / Linux - bash)---```deactivate```powershell8. To stop development, use Ctrl+C in the terminal(s). To deactivate the venv:uncscripts\run.ps1` if you use the helper script)