# PG Manager - Setup Guide 🚀

## 1. Prerequisites
*   **Python 3.8+**
*   **Node.js & npm** (for Tailwind CSS)
*   **PostgreSQL** (Database)

## 2. Environment Setup

### A. Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### B. Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node dependencies (Tailwind)
npm install
```

### C. Environment Variables
1.  Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```
2.  **Edit `.env`** and fill in your PostgreSQL credentials:
    ```ini
    DB_NAME=pgmanagement
    DB_USER=postgres
    DB_PASSWORD=your_password
    DB_HOST=localhost
    SECRET_KEY=your_secret_key
    ```

## 3. Database Setup 🗄️

### A. Create Database
Ensure the database exists in Postgres before running scripts.
```sql
CREATE DATABASE pgmanagement;
```

### B. Initialize Tables
Run the included python script to create `users`, `owners`, and `tenants` tables.
```bash
python app/database/init_db.py
```
*This script is idempotent (safe to run multiple times).*

## 4. Running the App code ▶️

### Development Mode (with Hot Reload)
Run both Flask and Tailwind watcher in parallel:
```bash
npm run dev
```

### Manual Run
```bash
# Terminal 1: Tailwind Watcher
npx tailwindcss -i ./src/styles/input.css -o ./app/static/css/custom.css --watch

# Terminal 2: Flask App
python run.py
```

## 5. Project Structure
*   `app/` - Main application code
*   `app/database/` - DB Helper (`database.py`) and Init Script (`init_db.py`)
*   `app/templates/` - HTML files (Owner & Tenant folders)
*   `app/static/` - CSS/JS assets
