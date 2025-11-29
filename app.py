from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import csv
from io import StringIO
from functools import wraps
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

load_dotenv()
# MySQL Configuration
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD') 
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = MySQL(app)

# Decorators for authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('user_login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin access required', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# ==================== USER ROUTES ====================

# User Registration
@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        city = request.form['city']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('user/register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('user/register.html')
        if not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter.', 'danger')
            return render_template('user/register.html')
        if not any(char.islower() for char in password):
            flash('Password must contain at least one lowercase letter.', 'danger')
            return render_template('user/register.html')
        if not any(char.isdigit() for char in password):
            flash('Password must contain at least one number.', 'danger')
            return render_template('user/register.html')
        if not any(not char.isalnum() for char in password):
            flash('Password must contain at least one special character.', 'danger')
            return render_template('user/register.html')

        password = generate_password_hash(request.form['password'])
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO Users (name, email, mobile, city, password) VALUES (%s, %s, %s, %s, %s)",
                       (name, email, mobile, city, password))
            mysql.connection.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('user_login'))
        except Exception as e:
            flash('Email already exists!', 'danger')
        finally:
            cur.close()
    
    return render_template('user/register.html')

# User Login
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE email = %s AND is_blocked = 0", [email])
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['user_name'] = user['name']
            session['user_type'] = 'user'
            flash('Login successful!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid credentials or account blocked', 'danger')
    
    return render_template('user/login.html')

# User Forgot Password
@app.route('/user/forgot_password', methods=['GET', 'POST'])
def user_forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()
        if user:
            return redirect(url_for('user_reset_password', email=email))
        else:
            flash('Email not found!', 'danger')
            return redirect(url_for('user_forgot_password'))
    return render_template('user/forgot_password.html')

@app.route('/user/reset_password/<email>', methods=['GET', 'POST'])
def user_reset_password(email):
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('user/reset_password.html', email=email)

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('user/reset_password.html', email=email)
        if not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter.', 'danger')
            return render_template('user/reset_password.html', email=email)
        if not any(char.islower() for char in password):
            flash('Password must contain at least one lowercase letter.', 'danger')
            return render_template('user/reset_password.html', email=email)
        if not any(char.isdigit() for char in password):
            flash('Password must contain at least one number.', 'danger')
            return render_template('user/reset_password.html', email=email)
        if not any(not char.isalnum() for char in password):
            flash('Password must contain at least one special character.', 'danger')
            return render_template('user/reset_password.html', email=email)

        password = generate_password_hash(request.form['password'])
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("UPDATE Users SET password = %s WHERE email = %s", (password, email))
            mysql.connection.commit()
            flash('Password updated successfully! Please login.', 'success')
            return redirect(url_for('user_login'))
        except Exception as e:
            flash('An error occurred!', 'danger')
        finally:
            cur.close()

    return render_template('user/reset_password.html', email=email)

# User Dashboard
@app.route('/user/dashboard')
@login_required
def user_dashboard():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT e.*, v.venue_name, v.city 
        FROM Events e 
        JOIN Venues v ON e.venue_id = v.venue_id 
        WHERE e.is_active = 1 AND e.end_date >= CURDATE()
        ORDER BY e.is_featured DESC, e.start_date ASC
    """)
    events = cur.fetchall()
    cur.close()
    
    return render_template('user/dashboard.html', events=events)

# Event Browsing
@app.route('/user/events')
@login_required
def browse_events():
    city = request.args.get('city', '')
    category = request.args.get('category', '')
    date = request.args.get('date', '')
    language = request.args.get('language', '')
    search = request.args.get('search', '')
    
    query = """
        SELECT e.*, v.venue_name, v.city 
        FROM Events e 
        JOIN Venues v ON e.venue_id = v.venue_id 
        WHERE e.is_active = 1 AND e.end_date >= CURDATE()
    """
    params = []
    
    if city:
        query += " AND v.city = %s"
        params.append(city)
    if category:
        query += " AND e.category = %s"
        params.append(category)
    if date:
        query += " AND %s BETWEEN e.start_date AND e.end_date"
        params.append(date)
    if language:
        query += " AND e.language = %s"
        params.append(language)
    if search:
        query += " AND (e.event_name LIKE %s OR e.category LIKE %s OR v.city LIKE %s)"
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    
    query += " ORDER BY e.is_featured DESC, e.start_date ASC"
    
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    events = cur.fetchall()
    
    # Get filter options
    cur.execute("SELECT DISTINCT city FROM Venues ORDER BY city")
    cities = [row['city'] for row in cur.fetchall()]
    
    cur.execute("SELECT DISTINCT category FROM Events WHERE is_active = 1 ORDER BY category")
    categories = [row['category'] for row in cur.fetchall()]
    
    cur.execute("SELECT DISTINCT language FROM Events WHERE is_active = 1 ORDER BY language")
    languages = [row['language'] for row in cur.fetchall()]
    
    cur.close()
    
    return render_template('user/events.html', events=events, cities=cities, 
                         categories=categories, languages=languages)

# Event Details
@app.route('/user/event/<int:event_id>')
@login_required
def event_details(event_id):
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT e.*, v.venue_name, v.city, v.address 
        FROM Events e 
        JOIN Venues v ON e.venue_id = v.venue_id 
        WHERE e.event_id = %s
    """, [event_id])
    event = cur.fetchone()
    
    if not event:
        flash('Event not found', 'danger')
        return redirect(url_for('browse_events'))
    
    cur.execute("""
        SELECT s.*, v.venue_name,
               (v.total_seats - COALESCE(SUM(bs.quantity), 0)) as available_seats
        FROM Shows s
        JOIN Venues v ON s.venue_id = v.venue_id
        LEFT JOIN Bookings b ON s.show_id = b.show_id AND b.status != 'Cancelled'
        LEFT JOIN Booking_Seats bs ON b.booking_id = bs.booking_id
        WHERE s.event_id = %s AND s.show_date >= CURDATE()
        GROUP BY s.show_id
        ORDER BY s.show_date, s.show_time
    """, [event_id])
    shows = cur.fetchall()
    
    cur.execute("""
        SELECT r.*, u.name as user_name
        FROM Reviews r
        JOIN Users u ON r.user_id = u.user_id
        WHERE r.event_id = %s
        ORDER BY r.created_at DESC
        LIMIT 10
    """, [event_id])
    reviews = cur.fetchall()
    
    cur.close()
    
    return render_template('user/event_details.html', event=event, shows=shows, reviews=reviews)

# Book Show - Select Seats
@app.route('/user/book/<int:show_id>', methods=['GET', 'POST'])
@login_required
def book_show(show_id):
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT s.*, e.event_name, e.poster_url, v.venue_name, v.city,
               v.silver_seats, v.gold_seats, v.platinum_seats, v.vip_seats,
               v.silver_price, v.gold_price, v.platinum_price, v.vip_price
        FROM Shows s
        JOIN Events e ON s.event_id = e.event_id
        JOIN Venues v ON s.venue_id = v.venue_id
        WHERE s.show_id = %s AND s.show_date >= CURDATE()
    """, [show_id])
    show = cur.fetchone()
    
    if not show:
        flash('Show not found or expired', 'danger')
        return redirect(url_for('browse_events'))
    
    # Calculate available seats by class
    cur.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN bs.seat_class = 'Silver' THEN bs.quantity ELSE 0 END), 0) as silver_booked,
            COALESCE(SUM(CASE WHEN bs.seat_class = 'Gold' THEN bs.quantity ELSE 0 END), 0) as gold_booked,
            COALESCE(SUM(CASE WHEN bs.seat_class = 'Platinum' THEN bs.quantity ELSE 0 END), 0) as platinum_booked,
            COALESCE(SUM(CASE WHEN bs.seat_class = 'VIP' THEN bs.quantity ELSE 0 END), 0) as vip_booked
        FROM Bookings b
        JOIN Booking_Seats bs ON b.booking_id = bs.booking_id
        WHERE b.show_id = %s AND b.status != 'Cancelled'
    """, [show_id])
    booked = cur.fetchone()
    
    available = {
        'Silver': show['silver_seats'] - booked['silver_booked'],
        'Gold': show['gold_seats'] - booked['gold_booked'],
        'Platinum': show['platinum_seats'] - booked['platinum_booked'],
        'VIP': show['vip_seats'] - booked['vip_booked']
    }
    
    prices = {
        'Silver': show['silver_price'],
        'Gold': show['gold_price'],
        'Platinum': show['platinum_price'],
        'VIP': show['vip_price']
    }
    
    # Get active offers
    cur.execute("""
        SELECT * FROM Offers 
        WHERE is_active = 1 
        AND CURDATE() BETWEEN valid_from AND valid_to
    """)
    offers = cur.fetchall()
    
    cur.close()
    
    if request.method == 'POST':
        seat_selections = []
        total_amount = 0
        
        for seat_class in ['Silver', 'Gold', 'Platinum', 'VIP']:
            quantity = int(request.form.get(f'{seat_class.lower()}_quantity', 0))
            if quantity > 0:
                if quantity > available[seat_class]:
                    flash(f'Not enough {seat_class} seats available', 'danger')
                    return redirect(url_for('book_show', show_id=show_id))
                
                seat_selections.append({
                    'class': seat_class,
                    'quantity': quantity,
                    'price': prices[seat_class]
                })
                total_amount += quantity * prices[seat_class]
        
        if not seat_selections:
            flash('Please select at least one seat', 'warning')
            return redirect(url_for('book_show', show_id=show_id))
        
        # Apply promo code if provided
        promo_code = request.form.get('promo_code', '').strip()
        discount = 0
        
        if promo_code:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT * FROM Offers 
                WHERE promo_code = %s AND is_active = 1 
                AND CURDATE() BETWEEN valid_from AND valid_to
            """, [promo_code])
            offer = cur.fetchone()
            cur.close()
            
            if offer:
                if offer['discount_type'] == 'Percentage':
                    discount = (total_amount * offer['discount_value']) / 100
                else:
                    discount = offer['discount_value']
                
                if offer['max_discount'] and discount > offer['max_discount']:
                    discount = offer['max_discount']
        
        final_amount = total_amount - discount
        
        # Create booking
        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO Bookings (user_id, show_id, total_amount, discount, final_amount, status)
                VALUES (%s, %s, %s, %s, %s, 'Pending')
            """, (session['user_id'], show_id, total_amount, discount, final_amount))
            
            booking_id = cur.lastrowid
            
            # Insert seat details
            for selection in seat_selections:
                cur.execute("""
                    INSERT INTO Booking_Seats (booking_id, seat_class, quantity, price_per_seat)
                    VALUES (%s, %s, %s, %s)
                """, (booking_id, selection['class'], selection['quantity'], selection['price']))
            
            mysql.connection.commit()
            flash('Booking created! Please complete payment.', 'success')
            return redirect(url_for('payment', booking_id=booking_id))
            
        except Exception as e:
            mysql.connection.rollback()
            flash('Booking failed. Please try again.', 'danger')
        finally:
            cur.close()
    
    return render_template('user/book_show.html', show=show, available=available, 
                         prices=prices, offers=offers)

# Payment
@app.route('/user/payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def payment(booking_id):
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT b.*, s.show_date, s.show_time, e.event_name, v.venue_name
        FROM Bookings b
        JOIN Shows s ON b.show_id = s.show_id
        JOIN Events e ON s.event_id = e.event_id
        JOIN Venues v ON s.venue_id = v.venue_id
        WHERE b.booking_id = %s AND b.user_id = %s
    """, (booking_id, session['user_id']))
    booking = cur.fetchone()
    
    if not booking:
        flash('Booking not found', 'danger')
        return redirect(url_for('user_dashboard'))
    
    cur.execute("""
        SELECT * FROM Booking_Seats WHERE booking_id = %s
    """, [booking_id])
    seats = cur.fetchall()
    
    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        
        cur.execute("""
            UPDATE Bookings 
            SET status = 'Confirmed', transaction_id = %s, payment_date = NOW()
            WHERE booking_id = %s
        """, (transaction_id, booking_id))
        mysql.connection.commit()
        
        flash('Payment successful! Booking confirmed.', 'success')
        cur.close()
        return redirect(url_for('my_bookings'))
    
    cur.close()
    return render_template('user/payment.html', booking=booking, seats=seats)

# My Bookings
@app.route('/user/bookings')
@login_required
def my_bookings():
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT b.*, s.show_date, s.show_time, e.event_name, e.poster_url, v.venue_name, v.city
        FROM Bookings b
        JOIN Shows s ON b.show_id = s.show_id
        JOIN Events e ON s.event_id = e.event_id
        JOIN Venues v ON s.venue_id = v.venue_id
        WHERE b.user_id = %s
        ORDER BY b.booking_date DESC
    """, [session['user_id']])
    bookings = cur.fetchall()
    
    cur.close()
    
    return render_template('user/my_bookings.html', bookings=bookings)

# Cancel Booking
@app.route('/user/cancel/<int:booking_id>')
@login_required
def cancel_booking(booking_id):
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT b.*, s.show_date, s.show_time
        FROM Bookings b
        JOIN Shows s ON b.show_id = s.show_id
        WHERE b.booking_id = %s AND b.user_id = %s AND b.status = 'Confirmed'
    """, (booking_id, session['user_id']))
    booking = cur.fetchone()
    
    if not booking:
        flash('Booking not found or cannot be cancelled', 'danger')
        return redirect(url_for('my_bookings'))
    
    # Check cancellation cutoff (2 hours before show)
    show_datetime = datetime.combine(booking['show_date'], 
                                     (datetime.min + booking['show_time']).time())
    cutoff = show_datetime - timedelta(hours=2)
    
    if datetime.now() >= cutoff:
        flash('Cannot cancel booking within 2 hours of show time', 'danger')
        return redirect(url_for('my_bookings'))
    
    cur.execute("UPDATE Bookings SET status = 'Cancelled' WHERE booking_id = %s", [booking_id])
    mysql.connection.commit()
    cur.close()
    
    flash('Booking cancelled successfully', 'success')
    return redirect(url_for('my_bookings'))

# Submit Review
@app.route('/user/review/<int:event_id>', methods=['POST'])
@login_required
def submit_review(event_id):
    rating = int(request.form['rating'])
    review_text = request.form['review']
    
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO Reviews (event_id, user_id, rating, review_text)
            VALUES (%s, %s, %s, %s)
        """, (event_id, session['user_id'], rating, review_text))
        mysql.connection.commit()
        flash('Review submitted successfully', 'success')
    except:
        flash('You have already reviewed this event', 'warning')
    finally:
        cur.close()
    
    return redirect(url_for('event_details', event_id=event_id))

# User Profile
@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        city = request.form['city']
        
        cur.execute("""
            UPDATE Users SET name = %s, mobile = %s, city = %s
            WHERE user_id = %s
        """, (name, mobile, city, session['user_id']))
        mysql.connection.commit()
        session['user_name'] = name
        flash('Profile updated successfully', 'success')
    
    cur.execute("SELECT * FROM Users WHERE user_id = %s", [session['user_id']])
    user = cur.fetchone()
    cur.close()
    
    return render_template('user/profile.html', user=user)

# User Logout
@app.route('/user/logout')
def user_logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# ==================== ADMIN ROUTES ====================

# Admin Registration
@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        emp_code = request.form['emp_code']
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('admin/register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('admin/register.html')
        if not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter.', 'danger')
            return render_template('admin/register.html')
        if not any(char.islower() for char in password):
            flash('Password must contain at least one lowercase letter.', 'danger')
            return render_template('admin/register.html')
        if not any(char.isdigit() for char in password):
            flash('Password must contain at least one number.', 'danger')
            return render_template('admin/register.html')
        if not any(not char.isalnum() for char in password):
            flash('Password must contain at least one special character.', 'danger')
            return render_template('admin/register.html')

        password = generate_password_hash(request.form['password'])
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO Admin (emp_code, name, mobile, email, username, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (emp_code, name, mobile, email, username, password))
            mysql.connection.commit()
            flash('Admin registration successful! Please login.', 'success')
            return redirect(url_for('admin_login'))
        except:
            flash('Username or email already exists!', 'danger')
        finally:
            cur.close()
    
    return render_template('admin/register.html')

# Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Admin WHERE username = %s", [username])
        admin = cur.fetchone()
        cur.close()
        
        if admin and check_password_hash(admin['password'], password):
            session['admin_id'] = admin['admin_id']
            session['admin_name'] = admin['name']
            session['user_type'] = 'admin'
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('admin/login.html')

# Admin Forgot Password
@app.route('/admin/forgot_password', methods=['GET', 'POST'])
def admin_forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Admin WHERE email = %s", [email])
        admin = cur.fetchone()
        cur.close()
        if admin:
            return redirect(url_for('admin_reset_password', email=email))
        else:
            flash('Email not found!', 'danger')
            return redirect(url_for('admin_forgot_password'))
    return render_template('admin/forgot_password.html')

@app.route('/admin/reset_password/<email>', methods=['GET', 'POST'])
def admin_reset_password(email):
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('admin/reset_password.html', email=email)

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('admin/reset_password.html', email=email)
        if not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter.', 'danger')
            return render_template('admin/reset_password.html', email=email)
        if not any(char.islower() for char in password):
            flash('Password must contain at least one lowercase letter.', 'danger')
            return render_template('admin/reset_password.html', email=email)
        if not any(char.isdigit() for char in password):
            flash('Password must contain at least one number.', 'danger')
            return render_template('admin/reset_password.html', email=email)
        if not any(not char.isalnum() for char in password):
            flash('Password must contain at least one special character.', 'danger')
            return render_template('admin/reset_password.html', email=email)

        password = generate_password_hash(request.form['password'])
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("UPDATE Admin SET password = %s WHERE email = %s", (password, email))
            mysql.connection.commit()
            flash('Password updated successfully! Please login.', 'success')
            return redirect(url_for('admin_login'))
        except Exception as e:
            flash('An error occurred!', 'danger')
        finally:
            cur.close()

    return render_template('admin/reset_password.html', email=email)

# Admin Dashboard
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    cur = mysql.connection.cursor()
    
    # Statistics
    cur.execute("SELECT COUNT(*) as total FROM Events WHERE is_active = 1")
    total_events = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as total FROM Bookings WHERE status = 'Confirmed'")
    total_bookings = cur.fetchone()['total']
    
    cur.execute("SELECT COALESCE(SUM(final_amount), 0) as total FROM Bookings WHERE status = 'Confirmed'")
    total_revenue = cur.fetchone()['total']
    
    cur.execute("""
        SELECT COALESCE(SUM(bs.quantity), 0) as total
        FROM Booking_Seats bs
        JOIN Bookings b ON bs.booking_id = b.booking_id
        WHERE b.status = 'Confirmed'
    """)
    total_tickets = cur.fetchone()['total']
    
    # Popular events
    cur.execute("""
        SELECT e.event_name, COUNT(b.booking_id) as bookings,
            COALESCE(SUM(b.final_amount), 0) as revenue
        FROM Events e
        LEFT JOIN Shows s ON e.event_id = s.event_id
        LEFT JOIN Bookings b ON s.show_id = b.show_id AND b.status = 'Confirmed'
        WHERE e.is_active = 1
        GROUP BY e.event_id
        ORDER BY bookings DESC
        LIMIT 5
    """)
    popular_events = cur.fetchall()
    
    cur.close()
    
    return render_template('admin/dashboard.html', 
                         total_events=total_events,
                         total_bookings=total_bookings,
                         total_revenue=total_revenue,
                         total_tickets=total_tickets,
                         popular_events=popular_events)

# Manage Events
@app.route('/admin/events')
@admin_required
def admin_events():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT e.*, v.venue_name, v.city
        FROM Events e
        JOIN Venues v ON e.venue_id = v.venue_id
        ORDER BY e.created_at DESC
    """)
    events = cur.fetchall()
    cur.close()
    
    return render_template('admin/events.html', events=events)

# Add Event
@app.route('/admin/event/add', methods=['GET', 'POST'])
@admin_required
def add_event():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        event_name = request.form['event_name']
        category = request.form['category']
        language = request.form['language']
        duration = int(request.form['duration'])
        age_rating = request.form['age_rating']
        description = request.form['description']
        poster_url = request.form['poster_url']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        venue_id = int(request.form['venue_id'])
        is_featured = 1 if request.form.get('is_featured') else 0
        
        try:
            cur.execute("""
                INSERT INTO Events (event_name, category, language, duration, age_rating, 
                                  description, poster_url, start_date, end_date, venue_id, is_featured)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (event_name, category, language, duration, age_rating, description, 
                  poster_url, start_date, end_date, venue_id, is_featured))
            mysql.connection.commit()
            flash('Event added successfully', 'success')
            return redirect(url_for('admin_events'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    cur.execute("SELECT * FROM Venues ORDER BY venue_name")
    venues = cur.fetchall()
    cur.close()
    
    return render_template('admin/add_event.html', venues=venues)

# Edit Event
@app.route('/admin/event/edit/<int:event_id>', methods=['GET', 'POST'])
@admin_required
def edit_event(event_id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        event_name = request.form['event_name']
        category = request.form['category']
        language = request.form['language']
        duration = int(request.form['duration'])
        age_rating = request.form['age_rating']
        description = request.form['description']
        poster_url = request.form['poster_url']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        venue_id = int(request.form['venue_id'])
        is_featured = 1 if request.form.get('is_featured') else 0
        is_active = 1 if request.form.get('is_active') else 0
        
        try:
            cur.execute("""
                UPDATE Events SET event_name=%s, category=%s, language=%s, duration=%s,
                                 age_rating=%s, description=%s, poster_url=%s, start_date=%s,
                                 end_date=%s, venue_id=%s, is_featured=%s, is_active=%s
                WHERE event_id = %s
            """, (event_name, category, language, duration, age_rating, description,
                  poster_url, start_date, end_date, venue_id, is_featured, is_active, event_id))
            mysql.connection.commit()
            flash('Event updated successfully', 'success')
            return redirect(url_for('admin_events'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    cur.execute("SELECT * FROM Events WHERE event_id = %s", [event_id])
    event = cur.fetchone()
    
    cur.execute("SELECT * FROM Venues ORDER BY venue_name")
    venues = cur.fetchall()
    cur.close()
    
    return render_template('admin/edit_event.html', event=event, venues=venues)

# Manage Venues
@app.route('/admin/venues')
@admin_required
def admin_venues():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Venues ORDER BY venue_name")
    venues = cur.fetchall()
    cur.close()
    
    return render_template('admin/venues.html', venues=venues)

# Add Venue
@app.route('/admin/venue/add', methods=['GET', 'POST'])
@admin_required
def add_venue():
    if request.method == 'POST':
        venue_name = request.form['venue_name']
        city = request.form['city']
        address = request.form['address']
        total_seats = int(request.form['total_seats'])
        silver_seats = int(request.form['silver_seats'])
        gold_seats = int(request.form['gold_seats'])
        platinum_seats = int(request.form['platinum_seats'])
        vip_seats = int(request.form['vip_seats'])
        silver_price = float(request.form['silver_price'])
        gold_price = float(request.form['gold_price'])
        platinum_price = float(request.form['platinum_price'])
        vip_price = float(request.form['vip_price'])
        
        if (silver_seats + gold_seats + platinum_seats + vip_seats) != total_seats:
            flash('Sum of class seats must equal total seats', 'danger')
            return redirect(url_for('add_venue'))
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO Venues (venue_name, city, address, total_seats, silver_seats,
                                  gold_seats, platinum_seats, vip_seats, silver_price,
                                  gold_price, platinum_price, vip_price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (venue_name, city, address, total_seats, silver_seats, gold_seats,
                  platinum_seats, vip_seats, silver_price, gold_price, platinum_price, vip_price))
            mysql.connection.commit()
            flash('Venue added successfully', 'success')
            return redirect(url_for('admin_venues'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cur.close()
    
    return render_template('admin/add_venue.html')

# Edit Venue
@app.route('/admin/venue/edit/<int:venue_id>', methods=['GET', 'POST'])
@admin_required
def edit_venue(venue_id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        venue_name = request.form['venue_name']
        city = request.form['city']
        address = request.form['address']
        total_seats = int(request.form['total_seats'])
        silver_seats = int(request.form['silver_seats'])
        gold_seats = int(request.form['gold_seats'])
        platinum_seats = int(request.form['platinum_seats'])
        vip_seats = int(request.form['vip_seats'])
        silver_price = float(request.form['silver_price'])
        gold_price = float(request.form['gold_price'])
        platinum_price = float(request.form['platinum_price'])
        vip_price = float(request.form['vip_price'])
        
        if (silver_seats + gold_seats + platinum_seats + vip_seats) != total_seats:
            flash('Sum of class seats must equal total seats', 'danger')
            return redirect(url_for('edit_venue', venue_id=venue_id))
        
        try:
            cur.execute("""
                UPDATE Venues SET venue_name=%s, city=%s, address=%s, total_seats=%s,
                                 silver_seats=%s, gold_seats=%s, platinum_seats=%s, vip_seats=%s,
                                 silver_price=%s, gold_price=%s, platinum_price=%s, vip_price=%s
                WHERE venue_id = %s
            """, (venue_name, city, address, total_seats, silver_seats, gold_seats,
                  platinum_seats, vip_seats, silver_price, gold_price, platinum_price,
                  vip_price, venue_id))
            mysql.connection.commit()
            flash('Venue updated successfully', 'success')
            return redirect(url_for('admin_venues'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    cur.execute("SELECT * FROM Venues WHERE venue_id = %s", [venue_id])
    venue = cur.fetchone()
    cur.close()
    
    return render_template('admin/edit_venue.html', venue=venue)

# Delete Venue
@app.route('/admin/venue/delete/<int:venue_id>')
@admin_required
def delete_venue(venue_id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM Venues WHERE venue_id = %s", [venue_id])
        mysql.connection.commit()
        flash('Venue deleted successfully', 'success')
    except:
        flash('Cannot delete venue with associated events', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('admin_venues'))

# Manage Shows
@app.route('/admin/shows')
@admin_required
def admin_shows():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT s.*, e.event_name, v.venue_name, v.city
        FROM Shows s
        JOIN Events e ON s.event_id = e.event_id
        JOIN Venues v ON s.venue_id = v.venue_id
        ORDER BY s.show_date DESC, s.show_time DESC
    """)
    shows = cur.fetchall()
    cur.close()
    
    return render_template('admin/shows.html', shows=shows)

# Add Show
@app.route('/admin/show/add', methods=['GET', 'POST'])
@admin_required
def add_show():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        event_id = int(request.form['event_id'])
        venue_id = int(request.form['venue_id'])
        show_date = request.form['show_date']
        show_time = request.form['show_time']
        
        try:
            cur.execute("""
                INSERT INTO Shows (event_id, venue_id, show_date, show_time)
                VALUES (%s, %s, %s, %s)
            """, (event_id, venue_id, show_date, show_time))
            mysql.connection.commit()
            flash('Show added successfully', 'success')
            return redirect(url_for('admin_shows'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    cur.execute("SELECT * FROM Events WHERE is_active = 1 ORDER BY event_name")
    events = cur.fetchall()
    
    cur.execute("SELECT * FROM Venues ORDER BY venue_name")
    venues = cur.fetchall()
    cur.close()
    
    return render_template('admin/add_show.html', events=events, venues=venues)

# Cancel Show
@app.route('/admin/show/cancel/<int:show_id>')
@admin_required
def cancel_show(show_id):
    cur = mysql.connection.cursor()
    
    # Cancel all confirmed bookings for this show
    cur.execute("""
        UPDATE Bookings SET status = 'Cancelled'
        WHERE show_id = %s AND status = 'Confirmed'
    """, [show_id])
    
    # Delete the show
    cur.execute("DELETE FROM Shows WHERE show_id = %s", [show_id])
    mysql.connection.commit()
    cur.close()
    
    flash('Show cancelled and all bookings refunded', 'success')
    return redirect(url_for('admin_shows'))

# Manage Bookings
@app.route('/admin/bookings')
@admin_required
def admin_bookings():
    event_id = request.args.get('event_id', '')
    venue_id = request.args.get('venue_id', '')
    user_id = request.args.get('user_id', '')
    date = request.args.get('date', '')
    status = request.args.get('status', '')
    
    query = """
        SELECT b.*, s.show_date, s.show_time, e.event_name, v.venue_name, u.name as user_name, u.email
        FROM Bookings b
        JOIN Shows s ON b.show_id = s.show_id
        JOIN Events e ON s.event_id = e.event_id
        JOIN Venues v ON s.venue_id = v.venue_id
        JOIN Users u ON b.user_id = u.user_id
        WHERE 1=1
    """
    params = []
    
    if event_id:
        query += " AND e.event_id = %s"
        params.append(event_id)
    if venue_id:
        query += " AND v.venue_id = %s"
        params.append(venue_id)
    if user_id:
        query += " AND b.user_id = %s"
        params.append(user_id)
    if date:
        query += " AND s.show_date = %s"
        params.append(date)
    if status:
        query += " AND b.status = %s"
        params.append(status)
    
    query += " ORDER BY b.booking_date DESC"
    
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    bookings = cur.fetchall()
    
    cur.execute("SELECT * FROM Events WHERE is_active = 1 ORDER BY event_name")
    events = cur.fetchall()
    
    cur.execute("SELECT * FROM Venues ORDER BY venue_name")
    venues = cur.fetchall()
    
    cur.close()
    
    return render_template('admin/bookings.html', bookings=bookings, 
                         events=events, venues=venues)

# Override Cancel Booking
@app.route('/admin/booking/cancel/<int:booking_id>')
@admin_required
def admin_cancel_booking(booking_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Bookings SET status = 'Cancelled' WHERE booking_id = %s", [booking_id])
    mysql.connection.commit()
    cur.close()
    
    flash('Booking cancelled successfully', 'success')
    return redirect(url_for('admin_bookings'))

# Manage Offers
@app.route('/admin/offers')
@admin_required
def admin_offers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Offers ORDER BY created_at DESC")
    offers = cur.fetchall()
    cur.close()
    
    return render_template('admin/offers.html', offers=offers)

# Add Offer
@app.route('/admin/offer/add', methods=['GET', 'POST'])
@admin_required
def add_offer():
    if request.method == 'POST':
        promo_code = request.form['promo_code'].upper()
        description = request.form['description']
        discount_type = request.form['discount_type']
        discount_value = float(request.form['discount_value'])
        max_discount = request.form.get('max_discount')
        max_discount = float(max_discount) if max_discount else None
        valid_from = request.form['valid_from']
        valid_to = request.form['valid_to']
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO Offers (promo_code, description, discount_type, discount_value,
                                  max_discount, valid_from, valid_to)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (promo_code, description, discount_type, discount_value, 
                  max_discount, valid_from, valid_to))
            mysql.connection.commit()
            flash('Offer added successfully', 'success')
            return redirect(url_for('admin_offers'))
        except:
            flash('Promo code already exists', 'danger')
        finally:
            cur.close()
    
    return render_template('admin/add_offer.html')

# Toggle Offer Status
@app.route('/admin/offer/toggle/<int:offer_id>')
@admin_required
def toggle_offer(offer_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Offers SET is_active = NOT is_active WHERE offer_id = %s", [offer_id])
    mysql.connection.commit()
    cur.close()
    
    flash('Offer status updated', 'success')
    return redirect(url_for('admin_offers'))

# Manage Users
@app.route('/admin/users')
@admin_required
def admin_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users ORDER BY created_at DESC")
    users = cur.fetchall()
    cur.close()
    
    return render_template('admin/users.html', users=users)

# Toggle User Block
@app.route('/admin/user/toggle/<int:user_id>')
@admin_required
def toggle_user_block(user_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Users SET is_blocked = NOT is_blocked WHERE user_id = %s", [user_id])
    mysql.connection.commit()
    cur.close()
    
    flash('User status updated', 'success')
    return redirect(url_for('admin_users'))

# Export Bookings
@app.route('/admin/export')
@admin_required
def export_bookings():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT b.booking_id, b.booking_date, b.total_amount, b.discount, b.final_amount,
               b.status, b.transaction_id, s.show_date, s.show_time,
               e.event_name, v.venue_name, u.name as user_name, u.email
        FROM Bookings b
        JOIN Shows s ON b.show_id = s.show_id
        JOIN Events e ON s.event_id = e.event_id
        JOIN Venues v ON s.venue_id = v.venue_id
        JOIN Users u ON b.user_id = u.user_id
        ORDER BY b.booking_date DESC
    """)
    bookings = cur.fetchall()
    cur.close()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Booking ID', 'Booking Date', 'User Name', 'Email', 'Event', 'Venue',
                    'Show Date', 'Show Time', 'Total Amount', 'Discount', 'Final Amount',
                    'Status', 'Transaction ID'])
    
    # Data
    for booking in bookings:
        writer.writerow([
            booking['booking_id'], booking['booking_date'], booking['user_name'],
            booking['email'], booking['event_name'], booking['venue_name'],
            booking['show_date'], booking['show_time'], booking['total_amount'],
            booking['discount'], booking['final_amount'], booking['status'],
            booking['transaction_id'] or 'N/A'
        ])
    
    output.seek(0)
    from flask import make_response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=bookings_export.csv'
    
    return response

# Admin Profile
@app.route('/admin/profile', methods=['GET', 'POST'])
@admin_required
def admin_profile():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        
        cur.execute("""
            UPDATE Admin SET name = %s, mobile = %s, email = %s
            WHERE admin_id = %s
        """, (name, mobile, email, session['admin_id']))
        mysql.connection.commit()
        session['admin_name'] = name
        flash('Profile updated successfully', 'success')
    
    cur.execute("SELECT * FROM Admin WHERE admin_id = %s", [session['admin_id']])
    admin = cur.fetchone()
    cur.close()
    
    return render_template('admin/profile.html', admin=admin)

# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/test_db')
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT 1')
        cur.close()
        return 'DB Connection Success :) '
    except Exception as e:
        return f'DB Connection Error: {e}'

if __name__ == '__main__':
    app.run(debug=True, port=5000)