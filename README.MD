# Event Ticket Booking System

A full-featured Flask-based event ticket booking system with user and admin functionalities.

## Features

### User Features
- **Registration & Auth:** Secure login/signup with password hashing.
- **Event Discovery:** - Dashboard split into "Live & Upcoming" and "Past" events.
  - Browse with filters (city, category, date, language).
- **Booking:** - Book tickets with specific seat selection (Silver, Gold, Platinum, VIP).
  - "Pay Now" option for pending bookings.
  - **New:** Dedicated Payment Success screen with receipt generation.
- **Ticket Management:**
  - **New:** Download printable tickets with booking details.
  - **New:** Password-protected cancellation system.
- **Engagement:** - Submit reviews and ratings.
  - **New:** Edit existing reviews.
- **Profile:** Manage personal details and view booking history.

### Admin Features
- **Dashboard:** Real-time statistics, revenue tracking, and popular events.
- **Event Management:** Add, edit, feature, and active/deactivate events.
- **Venue Management:** Configure venues with specific seat layouts and pricing.
- **Show Management:** - Schedule shows for events.
  - **New:** Shows categorized into "Ongoing" and "Passed" for better organization.
  - Cancel shows (auto-refunds bookings).
- **Booking Operations:** View all bookings, override/cancel bookings, export data to CSV.
- **Offers Management:** - Create promo codes.
  - **New:** Edit existing offers and toggle activation.
- **User Management:** Block/unblock users.

## Technology Stack
- **Backend:** Python Flask
- **Database:** MySQL
- **Frontend:** Bootstrap 5, HTML, CSS, JavaScript
- **Authentication:** Flask sessions with Werkzeug security hashing

## Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip

### Step 1: Clone or Create Project

```bash
mkdir ticket-booking-system
cd ticket-booking-system
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies


```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database

1. Login to MySQL:
```bash
mysql -u root -p
```

2. Create database and import schema:
```sql
CREATE DATABASE ticket_booking;
USE ticket_booking;
SOURCE database.sql;
```

Or use the SQL file 'init_queries.sql' provided to create all tables and sample data.

### Step 5: Configure Database Connection

Edit `app.py` and update MySQL credentials:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'  # Change this
app.config['MYSQL_DB'] = 'ticket_booking'
```

### Step 6: Project Structure

Create the following folder structure:

```
ticket-booking-system/
├── app.py
├── requirements.txt
├── database.sql
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── user/
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── events.html
│   │   ├── event_details.html
│   │   ├── book_show.html
│   │   ├── payment.html
│   │   ├── payment_success.html  
│   │   ├── my_bookings.html
│   │   ├── ticket.html           
│   │   ├── profile.html
│   │   ├── forgot_password.html
│   │   └── reset_password.html
│   └── admin/
│       ├── register.html
│       ├── login.html
│       ├── dashboard.html
│       ├── events.html
│       ├── add_event.html
│       ├── edit_event.html
│       ├── venues.html
│       ├── add_venue.html
│       ├── edit_venue.html
│       ├── shows.html
│       ├── add_show.html
│       ├── bookings.html
│       ├── offers.html
│       ├── add_offer.html
│       ├── edit_offer.html       
│       ├── users.html
│       ├── profile.html
│       ├── forgot_password.html
│       └── reset_password.html
└── static/ (optional)
```

### Step 7: Run the Application

```bash
python app.py
```

The application will run on `http://localhost:5000`

## Usage

### For Users

1. **Register:** Go to `http://localhost:5000/user/register`
2. **Login:** Use your email and password
3. **Browse Events:** Filter by city, category, date, or language
4. **Book Tickets:** - Select a show
   - Choose seat class and quantity
   - Apply promo code (optional)
   - Complete payment with a test transaction ID
   - **View and print payment receipt**
5. **Manage Bookings:** - View upcoming and past bookings
   - **Download/Print Tickets**
   - Cancel bookings (requires password)

### For Admins

1. **Register:** Go to `http://localhost:5000/admin/register`
2. **Login:** Use your username and password
3. **Add Venue:** Define seat layout and pricing
4. **Add Event:** Link to venue and set dates
5. **Manage Shows:** Schedule show times (categorized by Ongoing/Passed)
6. **Manage Offers:** Create and **Edit** promo codes
7. **Manage:** Monitor bookings, users, and export data

## Default Sample Data

The database comes with sample data:

**Venues:**
- Grand Theatre, Mumbai
- City Auditorium, Delhi
- Cultural Center, Bangalore
- Royal Arena, Pune

**Events:**
- The Phantom of Opera
- Bollywood Nights
- Comedy Carnival
- Classical Fusion
- Rock Festival 2024

**Promo Codes:**
- WELCOME20 (20% off, max ₹500)
- FLAT100 (Flat ₹100 off)
- WEEKEND50 (50% off, max ₹1000)
- EARLY200 (Flat ₹200 off)

## Key Features Explained

### Seat Management
- Venues have 4 seat classes: Silver, Gold, Platinum, VIP
- Each class has configurable quantity and price
- Real-time seat availability tracking

### Booking Flow
1. User selects show and seats
2. Applies promo code (validates expiry and limits)
3. Reviews booking summary
4. Enters transaction ID (simulated payment)
5. **Success Screen:** Displays receipt with print option
6. **Ticket Generation:** Downloadable ticket available in dashboard

### Cancellation Policy
- Users can cancel up to **24 hours** before show time
- **Security Check:** Users must enter their **account password** to confirm cancellation
- Admins can override and cancel any booking

### Business Logic
- Prevents double booking
- Auto-updates seat counts
- Validates promo codes (expiry and active status)
- Auto-cancels bookings when show is cancelled

## Database Schema

### Core Tables
- **Users:** User accounts and profiles
- **Admin:** Admin accounts
- **Venues:** Theater/venue information
- **Events:** Event details
- **Shows:** Event schedules
- **Bookings:** Ticket bookings
- **Booking_Seats:** Seat details per booking
- **Offers:** Promo codes
- **Reviews:** Event reviews and ratings

### Key Relationships
- Events belong to Venues
- Shows link Events to specific Venues and times
- Bookings link Users to Shows
- Reviews link Users to Events

## API Endpoints

### User Routes
- `GET/POST /user/register` - User registration
- `GET/POST /user/login` - User login
- `GET /user/dashboard` - User dashboard (Split views)
- `GET /user/events` - Browse events with filters
- `GET /user/event/<id>` - Event details
- `GET/POST /user/book/<show_id>` - Book show
- `GET/POST /user/payment/<booking_id>` - Payment
- `GET /user/ticket/<booking_id>` - **Download Ticket**
- `GET /user/bookings` - My bookings
- `POST /user/cancel/<booking_id>` - Cancel booking (with password)
- `POST /user/review/<event_id>` - Submit or Edit review
- `GET/POST /user/profile` - User profile
- `GET /user/logout` - Logout

### Admin Routes
- `GET/POST /admin/register` - Admin registration
- `GET/POST /admin/login` - Admin login
- `GET /admin/dashboard` - Admin dashboard with stats
- `GET /admin/events` - Manage events
- `GET/POST /admin/event/add` - Add event
- `GET/POST /admin/event/edit/<id>` - Edit event
- `GET /admin/venues` - Manage venues
- `GET/POST /admin/venue/add` - Add venue
- `GET/POST /admin/venue/edit/<id>` - Edit venue
- `GET /admin/venue/delete/<id>` - Delete venue
- `GET /admin/shows` - Manage shows
- `GET/POST /admin/show/add` - Add show
- `GET /admin/show/cancel/<id>` - Cancel show
- `GET /admin/bookings` - View all bookings
- `GET /admin/booking/cancel/<id>` - Cancel booking
- `GET /admin/offers` - Manage offers
- `GET/POST /admin/offer/add` - Add offer
- `GET/POST /admin/offer/edit/<id>` - **Edit offer**
- `GET /admin/offer/toggle/<id>` - Activate/deactivate
- `GET /admin/users` - Manage users
- `GET /admin/user/toggle/<id>` - Block/unblock user
- `GET /admin/export` - Export bookings CSV
- `GET/POST /admin/profile` - Admin profile
- `GET /admin/logout` - Logout

## Security Features
- Password hashing using Werkzeug
- Session-based authentication
- Login required decorators
- SQL injection prevention (parameterized queries)
- Input validation

## Testing

### Test User Flow
1. Register a new user
2. Browse and filter events
3. Select an event and view shows
4. Book tickets with promo code WELCOME20
5. Enter transaction ID: TEST123456
6. **Download Ticket** from "My Bookings"
7. **Edit Review** for the event

### Test Admin Flow
1. Register a new admin
2. Add a new venue
3. Add a new event linked to the venue
4. Create shows for the event
5. Create and **Edit** a promotional offer
6. View booking statistics
7. Export booking data

## Troubleshooting

### MySQL Connection Error
```
Error: (2002, "Can't connect to MySQL server")
```
**Solution:** Ensure MySQL is running and credentials are correct in `app.py`

### Table Not Found
```
Error: (1146, "Table 'ticket_booking.users' doesn't exist")
```
**Solution:** Import the database schema: `mysql -u root -p ticket_booking < database.sql`

### Port Already in Use
```
Error: Address already in use
```
**Solution:** Change port in `app.py`: `app.run(debug=True, port=5001)`

## Future Enhancements
- Payment gateway integration
- Email notifications
- QR code generation for tickets
- Seat map visualization
- Advanced analytics dashboard
- Mobile app
- Social media integration
- Multi-language support

## License
MIT License - Free to use and modify

## Support
For issues or questions, please create an issue in the repository.

## Contributors
Developed for educational and demonstration purposes.