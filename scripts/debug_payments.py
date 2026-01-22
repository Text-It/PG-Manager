import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def debug_payments():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            port=os.environ.get('DB_PORT')
        )
        cur = conn.cursor()
        
        current_month = datetime.now().strftime('%Y-%m')
        print(f"--- Debugging Payments for {current_month} ---")
        
        # Get all tenants
        cur.execute("""
            SELECT t.id, t.full_name, t.email, p.status, p.amount, p.id
            FROM tenants t
            LEFT JOIN payments p ON t.id = p.tenant_id AND p.payment_month = %s
        """, (current_month,))
        
        rows = cur.fetchall()
        
        if not rows:
            print("No tenants found.")
        else:
            print(f"{'Name':<20} | {'Email':<30} | {'Status':<15} | {'Amount':<10}")
            print("-" * 85)
            for row in rows:
                status = row[3] if row[3] else "NULL (Unpaid)"
                amount = str(row[4]) if row[4] else "-"
                print(f"{row[1]:<20} | {row[2]:<30} | {status:<15} | {amount:<10}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    debug_payments()
