CREATE DATABASE IF NOT EXISTS ticket_booking;
-- drop database ticket_booking; 
USE ticket_booking;

show tables;
select * from users;
-- Users Table
-- CREATE TABLE Users (
--     user_id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(100) NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL,
--     mobile VARCHAR(15) NOT NULL,
--     city VARCHAR(50) NOT NULL,
--     password VARCHAR(255) NOT NULL,
--     is_blocked BOOLEAN DEFAULT 0,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Admin Table
-- CREATE TABLE Admin (
--     admin_id INT AUTO_INCREMENT PRIMARY KEY,
--     emp_code VARCHAR(50) UNIQUE NOT NULL,
--     name VARCHAR(100) NOT NULL,
--     mobile VARCHAR(15) NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL,
--     username VARCHAR(50) UNIQUE NOT NULL,
--     password VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Venues Table
-- CREATE TABLE Venues (
--     venue_id INT AUTO_INCREMENT PRIMARY KEY,
--     venue_name VARCHAR(150) NOT NULL,
--     city VARCHAR(50) NOT NULL,
--     address TEXT NOT NULL,
--     total_seats INT NOT NULL,
--     silver_seats INT NOT NULL DEFAULT 0,
--     gold_seats INT NOT NULL DEFAULT 0,
--     platinum_seats INT NOT NULL DEFAULT 0,
--     vip_seats INT NOT NULL DEFAULT 0,
--     silver_price DECIMAL(10, 2) NOT NULL DEFAULT 0,
--     gold_price DECIMAL(10, 2) NOT NULL DEFAULT 0,
--     platinum_price DECIMAL(10, 2) NOT NULL DEFAULT 0,
--     vip_price DECIMAL(10, 2) NOT NULL DEFAULT 0,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Events Table
-- CREATE TABLE Events (
--     event_id INT AUTO_INCREMENT PRIMARY KEY,
--     event_name VARCHAR(150) NOT NULL,
--     category VARCHAR(50) NOT NULL,
--     language VARCHAR(50) NOT NULL,
--     duration INT NOT NULL COMMENT 'Duration in minutes',
--     age_rating VARCHAR(10) NOT NULL,
--     description TEXT,
--     poster_url VARCHAR(255),
--     start_date DATE NOT NULL,
--     end_date DATE NOT NULL,
--     venue_id INT NOT NULL,
--     is_active BOOLEAN DEFAULT 1,
--     is_featured BOOLEAN DEFAULT 0,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (venue_id) REFERENCES Venues(venue_id) ON DELETE RESTRICT
-- );

-- Shows Table
-- CREATE TABLE Shows (
--     show_id INT AUTO_INCREMENT PRIMARY KEY,
--     event_id INT NOT NULL,
--     venue_id INT NOT NULL,
--     show_date DATE NOT NULL,
--     show_time TIME NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE,
--     FOREIGN KEY (venue_id) REFERENCES Venues(venue_id) ON DELETE RESTRICT,
--     UNIQUE KEY unique_show (venue_id, show_date, show_time)
-- );

-- Bookings Table
-- CREATE TABLE Bookings (
--     booking_id INT AUTO_INCREMENT PRIMARY KEY,
--     user_id INT NOT NULL,
--     show_id INT NOT NULL,
--     booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     total_amount DECIMAL(10, 2) NOT NULL,
--     discount DECIMAL(10, 2) DEFAULT 0,
--     final_amount DECIMAL(10, 2) NOT NULL,
--     status ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Pending',
--     transaction_id VARCHAR(100),
--     payment_date TIMESTAMP NULL,
--     FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
--     FOREIGN KEY (show_id) REFERENCES Shows(show_id) ON DELETE CASCADE
-- );

-- Booking Seats Table
-- CREATE TABLE Booking_Seats (
--     booking_seat_id INT AUTO_INCREMENT PRIMARY KEY,
--     booking_id INT NOT NULL,
--     seat_class ENUM('Silver', 'Gold', 'Platinum', 'VIP') NOT NULL,
--     quantity INT NOT NULL,
--     price_per_seat DECIMAL(10, 2) NOT NULL,
--     FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE
-- );

-- Offers Table
-- CREATE TABLE Offers (
--     offer_id INT AUTO_INCREMENT PRIMARY KEY,
--     promo_code VARCHAR(50) UNIQUE NOT NULL,
--     description TEXT,
--     discount_type ENUM('Percentage', 'Fixed') NOT NULL,
--     discount_value DECIMAL(10, 2) NOT NULL,
--     max_discount DECIMAL(10, 2) NULL,
--     valid_from DATE NOT NULL,
--     valid_to DATE NOT NULL,
--     is_active BOOLEAN DEFAULT 1,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Reviews Table
-- CREATE TABLE Reviews (
--     review_id INT AUTO_INCREMENT PRIMARY KEY,
--     event_id INT NOT NULL,
--     user_id INT NOT NULL,
--     rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
--     review_text TEXT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE,
--     FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
--     UNIQUE KEY unique_review (event_id, user_id)
-- );

-- Indexes for performance
-- CREATE INDEX idx_events_active ON Events(is_active, start_date, end_date);
-- CREATE INDEX idx_shows_date ON Shows(show_date, show_time);
-- CREATE INDEX idx_bookings_user ON Bookings(user_id, status);
-- CREATE INDEX idx_bookings_show ON Bookings(show_id, status);
-- CREATE INDEX idx_offers_promo ON Offers(promo_code, is_active);
-- CREATE INDEX idx_reviews_event ON Reviews(event_id);

-- Sample Data
-- Insert Sample Venues
-- INSERT INTO Venues (venue_name, city, address, total_seats, silver_seats, gold_seats, platinum_seats, vip_seats, silver_price, gold_price, platinum_price, vip_price) VALUES
-- ('Grand Theatre', 'Mumbai', '123 Marine Drive, Mumbai', 500, 200, 150, 100, 50, 200.00, 350.00, 500.00, 800.00),
-- ('City Auditorium', 'Delhi', '456 Connaught Place, Delhi', 600, 250, 200, 100, 50, 180.00, 320.00, 450.00, 750.00),
-- ('Cultural Center', 'Bangalore', '789 MG Road, Bangalore', 400, 180, 120, 70, 30, 220.00, 380.00, 550.00, 900.00),
-- ('Royal Arena', 'Pune', '321 FC Road, Pune', 450, 200, 140, 80, 30, 190.00, 330.00, 480.00, 780.00);

-- Insert Sample Events
-- INSERT INTO Events (event_name, category, language, duration, age_rating, description, poster_url, start_date, end_date, venue_id, is_active, is_featured) VALUES
-- ('The Phantom of Opera', 'Musical', 'English', 180, 'U', 'A spectacular musical about a mysterious phantom haunting the Paris Opera House.', 'https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?w=400', '2025-12-01', '2025-12-31', 1, 1, 1),
-- ('Bollywood Nights', 'Concert', 'Hindi', 150, 'U', 'An evening of classic Bollywood hits performed live.', 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400', '2025-11-28', '2025-12-15', 2, 1, 1),
-- ('Comedy Carnival', 'Comedy', 'English', 120, 'A', 'Stand-up comedy show featuring top comedians.', 'https://images.unsplash.com/photo-1585699324551-f6c309eedeca?w=400', '2025-11-25', '2025-12-10', 3, 1, 0),
-- ('Classical Fusion', 'Classical', 'Instrumental', 135, 'U', 'A beautiful blend of Indian classical and western music.', 'https://images.unsplash.com/photo-1507838153414-b4b713384a76?w=400', '2025-12-05', '2025-12-20', 4, 1, 0),
-- ('Rock Festival 2025', 'Concert', 'English', 240, 'A', 'Two-day rock music festival featuring international and local bands.', 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=400', '2025-12-15', '2025-12-16', 1, 1, 1);

-- Insert Sample Shows
-- INSERT INTO Shows (event_id, venue_id, show_date, show_time) VALUES
-- (1, 1, '2025-12-01', '19:00:00'),
-- (1, 1, '2025-12-02', '19:00:00'),
-- (1, 1, '2025-12-07', '15:00:00'),
-- (1, 1, '2025-12-08', '19:00:00'),
-- (2, 2, '2025-11-28', '20:00:00'),
-- (2, 2, '2025-11-29', '20:00:00'),
-- (2, 2, '2025-12-05', '20:00:00'),
-- (3, 3, '2025-11-30', '19:30:00'),
-- (3, 3, '2025-12-01', '19:30:00'),
-- (4, 4, '2025-12-06', '18:00:00'),
-- (4, 4, '2025-12-07', '18:00:00'),
-- (5, 1, '2025-12-15', '17:00:00'),
-- (5, 1, '2025-12-16', '17:00:00');

-- Insert Sample Offers
-- INSERT INTO Offers (promo_code, description, discount_type, discount_value, max_discount, valid_from, valid_to, is_active) VALUES
-- ('WELCOME20', 'Welcome offer - 20% off on your first booking', 'Percentage', 20.00, 500.00, '2025-11-01', '2025-12-31', 1),
-- ('FLAT100', 'Flat Rs. 100 off on all bookings', 'Fixed', 100.00, NULL, '2025-11-15', '2025-12-15', 1),
-- ('WEEKEND50', 'Weekend special - 50% off', 'Percentage', 50.00, 1000.00, '2025-11-23', '2025-12-31', 1),
-- ('EARLY200', 'Early bird discount - Rs. 200 off', 'Fixed', 200.00, NULL, '2025-11-20', '2025-12-10', 1);