import os
import secrets
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432"))
        )
        return conn
    except Exception as e:
        print(f"DB Connection Error: {e}")
        return None

def migrate():
    conn = get_db_connection()
    if not conn: return

    cur = conn.cursor()
    try:
        print("Starting Migration...")

        # 1. Get all Owners
        cur.execute("SELECT id, full_name FROM owners")
        owners = cur.fetchall()

        for owner in owners:
            owner_id = owner[0]
            owner_name = owner[1]
            print(f"Processing Owner: {owner_name}")

            # 2. Ensure Owner has a default Property
            cur.execute("SELECT id FROM properties WHERE owner_id = %s", (owner_id,))
            prop = cur.fetchone()
            
            if not prop:
                print("  -> Creating default property")
                cur.execute("""
                    INSERT INTO properties (owner_id, name, address) 
                    VALUES (%s, 'My PG', 'Main Address') 
                    RETURNING id
                """, (owner_id,))
                property_id = cur.fetchone()[0]
            else:
                property_id = prop[0]

            # 3. Get all Tenants for this owner who have a room_number set
            cur.execute("""
                SELECT id, room_number, monthly_rent 
                FROM tenants 
                WHERE owner_id = %s AND room_number IS NOT NULL AND room_id IS NULL
            """, (owner_id,))
            
            tenants = cur.fetchall()
            
            for tenant in tenants:
                t_id = tenant[0]
                room_no = tenant[1]
                rent = tenant[2] or 0
                
                # 4. Check if Room exists, else create it
                cur.execute("SELECT id FROM rooms WHERE property_id = %s AND room_number = %s", (property_id, room_no))
                room = cur.fetchone()
                
                if not room:
                    print(f"  -> Creating Room {room_no}")
                    cur.execute("""
                        INSERT INTO rooms (property_id, room_number, capacity, rent_amount)
                        VALUES (%s, %s, 3, %s)
                        RETURNING id
                    """, (property_id, room_no, rent))
                    room_id = cur.fetchone()[0]
                else:
                    room_id = room[0]
                
                # 5. Link Tenant to Room
                cur.execute("UPDATE tenants SET room_id = %s WHERE id = %s", (room_id, t_id))
                print(f"  -> Linked Tenant {t_id} to Room {room_no}")

        conn.commit()
        print("Migration Completed Successfully! 🚀")

    except Exception as e:
        conn.rollback()
        print(f"Migration Failed: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    migrate()
