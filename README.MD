# Event Ticket Booking System

A full-featured Flask-based event ticket booking system with user and admin functionalities.

## Features

### User Features
- User registration and authentication
- Browse events with filters (city, category, date, language)
- View event details with shows and reviews
- Book tickets with seat selection
- Apply promo codes for discounts
- Manage bookings (view, cancel)
- Submit reviews and ratings
- Profile management

### Admin Features
- Admin registration and authentication
- Dashboard with statistics
- Manage events (add, edit, activate/deactivate, feature)
- Manage venues (add, edit, delete, configure seats)
- Manage shows (create, cancel)
- View and manage bookings
- Create and manage promo codes
- Block/unblock users
- Export booking data to CSV

## Technology Stack
- **Backend:** Python Flask
- **Database:** MySQL
- **Frontend:** Bootstrap 5, HTML, CSS, JavaScript
- **Authentication:** Flask sessions with password hashing

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

Create `requirements.txt`:

```
Flask==3.0.0
Flask-MySQLdb==2.0.0
mysqlclient==2.2.0
Werkzeug==3.0.1
```

Install:

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

Or use the SQL file provided to create all tables and sample data.

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
│   │   ├── my_bookings.html
│   │   └── profile.html
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
│       ├── users.html
│       └── profile.html
└── static/ (optional, for custom CSS/JS)
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
4. **Book Tickets:** 
   - Select a show
   - Choose seat class and quantity
   - Apply promo code (optional)
   - Complete payment with a test transaction ID
5. **Manage Bookings:** View upcoming and past bookings, cancel if needed

### For Admins

1. **Register:** Go to `http://localhost:5000/admin/register`
2. **Login:** Use your username and password
3. **Add Venue:** Define seat layout and pricing
4. **Add Event:** Link to venue and set dates
5. **Create Shows:** Schedule show times
6. **Create Offers:** Add promo codes with discounts
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
2. Applies promo code (optional)
3. Reviews booking summary
4. Enters transaction ID (simulated payment)
5. Booking confirmed

### Cancellation Policy
- Users can cancel up to 2 hours before show time
- Admins can override and cancel any booking

### Business Logic
- Prevents double booking
- Auto-updates seat counts
- Validates promo codes
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
- `GET /user/dashboard` - User dashboard
- `GET /user/events` - Browse events with filters
- `GET /user/event/<id>` - Event details
- `GET/POST /user/book/<show_id>` - Book show
- `GET/POST /user/payment/<booking_id>` - Payment
- `GET /user/bookings` - My bookings
- `GET /user/cancel/<booking_id>` - Cancel booking
- `POST /user/review/<event_id>` - Submit review
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
6. View booking in "My Bookings"
7. Submit a review for the event

### Test Admin Flow
1. Register a new admin
2. Add a new venue
3. Add a new event linked to the venue
4. Create shows for the event
5. Create a promotional offer
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