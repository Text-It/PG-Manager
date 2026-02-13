
import os
import psycopg2
import uuid
import random
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from faker import Faker

# Load env variables
load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
}

# Constants
TEST_EMAIL = "testowner@example.com"
TEST_PASSWORD = "password123"

fake = Faker('en_IN') # Use Indian locale for names/addresses

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        return None

def demo_seed():
    conn = get_db_connection()
    if not conn: return
    cur = conn.cursor()
    print("🚀 Starting MASSIVE Demo Database Seeding...")

    try:
        # 1. Clean Slate
        print("🧹 Cleaning existing data...")
        tables = [
            "activity_logs", "notices", "complaints", "expenses", 
            "payments", "tenants", "rooms", "properties", 
            "owners", "users", "otp_verifications"
        ]
        cur.execute(f"TRUNCATE TABLE {', '.join(tables)} RESTART IDENTITY CASCADE;")
        
        # 2. Create Base User & Owner
        print("👤 Creating Owner Account...")
        user_id = str(uuid.uuid4())
        owner_id = str(uuid.uuid4())
        
        cur.execute("""
            INSERT INTO users (id, email, password_hash, role)
            VALUES (%s, %s, %s, 'OWNER')
        """, (user_id, TEST_EMAIL, generate_password_hash(TEST_PASSWORD)))
        
        cur.execute("""
            INSERT INTO owners (id, user_id, full_name, phone_number, business_name, upi_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (owner_id, user_id, "Demo Owner", "9876543210", "Sunshine Hospitality Group", "demo@upi"))
        
        # 3. Create Diverse Properties
        print("🏢 Building Properties...")
        properties = [
            {"name": "Sunshine Residency", "address": "Andheri West, Mumbai", "type": "PG"},
            {"name": "Urban Hive Co-Living", "address": "Koramangala, Bangalore", "type": "COLIVING"},
            {"name": "Green Valley Student Housing", "address": "Pune University Road", "type": "HOSTEL"}
        ]
        
        prop_ids = []
        for p in properties:
            p_id = str(uuid.uuid4())
            cur.execute("INSERT INTO properties (id, owner_id, name, address) VALUES (%s, %s, %s, %s)", 
                        (p_id, owner_id, p['name'], p['address']))
            prop_ids.append(p_id)
            
        # 4. Create Rooms & Expenses
        print("🛏️  Constructing Rooms & Adding Expenses...")
        room_ids = []
        
        for p_idx, p_id in enumerate(prop_ids):
            # Create Floors 1-4
            for floor in range(1, 5):
                for r in range(1, 6): # 5 rooms per floor
                    r_id = str(uuid.uuid4())
                    room_num = f"{floor}{r:02d}"
                    capacity = random.choice([1, 2, 3, 4])
                    rent = random.choice([6000, 8000, 10000, 15000, 20000])
                    
                    cur.execute("""
                        INSERT INTO rooms (id, property_id, room_number, floor_number, capacity, rent_amount)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (r_id, p_id, room_num, floor, capacity, rent))
                    
                    room_ids.append({'id': r_id, 'num': room_num, 'rent': rent, 'cap': capacity, 'pid': p_id})
            
            # Add Expenses for each property
            for _ in range(random.randint(5, 15)):
                exp_date = fake.date_between(start_date='-60d', end_date='today')
                amount = random.randint(500, 5000)
                category = random.choice(['Maintenance', 'Utility', 'Salary', 'Cleaning', 'Internet'])
                desc = f"{category} Bill - {fake.month_name()}"
                
                cur.execute("""
                    INSERT INTO expenses (owner_id, amount, category, description, expense_date, expense_month)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (owner_id, amount, category, desc, exp_date, exp_date.strftime('%Y-%m')))

        # 5. Create Tenants
        print("👥  Moving in Tenants (Active, Past, Future)...")
        tenant_ids = []
        
        # Scenarios:
        # - Good Payer (Active)
        # - Late Payer (Active)
        # - Notice Period (Active -> Leaving)
        # - Past Tenant (Moved Out)
        # - Future Booking (Not moved in yet) - Requires tricky logic with lease_start > now, simplified to mostly Active/Past for demo visual impact
        
        for i in range(120): # 120 Tenants
            room = random.choice(room_ids)
            t_id = str(uuid.uuid4())
            
            profile = fake.simple_profile()
            full_name = profile['name']
            email = profile['mail']
            phone = fake.phone_number()
            
            # Determine Status & Lease details
            rand_val = random.random()
            if rand_val < 0.1:
                status = 'DRAFT' # Future/Incomplete
                start_date = datetime.now() + timedelta(days=random.randint(1, 10))
            elif rand_val < 0.2:
                status = 'NOTICE' # Leaving soon
                start_date = datetime.now() - timedelta(days=random.randint(60, 300))
            elif rand_val < 0.3:
                # Past tenant (conceptually), but schema might just treat them as inactive or removed? 
                # Let's keep them 'ACTIVE' but old move-in for history, or maybe just skip 'Past' status if not in Enum
                status = 'ACTIVE' 
                start_date = datetime.now() - timedelta(days=random.randint(200, 500))
            else:
                status = 'ACTIVE'
                start_date = datetime.now() - timedelta(days=random.randint(30, 180))
            
            # Security Deposit
            deposit = room['rent'] * random.choice([1, 2, 3])
            
            cur.execute("""
                INSERT INTO tenants (id, owner_id, full_name, email, phone_number, room_id, room_number, monthly_rent, security_deposit, onboarding_status, lease_start)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (t_id, owner_id, full_name, email, phone, room['id'], room['num'], room['rent'], deposit, status, start_date))

            tenant_ids.append({'id': t_id, 'name': full_name, 'rent': room['rent'], 'start': start_date, 'status': status, 'deposit': deposit})
            
            # Log Creation
            log_meta = {'room': room['num'], 'metadata': 'blue'}
            cur.execute("""
                INSERT INTO activity_logs (owner_id, event_type, description, metadata, created_at)
                VALUES (%s, 'TENANT_ADD', %s, %s, %s)
            """, (owner_id, f"Added {full_name} to Room {room['num']}", json.dumps(log_meta), start_date))


        # 6. Generate Payments & Financial History
        print("💰  Generating Financial Transactions...")
        
        for t in tenant_ids:
            if t['status'] == 'DRAFT': continue 
            
            # Pay Security Deposit (mostly)
            if random.random() > 0.1:
                cur.execute("""
                    INSERT INTO payments (tenant_id, amount, payment_date, payment_month, status, payment_mode, remarks)
                    VALUES (%s, %s, %s, %s, 'COMPLETED', %s, 'Security Deposit')
                """, (t['id'], t['deposit'], t['start'], t['start'].strftime('%Y-%m'), 'UPI'))

            # Rent Payments
            current_date = t['start']
            last_date = datetime.now()
            
            while current_date < last_date:
                # Decide if they pay this month
                # 80% pay on time, 10% late, 5% partial, 5% missed
                month_str = current_date.strftime('%Y-%m')
                due_amount = t['rent']
                
                pay_roll = random.random()
                
                if pay_roll < 0.80: # On Time / Normal
                    pay_date = current_date + timedelta(days=random.randint(1, 5))
                    if pay_date > last_date: break
                    
                    cur.execute("""
                        INSERT INTO payments (tenant_id, amount, payment_date, payment_month, status, payment_mode, remarks)
                        VALUES (%s, %s, %s, %s, 'COMPLETED', %s, 'Monthly Rent')
                    """, (t['id'], due_amount, pay_date, month_str, random.choice(['UPI', 'CASH', 'BANK_TRANSFER'])))
                    
                    # Log
                    meta = {'amount': due_amount, 'metadata': 'green'}
                    cur.execute("INSERT INTO activity_logs (owner_id, event_type, description, metadata, created_at) VALUES (%s, 'PAYMENT', %s, %s, %s)", 
                                (owner_id, f"Rent received from {t['name']}", json.dumps(meta), pay_date))

                elif pay_roll < 0.90: # Late Payment
                    pay_date = current_date + timedelta(days=random.randint(10, 20))
                    if pay_date > last_date: break
                     
                    cur.execute("""
                        INSERT INTO payments (tenant_id, amount, payment_date, payment_month, status, payment_mode, remarks)
                        VALUES (%s, %s, %s, %s, 'COMPLETED', %s, 'Late Rent Payment')
                    """, (t['id'], due_amount, pay_date, month_str, random.choice(['UPI', 'CASH'])))

                elif pay_roll < 0.95: # Partial Payment
                    pay_date = current_date + timedelta(days=random.randint(1, 10))
                    partial_amt = int(due_amount * random.choice([0.5, 0.7]))
                    
                    if pay_date < last_date:
                        cur.execute("""
                            INSERT INTO payments (tenant_id, amount, payment_date, payment_month, status, payment_mode, remarks)
                            VALUES (%s, %s, %s, %s, 'COMPLETED', %s, 'Partial Rent')
                        """, (t['id'], partial_amt, pay_date, month_str, 'CASH'))
                
                else:
                    # Missed Payment (No Record)
                    pass

                # Move to next month
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1, day=1)

        # 7. Generate Notices & Complaints
        print("📢  Posting Notices & Complaints...")
        
        # Notices
        notices = [
            ("Pool Maintenance", "Swimming pool will be closed for cleaning this weekend."),
            ("Diwali Celebration", "Join us for Diwali sweets distribution in the lobby!"),
            ("Rent Reminder", "Please pay rent by 5th of every month to avoid late fees."),
            ("Wifi Upgrade", "We are upgrading to 1Gbps fiber this Tuesday.")
        ]
        
        for n_title, n_desc in notices:
            n_date = fake.date_this_month()
            cur.execute("""
                INSERT INTO notices (owner_id, title, description, created_at)
                VALUES (%s, %s, %s, %s)
            """, (owner_id, n_title, n_desc, n_date))

        # Complaints
        complaint_types = ["Plumbing", "Electrical", "Internet", "Furniture", "Cleaning"]
        
        for _ in range(40):
            t = random.choice(tenant_ids)
            if t['status'] == 'DRAFT': continue
            
            c_type = random.choice(complaint_types)
            c_title = f"{c_type} Issue"
            c_desc = f"Having trouble with {c_type.lower()} in the room."
            c_status = random.choice(['PENDING', 'IN_PROGRESS', 'RESOLVED'])
            c_prio = random.choice(['LOW', 'MEDIUM', 'HIGH'])
            c_date = fake.date_between(start_date='-60d', end_date='today')
            
            cur.execute("""
                INSERT INTO complaints (tenant_id, owner_id, title, description, status, priority, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (t['id'], owner_id, c_title, c_desc, c_status, c_prio, c_date))
            
            # Log
            meta = {'status': c_status, 'metadata': 'red'}
            cur.execute("INSERT INTO activity_logs (owner_id, event_type, description, metadata, created_at) VALUES (%s, 'COMPLAINT', %s, %s, %s)", 
                        (owner_id, f"Complaint: {c_title} ({t['name']})", json.dumps(meta), c_date))



        conn.commit()

        # 8. Create a Demo Tenant Account (Login Access)
        print("👤 Creating Demo Tenant Account...")
        if tenant_ids:
            demo_tenant = tenant_ids[0] # Pick the first tenant
            demo_email = "tenant@example.com"
            demo_pass = "tenant123"
            
            # Create User
            u_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO users (id, email, password_hash, role)
                VALUES (%s, %s, %s, 'TENANT')
            """, (u_id, demo_email, generate_password_hash(demo_pass)))
            
            # Link User to Tenant Record
            cur.execute("""
                UPDATE tenants 
                SET user_id = %s, email = %s 
                WHERE id = %s
            """, (u_id, demo_email, demo_tenant['id']))
            conn.commit()
            
            print(f"   Linked 'Demo Tenant' to {demo_tenant['name']}")

        print("\n✅ MASSIVE DATA SEED COMPLETE!")
        print(f"Stats:")
        print(f" - 3 Properties created")
        print(f" - {len(room_ids)} Rooms created")
        print(f" - {len(tenant_ids)} Tenants moved in")
        print(f" - Hundreds of payments & expenses generated")
        print(f"\n🔑 Login Credentials:")
        print(f"   Email: {TEST_EMAIL}")
        print(f"   Pass:  {TEST_PASSWORD}")

    except Exception as e:
        conn.rollback()
        import traceback
        traceback.print_exc()
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    demo_seed()
