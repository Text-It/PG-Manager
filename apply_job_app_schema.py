import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
}

def apply_schema():
    print("🚀 applying 09_job_applications.sql...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        schema_path = os.path.join("database_schemas", "09_job_applications.sql")
        with open(schema_path, 'r') as f:
            sql = f.read()
            
        cur.execute(sql)
        conn.commit()
        print("✅ Successfully applied job applications schema.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error applying schema: {e}")

if __name__ == "__main__":
    apply_schema()
