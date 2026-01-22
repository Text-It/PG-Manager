import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def reset_payment():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            port=os.environ.get('DB_PORT')
        )
        cur = conn.cursor()
        
        # Hardcoding the test user seen in logs
        target_email = 'man@gmail.com' 
        current_month = datetime.now().strftime('%Y-%m')
        
        # Get Tenant ID
        cur.execute("SELECT id FROM tenants WHERE email = %s", (target_email,))
        res = cur.fetchone()
        
        if not res:
            print(f"Tenant {target_email} not found.")
            return

        tenant_id = res[0]

        # Delete payments for this month
        cur.execute("DELETE FROM payments WHERE tenant_id = %s AND payment_month = %s", (tenant_id, current_month))
        deleted_count = cur.rowcount
        conn.commit()
        
        if deleted_count > 0:
            print(f"Successfully deleted {deleted_count} payment record(s) for {target_email}.")
            print("Rent status should now be 'UNPAID' (Due).")
        else:
            print("No payment records found to delete for this month.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    reset_payment()
