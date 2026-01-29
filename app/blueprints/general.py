from flask import render_template, session, redirect, url_for, request, flash, current_app
from . import bp
import os
from werkzeug.utils import secure_filename
from app.database.database import get_db_connection

@bp.route("/")
def index():
    if 'user_id' in session:
        if session.get('role') == 'OWNER':
            return redirect(url_for('main.owner_dashboard'))
        elif session.get('role') == 'TENANT':
             return redirect(url_for('main.tenant_dashboard'))
            
    return render_template("index.html")

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/careers')
def careers():
    return render_template('careers.html')

@bp.route('/careers/apply', methods=['POST'])
def apply_for_job():
    if request.method == 'POST':
        # 1. Capture Form Data
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']
        cover_letter = request.form.get('cover_letter', '')
        
        linkedin_url = request.form.get('linkedin_url', '')
        portfolio_url = request.form.get('portfolio_url', '')
        experience_years = request.form.get('experience_years', '')
        current_ctc = request.form.get('current_ctc', '')
        expected_ctc = request.form.get('expected_ctc', '')
        notice_period = request.form.get('notice_period', '')

        # 2. Handle File Upload
        resume_data = None
        resume_filename = None
        resume_mimetype = None
        
        if 'resume' in request.files:
            file = request.files['resume']
            if file.filename != '':
                resume_filename = secure_filename(file.filename)
                resume_mimetype = file.mimetype
                resume_data = file.read() # Read binary data
                
        # 3. Save to Database
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO job_applications 
                (full_name, email, phone, role_applied, resume_filename, resume_data, resume_mimetype, cover_letter,
                 linkedin_url, portfolio_url, experience_years, current_ctc, expected_ctc, notice_period)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (full_name, email, phone, role, resume_filename, resume_data, resume_mimetype, cover_letter,
                  linkedin_url, portfolio_url, experience_years, current_ctc, expected_ctc, notice_period))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"DB Error: {e}")
            flash('Error saving application. Please try again.', 'error')
            return redirect(url_for('main.careers'))

        # 4. Send Email via SMTP
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        smtp_server = os.environ.get('MAIL_SERVER')
        smtp_port = os.environ.get('MAIL_PORT')
        smtp_user = os.environ.get('MAIL_USERNAME')
        smtp_password = os.environ.get('MAIL_PASSWORD')

        if smtp_server and smtp_user and smtp_password:
            try:
                # A. Email to Admin
                msg_admin = MIMEMultipart()
                msg_admin['From'] = smtp_user
                msg_admin['To'] = smtp_user  # Send to self/admin
                msg_admin['Subject'] = f"New Job Application: {role} - {full_name}"
                
                body_admin = f"""
                New Applicant Details:
                ----------------------
                Name: {full_name}
                Email: {email}
                Phone: {phone}
                Role: {role}
                Experience: {experience_years}
                CTC (Current/Expected): {current_ctc} / {expected_ctc}
                Notice Period: {notice_period}
                LinkedIn: {linkedin_url}
                Portfolio: {portfolio_url}

                Resume Saved as: {resume_filename}
                """
                msg_admin.attach(MIMEText(body_admin, 'plain'))

                server = smtplib.SMTP(smtp_server, int(smtp_port) if smtp_port else 587)
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg_admin)

                # B. Email to Applicant
                msg_user = MIMEMultipart()
                msg_user['From'] = smtp_user
                msg_user['To'] = email
                msg_user['Subject'] = f"Application Received - {role} at PG-Manager"
                
                body_user = f"""
                Hi {full_name},

                Thanks for applying for the {role} position at PG-Manager.
                We have received your application and our team is currently reviewing it.

                We will get back to you shortly if your profile matches our requirements.

                Best Regards,
                PG-Manager HR Team
                """
                msg_user.attach(MIMEText(body_user, 'plain'))
                server.send_message(msg_user)
                
                server.quit()
                print("Emails sent successfully via SMTP.")

            except Exception as e:
                print(f"SMTP Error: {e}")
                # Don't fail the request if email fails, just log it
        else:
            print("SMTP credentials not found. Skipping email.")

        flash('Application submitted successfully! Check your email for confirmation.', 'success')
        return redirect(url_for('main.careers'))

    return redirect(url_for('main.careers'))
def time_ago(date):
    if not date: return ''
    from datetime import datetime, timezone, date as d
    
    # Handle datetime.date objects (no time)
    if not isinstance(date, datetime) and isinstance(date, d):
        date = datetime.combine(date, datetime.min.time())
        
    now = datetime.now(timezone.utc) if date.tzinfo else datetime.now()
    
    diff = now - date
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return 'Just now'
    elif seconds < 3600:
        return f'{int(seconds // 60)} mins ago'
    elif seconds < 86400:
        return f'{int(seconds // 3600)} hours ago'
    else:
        return f'{int(seconds // 86400)} days ago'
