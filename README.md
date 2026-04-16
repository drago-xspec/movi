# CineBook - Movie Ticket Booking System

A full-stack movie booking web application built with **Python/Flask**, **MongoDB**, and **Vanilla JavaScript**.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Admin Panel](#admin-panel)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### 1. **User Authentication**
- User registration with email validation
- Secure login with JWT tokens
- Password hashing using Werkzeug
- Profile management

### 2. **Movie Browsing**
- Display movie listings with posters, ratings, duration, cast
- Search by title or description
- Filter by genre
- Beautiful movie cards with hover effects

### 3. **Theater & Schedule Management**
- View available theaters in different cities
- Multiple show timings for each movie
- Different pricing for different shows
- Multiple formats (2D, 3D, IMAX) and languages

### 4. **Interactive Seat Selection**
- Visual seat grid layout (10x10)
- Real-time seat availability
- Select/deselect seats
- Booking summary with total price

### 5. **Booking & Payment**
- Create bookings with selected seats
- Mock payment gateway integration
- Card number, expiry, CVV validation
- Booking confirmation with reference number

### 6. **Booking History**
- View all user bookings
- Cancel pending bookings
- Booking status tracking (pending, confirmed, cancelled)

### 7. **Admin Panel**
- Dashboard with statistics (users, bookings, revenue)
- Add/manage movies with posters
- Add/manage theaters and screens
- Add/manage show timings
- Initialize seats for shows
- View all bookings

### 8. **Responsive Design**
- Mobile-friendly interface
- Works on desktop, tablet, and phone
- Touch-friendly seat selection
- Responsive navigation

---

## 📁 Project Structure

```
movie-booking-api/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration example
├── seed_db.py            # Database seeding script
├── index.html            # Frontend HTML
├── app.js                # Frontend JavaScript
├── styles.css            # Frontend CSS
└── README.md             # This file
```

---

## 🔧 Prerequisites

### Required Software
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **MongoDB 4.0+** - [Download](https://www.mongodb.com/try/download/community)
- **Node.js** (optional, for package management)
- **Git** (optional, for version control)

### Browser Requirements
- Modern browser with ES6 support (Chrome, Firefox, Safari, Edge)
- JavaScript enabled

---

## 📦 Installation & Setup

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <your-repo-url>
cd movie-booking-api

# Or manually extract the files
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your settings
# Change SECRET_KEY to a strong random string
# Update MONGO_URI if MongoDB is on different host
```

### Step 5: Ensure MongoDB is Running

```bash
# On Windows
mongod

# On macOS (with Homebrew)
brew services start mongodb-community

# On Linux
sudo systemctl start mongod
```

### Step 6: Seed Database with Sample Data

```bash
python seed_db.py
```

You should see output like:
```
🗑️  Clearing existing collections...
📽️  Adding sample movies...
✅ Inserted 10 movies
🏢 Adding sample theaters...
✅ Inserted 5 theaters

📊 Database seeding complete!
   - Movies: 10
   - Theaters: 5
```

---

## 🚀 Running the Application

### Start the Flask Backend

```bash
# From the project directory with venv activated
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000/
 * Debug mode: on
```

### Open the Frontend

1. Open `index.html` in your web browser
   - Double-click the file, or
   - Use a local server:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Then navigate to http://localhost:8000/index.html
   ```

2. The application is now ready to use!

---

## 🔌 API Documentation

### Authentication Endpoints

#### Register User
```
POST /api/auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "password123",
    "phone": "9876543210"
}

Response: {
    "message": "User registered successfully",
    "token": "jwt_token_here",
    "user": { ... }
}
```

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}

Response: {
    "message": "Login successful",
    "token": "jwt_token_here",
    "user": { ... }
}
```

#### Get Profile
```
GET /api/auth/profile
Authorization: Bearer {token}

Response: {
    "user": { ... }
}
```

#### Update Profile
```
PUT /api/auth/profile
Authorization: Bearer {token}
Content-Type: application/json

{
    "full_name": "New Name",
    "phone": "9876543210"
}
```

### Movie Endpoints

#### Get All Movies
```
GET /api/movies?search=keyword&genre=Action
Response: { "movies": [...] }
```

#### Get Movie Details
```
GET /api/movies/{movie_id}
Response: { "movie": {...} }
```

#### Add Movie (Admin Only)
```
POST /api/movies
Authorization: Bearer {token}
Content-Type: application/json

{
    "title": "Movie Title",
    "genre": "Action",
    "duration": 148,
    "rating": 8.5,
    "description": "...",
    "poster_url": "https://...",
    "release_date": "2024-01-01",
    "cast": ["Actor1", "Actor2"]
}
```

### Theater Endpoints

#### Get All Theaters
```
GET /api/theaters
Response: { "theaters": [...] }
```

#### Add Theater (Admin Only)
```
POST /api/theaters
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "PVR Cinemas",
    "city": "Mumbai",
    "address": "...",
    "screens": 8,
    "total_seats": 100
}
```

### Show Endpoints

#### Get Shows
```
GET /api/shows?movie_id={id}&theater_id={id}&date=2024-01-01
Response: { "shows": [...] }
```

#### Add Show (Admin Only)
```
POST /api/shows
Authorization: Bearer {token}
Content-Type: application/json

{
    "movie_id": "...",
    "theater_id": "...",
    "show_date": "2024-01-01",
    "show_time": "14:30",
    "price": 300,
    "language": "English",
    "format": "2D"
}
```

### Booking Endpoints

#### Create Booking
```
POST /api/bookings
Authorization: Bearer {token}
Content-Type: application/json

{
    "show_id": "...",
    "seat_ids": ["seat_id_1", "seat_id_2"]
}

Response: {
    "booking_id": "...",
    "booking_reference": "BK20240101123456",
    "total_price": 600
}
```

#### Get User Bookings
```
GET /api/bookings/user
Authorization: Bearer {token}
Response: { "bookings": [...] }
```

#### Cancel Booking
```
PUT /api/bookings/{booking_id}/cancel
Authorization: Bearer {token}
Response: { "message": "Booking cancelled successfully" }
```

### Payment Endpoints

#### Process Payment
```
POST /api/payments
Authorization: Bearer {token}
Content-Type: application/json

{
    "booking_id": "...",
    "card_number": "1234567890123456",
    "expiry": "12/25",
    "cvv": "123",
    "payment_method": "credit_card"
}

Response: {
    "transaction_id": "TXN...",
    "booking_id": "..."
}
```

### Admin Endpoints

#### Get Statistics
```
GET /api/admin/stats
Authorization: Bearer {token}
Response: {
    "total_users": 50,
    "total_bookings": 100,
    "total_revenue": 50000,
    "pending_bookings": 5
}
```

#### Get All Bookings
```
GET /api/admin/bookings
Authorization: Bearer {token}
Response: { "bookings": [...] }
```

---

## 🗄️ Database Schema

### Users Collection
```json
{
    "_id": ObjectId,
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "hashed_password",
    "phone": "9876543210",
    "role": "user",  // or "admin"
    "created_at": ISODate,
    "updated_at": ISODate
}
```

### Movies Collection
```json
{
    "_id": ObjectId,
    "title": "Movie Title",
    "genre": "Action",
    "duration": 148,
    "rating": 8.5,
    "description": "...",
    "poster_url": "https://...",
    "release_date": "2024-01-01",
    "cast": ["Actor1", "Actor2"],
    "created_at": ISODate,
    "updated_at": ISODate
}
```

### Theaters Collection
```json
{
    "_id": ObjectId,
    "name": "PVR Cinemas",
    "city": "Mumbai",
    "address": "...",
    "screens": 8,
    "total_seats": 100,
    "created_at": ISODate,
    "updated_at": ISODate
}
```

### Shows Collection
```json
{
    "_id": ObjectId,
    "movie_id": ObjectId,
    "theater_id": ObjectId,
    "show_date": "2024-01-01",
    "show_time": "14:30",
    "price": 300,
    "language": "English",
    "format": "2D",
    "created_at": ISODate,
    "updated_at": ISODate
}
```

### Seats Collection
```json
{
    "_id": ObjectId,
    "show_id": ObjectId,
    "seat_number": 1,
    "row": "A",
    "column": 1,
    "is_booked": false,
    "booked_by": ObjectId,
    "booking_id": ObjectId,
    "created_at": ISODate
}
```

### Bookings Collection
```json
{
    "_id": ObjectId,
    "user_id": ObjectId,
    "show_id": ObjectId,
    "seat_ids": [ObjectId, ObjectId],
    "total_seats": 2,
    "total_price": 600,
    "status": "confirmed",  // pending, confirmed, cancelled
    "booking_reference": "BK20240101123456",
    "payment_id": ObjectId,
    "created_at": ISODate,
    "updated_at": ISODate
}
```

### Payments Collection
```json
{
    "_id": ObjectId,
    "booking_id": ObjectId,
    "user_id": ObjectId,
    "amount": 600,
    "payment_method": "credit_card",
    "status": "completed",
    "transaction_id": "TXN20240101123456",
    "created_at": ISODate
}
```

---

## 👨‍💼 Admin Panel

### Access Admin Panel
1. Create an account as regular user
2. Ask a database admin to change your role to "admin" in MongoDB
3. Login - Admin menu will appear in navigation
4. Click "Admin Panel" link

### Admin Functions

#### Dashboard
- View total users
- View total bookings
- View total revenue
- View pending bookings

#### Manage Movies
- Add new movies with posters
- Movies stored with ratings, duration, cast
- Supports all genres

#### Manage Theaters
- Add multiple theaters in different cities
- Specify screen count and seat capacity
- Track theater information

#### Manage Shows
- Add showtimes for movies
- Set pricing per show
- Choose language and format
- Automatic seat initialization

#### View Bookings
- See all user bookings
- Track booking status
- Monitor revenue

---

## 🔐 Security Features

- **Password Hashing**: Using Werkzeug for secure password storage
- **JWT Authentication**: Token-based authentication with expiration
- **Input Validation**: All inputs validated on backend
- **CORS Enabled**: Configured for cross-origin requests
- **Admin Role Check**: Admin endpoints require admin role
- **Database Indexes**: Indexes on frequently queried fields

---

## 📝 Sample Test Data

After running `seed_db.py`, you have:

**Sample Movies:**
- The Shawshank Redemption (9.3 rating)
- The Godfather (9.2 rating)
- The Dark Knight (9.0 rating)
- Pulp Fiction (8.9 rating)
- Forrest Gump (8.8 rating)
- Inception (8.8 rating)
- The Matrix (8.7 rating)
- Interstellar (8.6 rating)
- Avengers: Endgame (8.4 rating)
- Fight Club (8.8 rating)

**Sample Theaters:**
- PVR Cinemas - Downtown (Mumbai)
- INOX Plaza (Delhi)
- Cinepolis Grand (Bangalore)
- Star Cinema (Hyderabad)
- Raj Cinema Complex (Pune)

---

## 🐛 Troubleshooting

### MongoDB Connection Error
**Error**: `connection refused`

**Solution**:
1. Ensure MongoDB is running
2. Check MongoDB URI in `.env`
3. Verify MongoDB is on correct port (default 27017)

### CORS Error
**Error**: `No 'Access-Control-Allow-Origin' header`

**Solution**:
- CORS is already enabled in `app.py`
- Ensure Flask is running on `http://localhost:5000`
- Open frontend from `http://localhost:8000`

### JWT Token Expired
**Error**: `Token is invalid!`

**Solution**:
- Login again to get new token
- Token expires after 30 days

### Images Not Loading
**Error**: Movie posters showing broken image

**Solution**:
- URLs are from external sources
- Check internet connection
- Edit poster URLs in database if needed

### Port Already in Use
**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 5000
# Windows: netstat -ano | findstr :5000
# Mac/Linux: lsof -i :5000

# Kill the process and try again
```

---

## 🚀 Deploy to Production

### Changes Needed:

1. **Set Strong Secret Key**
```python
# In app.py or .env
SECRET_KEY = 'generate-a-strong-random-key'
```

2. **Disable Debug Mode**
```python
# In app.py
app.run(debug=False, port=5000)
```

3. **Use Production Database**
```
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/
```

4. **Use HTTPS**
- Deploy using gunicorn or similar WSGI server
- Use SSL certificates

5. **Set CORS Properly**
```python
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

---

## 📱 Browser Compatibility

- ✅ Chrome (Latest)
- ✅ Firefox (Latest)
- ✅ Safari (Latest)
- ✅ Edge (Latest)
- ⚠️ Internet Explorer (Not supported)

---

## 🤝 Contributing

This is a learning project. Feel free to:
- Report issues
- Suggest improvements
- Add new features

---

## 💡 Future Enhancements

- [ ] Email notifications for bookings
- [ ] SMS notifications
- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] User reviews and ratings
- [ ] Wishlist feature
- [ ] Group booking discounts
- [ ] Promotional codes
- [ ] Real-time seat updates (WebSocket)
- [ ] Multiple language support
- [ ] Advanced analytics for admins

---

## 📞 Support

For issues and questions:
1. Check the Troubleshooting section
2. Review API documentation
3. Check browser console for errors
4. Verify all prerequisites are installed

---

## 📄 License

This project is open source and available for educational purposes.

---

## 👨‍💻 Created By

Movie Booking System - A full-stack learning project

---

**Last Updated**: January 2024
**Version**: 1.0.0
