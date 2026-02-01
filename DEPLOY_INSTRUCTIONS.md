# 🚀 Deployment Instructions for Vercel

Your app is ready for Vercel, BUT you need a **Cloud Database**. Vercel only hosts the code; it cannot see your computer's local database.

## Step 1: Get a Free Cloud Database
1.  Go to **Neon.tech** or **Supabase.com** (both have generous free tiers).
2.  Create a new Postgres Project.
3.  **Copy the Connection Details** (Host, Database Name, User, Password, Port).

## Step 2: Set up Schema (The Tables)
The cloud database is empty. You need to create the tables there.
1.  On your **Local Computer**, edit your `.env` file to point to the **Cloud Database** temporarily:
    ```
    DB_HOST=ep-shiny-....aws.neon.tech
    DB_USER=neondb_owner
    DB_PASSWORD=...
    ...
    ```
2.  Run the setup script locally:
    ```bash
    python setup_db.py
    ```
    (This will create all tables `users`, `tenants`, `password_resets`, etc. on the Cloud DB).

## Step 3: Deploy to Vercel
1.  Push your code to **GitHub**.
2.  Go to **Vercel.com** -> "Add New..." -> "Project" -> Select your repo.
3.  **Environment Variables**: In the Vercel config screen, add these variables (copy from your Cloud DB):
    *   `DB_HOST`
    *   `DB_NAME`
    *   `DB_USER`
    *   `DB_PASSWORD`
    *   `DB_PORT` (usually 5432)
    *   `SECRET_KEY` (make up a random string)
    *   `MAIL_USERNAME` (your gmail)
    *   `MAIL_PASSWORD` (your app password)
4.  Click **Deploy**! 🚀

## Troubleshooting
*   **500 Error?**: Check "Logs" in Vercel. Usually means DB connection failed.
*   **Static Files**: Vercel handles `static/` folder automatically.

---

# 🌍 Option 2: Deploy to Netlify

I have also configured the app for Netlify!

1.  Push your code to **GitHub**.
2.  Go to **Netlify.com** -> "Add new site" -> "Import from Git".
3.  **Build Settings**:
    *   **Build command**: `npm run build:css`
    *   **Publish directory**: `app/static`
    *   **Functions directory**: `netlify/functions` (Should be auto-detected from netlify.toml)
4.  **Environment Variables**:
    *   Click **"Advanced"** or go to "Site Settings" -> "Environment Variables".
    *   Add the **Exact Same Variables** as above (`DB_HOST`, `DB_USER`, `MAIL_PASSWORD`, etc.).
5.  **Deploy Site**.

Netlify will use the `netlify/functions/api.py` file to run your Flask app as a Serverless Function.
