# PG-Manager

This repository now includes a minimal Flask application skeleton and helper scripts to get you started locally.

## Quick Start (Windows)

1. Create virtual environment and install dependencies:

   ```powershell
   .\scripts\setup.ps1
   ```

2. Copy `.env.example` to `.env` if you need to override defaults.

3. Run the app:

   ```powershell
   .\scripts\run.ps1
   ```

4. Open http://127.0.0.1:5000/ to see the test JSON response.

## VS Code

- Use the **Run Flask** task (Tasks > Run Task > Run Flask), or
- Use the debug configuration **Python: Flask (run.py)** in the Run and Debug panel.

## Tailwind CSS

This project uses Tailwind CLI for the frontend. To build Tailwind CSS:

```powershell
npm install
npm run build:css   # one-time build
npm run watch:css   # development watch mode
```

You can also run backend + frontend with one command:

```powershell
# Activate your Python venv first so `python` points to the venv interpreter
.\venv\Scripts\Activate.ps1   # or .\.venv\Scripts\Activate.ps1
npm run dev
```

The compiled CSS is written to `app/static/css/tailwind.css` and is included by `app/templates/index.html`.

For more details, see `FLASK_SETUP.md`.
