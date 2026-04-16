from flask import Flask, request, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import os
import jwt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ALGORITHM'] = 'HS256'

CORS(app)

# MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['movie_booking_db']

# Collections
users_collection = db['users']
movies_collection = db['movies']
theaters_collection = db['theaters']
shows_collection = db['shows']
bookings_collection = db['bookings']
seats_collection = db['seats']
payments_collection = db['payments']

# Create indexes
users_collection.create_index('email', unique=True)
movies_collection.create_index('title')
shows_collection.create_index(['movie_id', 'theater_id', 'show_time'])
bookings_collection.create_index('user_id')
bookings_collection.create_index('show_id')

# ==================== Helper Functions ====================

def token_required(f):
    """Decorator to check JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[app.config['JWT_ALGORITHM']])
            current_user = users_collection.find_one({'_id': data['user_id']})
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator to check admin role"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.get('role') != 'admin':
            return jsonify({'message': 'Admin access required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

def generate_token(user_id):
    """Generate JWT token"""
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(days=30)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm=app.config['JWT_ALGORITHM'])

def serialize_document(doc):
    """Convert MongoDB ObjectId to string"""
    if doc:
        doc['id'] = str(doc.pop('_id', ''))
    return doc

# ==================== Authentication Routes ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration"""
    data = request.get_json()
    
    # Validate input
    if not data.get('email') or not data.get('password') or not data.get('full_name'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user exists
    if users_collection.find_one({'email': data['email']}):
        return jsonify({'message': 'Email already registered'}), 400
    
    # Create new user
    new_user = {
        'email': data['email'],
        'full_name': data['full_name'],
        'password': generate_password_hash(data['password']),
        'phone': data.get('phone', ''),
        'role': 'user',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    result = users_collection.insert_one(new_user)
    token = generate_token(result.inserted_id)
    
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': {
            'id': str(result.inserted_id),
            'email': data['email'],
            'full_name': data['full_name']
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400
    
    user = users_collection.find_one({'email': data['email']})
    
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    token = generate_token(user['_id'])
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': str(user['_id']),
            'email': user['email'],
            'full_name': user['full_name'],
            'role': user.get('role', 'user')
        }
    }), 200

@app.route('/api/auth/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get user profile"""
    return jsonify({
        'user': {
            'id': str(current_user['_id']),
            'email': current_user['email'],
            'full_name': current_user['full_name'],
            'phone': current_user.get('phone', ''),
            'role': current_user.get('role', 'user')
        }
    }), 200

@app.route('/api/auth/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user profile"""
    data = request.get_json()
    
    update_fields = {}
    if 'full_name' in data:
        update_fields['full_name'] = data['full_name']
    if 'phone' in data:
        update_fields['phone'] = data['phone']
    
    update_fields['updated_at'] = datetime.utcnow()
    
    users_collection.update_one(
        {'_id': current_user['_id']},
        {'$set': update_fields}
    )
    
    return jsonify({'message': 'Profile updated successfully'}), 200

# ==================== Movie Routes ====================

@app.route('/api/movies', methods=['GET'])
def get_movies():
    """Get all movies with filters"""
    genre = request.args.get('genre')
    search = request.args.get('search')
    
    query = {}
    if genre:
        query['genre'] = genre
    if search:
        query['$or'] = [
            {'title': {'$regex': search, '$options': 'i'}},
            {'description': {'$regex': search, '$options': 'i'}}
        ]
    
    movies = list(movies_collection.find(query).limit(50))
    for movie in movies:
        serialize_document(movie)
    
    return jsonify({'movies': movies}), 200

@app.route('/api/movies/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get specific movie details"""
    from bson.objectid import ObjectId
    
    movie = movies_collection.find_one({'_id': ObjectId(movie_id)})
    if not movie:
        return jsonify({'message': 'Movie not found'}), 404
    
    serialize_document(movie)
    return jsonify({'movie': movie}), 200

@app.route('/api/movies', methods=['POST'])
@token_required
@admin_required
def add_movie(current_user):
    """Add new movie (Admin only)"""
    data = request.get_json()
    
    required_fields = ['title', 'genre', 'duration', 'rating', 'description', 'poster_url']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    new_movie = {
        'title': data['title'],
        'genre': data['genre'],
        'duration': data['duration'],
        'rating': float(data['rating']),
        'description': data['description'],
        'poster_url': data['poster_url'],
        'release_date': data.get('release_date'),
        'cast': data.get('cast', []),
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    result = movies_collection.insert_one(new_movie)
    
    return jsonify({
        'message': 'Movie added successfully',
        'movie_id': str(result.inserted_id)
    }), 201

# ==================== Theater Routes ====================

@app.route('/api/theaters', methods=['GET'])
def get_theaters():
    """Get all theaters"""
    theaters = list(theaters_collection.find())
    for theater in theaters:
        serialize_document(theater)
    return jsonify({'theaters': theaters}), 200

@app.route('/api/theaters', methods=['POST'])
@token_required
@admin_required
def add_theater(current_user):
    """Add new theater (Admin only)"""
    data = request.get_json()
    
    required_fields = ['name', 'city', 'address', 'screens']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    new_theater = {
        'name': data['name'],
        'city': data['city'],
        'address': data['address'],
        'screens': data['screens'],
        'total_seats': data.get('total_seats', 100),
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    result = theaters_collection.insert_one(new_theater)
    
    return jsonify({
        'message': 'Theater added successfully',
        'theater_id': str(result.inserted_id)
    }), 201

# ==================== Show Routes ====================

@app.route('/api/shows', methods=['GET'])
def get_shows():
    """Get shows for a movie and theater"""
    movie_id = request.args.get('movie_id')
    theater_id = request.args.get('theater_id')
    show_date = request.args.get('date')
    
    from bson.objectid import ObjectId
    
    query = {}
    if movie_id:
        query['movie_id'] = ObjectId(movie_id)
    if theater_id:
        query['theater_id'] = ObjectId(theater_id)
    if show_date:
        query['show_date'] = show_date
    
    shows = list(shows_collection.find(query).sort('show_time', 1))
    for show in shows:
        serialize_document(show)
    
    return jsonify({'shows': shows}), 200

@app.route('/api/shows', methods=['POST'])
@token_required
@admin_required
def add_show(current_user):
    """Add new show/screening (Admin only)"""
    data = request.get_json()
    from bson.objectid import ObjectId
    
    required_fields = ['movie_id', 'theater_id', 'show_date', 'show_time', 'price']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    new_show = {
        'movie_id': ObjectId(data['movie_id']),
        'theater_id': ObjectId(data['theater_id']),
        'show_date': data['show_date'],
        'show_time': data['show_time'],
        'price': float(data['price']),
        'language': data.get('language', 'English'),
        'format': data.get('format', '2D'),
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    result = shows_collection.insert_one(new_show)
    
    return jsonify({
        'message': 'Show added successfully',
        'show_id': str(result.inserted_id)
    }), 201

# ==================== Seat Routes ====================

@app.route('/api/seats/<show_id>', methods=['GET'])
def get_seats(show_id):
    """Get seat layout for a show"""
    from bson.objectid import ObjectId
    
    seats = list(seats_collection.find({'show_id': ObjectId(show_id)}))
    for seat in seats:
        serialize_document(seat)
    
    return jsonify({'seats': seats}), 200

@app.route('/api/seats', methods=['POST'])
@token_required
@admin_required
def initialize_seats(current_user):
    """Initialize seats for a show (Admin only)"""
    data = request.get_json()
    from bson.objectid import ObjectId
    
    show_id = data.get('show_id')
    rows = data.get('rows', 10)
    cols = data.get('cols', 10)
    
    # Delete existing seats
    seats_collection.delete_many({'show_id': ObjectId(show_id)})
    
    # Create new seats
    seats = []
    seat_number = 1
    for row in range(rows):
        for col in range(cols):
            seats.append({
                'show_id': ObjectId(show_id),
                'seat_number': seat_number,
                'row': chr(65 + row),  # A, B, C, ...
                'column': col + 1,
                'is_booked': False,
                'booked_by': None,
                'booking_id': None,
                'created_at': datetime.utcnow()
            })
            seat_number += 1
    
    seats_collection.insert_many(seats)
    
    return jsonify({
        'message': 'Seats initialized successfully',
        'total_seats': len(seats)
    }), 201

# ==================== Booking Routes ====================

@app.route('/api/bookings', methods=['POST'])
@token_required
def create_booking(current_user):
    """Create a booking"""
    data = request.get_json()
    from bson.objectid import ObjectId
    
    show_id = ObjectId(data.get('show_id'))
    seat_ids = [ObjectId(seat_id) for seat_id in data.get('seat_ids', [])]
    
    if not seat_ids:
        return jsonify({'message': 'No seats selected'}), 400
    
    # Check seat availability
    booked_seats = list(seats_collection.find({
        '_id': {'$in': seat_ids},
        'is_booked': True
    }))
    
    if booked_seats:
        return jsonify({'message': 'Some seats are already booked'}), 400
    
    # Get show details for pricing
    show = shows_collection.find_one({'_id': show_id})
    if not show:
        return jsonify({'message': 'Show not found'}), 404
    
    total_price = len(seat_ids) * show['price']
    
    # Create booking
    new_booking = {
        'user_id': current_user['_id'],
        'show_id': show_id,
        'seat_ids': seat_ids,
        'total_seats': len(seat_ids),
        'total_price': total_price,
        'status': 'pending',
        'booking_reference': f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    result = bookings_collection.insert_one(new_booking)
    
    # Update seat status
    seats_collection.update_many(
        {'_id': {'$in': seat_ids}},
        {
            '$set': {
                'is_booked': True,
                'booked_by': current_user['_id'],
                'booking_id': result.inserted_id
            }
        }
    )
    
    return jsonify({
        'message': 'Booking created successfully',
        'booking_id': str(result.inserted_id),
        'booking_reference': new_booking['booking_reference'],
        'total_price': total_price
    }), 201

@app.route('/api/bookings/<booking_id>', methods=['GET'])
@token_required
def get_booking(current_user, booking_id):
    """Get booking details"""
    from bson.objectid import ObjectId
    
    booking = bookings_collection.find_one({
        '_id': ObjectId(booking_id),
        'user_id': current_user['_id']
    })
    
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404
    
    serialize_document(booking)
    return jsonify({'booking': booking}), 200

@app.route('/api/bookings/user', methods=['GET'])
@token_required
def get_user_bookings(current_user):
    """Get all bookings for current user"""
    bookings = list(bookings_collection.find({'user_id': current_user['_id']}))
    for booking in bookings:
        serialize_document(booking)
    
    return jsonify({'bookings': bookings}), 200

@app.route('/api/bookings/<booking_id>/cancel', methods=['PUT'])
@token_required
def cancel_booking(current_user, booking_id):
    """Cancel a booking"""
    from bson.objectid import ObjectId
    
    booking = bookings_collection.find_one({
        '_id': ObjectId(booking_id),
        'user_id': current_user['_id']
    })
    
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404
    
    if booking['status'] in ['confirmed', 'cancelled']:
        return jsonify({'message': f"Cannot cancel booking with status: {booking['status']}"}), 400
    
    # Update booking status
    bookings_collection.update_one(
        {'_id': ObjectId(booking_id)},
        {'$set': {'status': 'cancelled', 'updated_at': datetime.utcnow()}}
    )
    
    # Release seats
    seats_collection.update_many(
        {'booking_id': ObjectId(booking_id)},
        {'$set': {'is_booked': False, 'booked_by': None, 'booking_id': None}}
    )
    
    return jsonify({'message': 'Booking cancelled successfully'}), 200

# ==================== Payment Routes ====================

@app.route('/api/payments', methods=['POST'])
@token_required
def process_payment(current_user):
    """Process payment (Mock payment gateway)"""
    data = request.get_json()
    from bson.objectid import ObjectId
    
    booking_id = ObjectId(data.get('booking_id'))
    
    booking = bookings_collection.find_one({
        '_id': booking_id,
        'user_id': current_user['_id']
    })
    
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404
    
    # Simulate payment validation
    if not all(key in data for key in ['card_number', 'expiry', 'cvv']):
        return jsonify({'message': 'Invalid payment details'}), 400
    
    # Create payment record
    payment = {
        'booking_id': booking_id,
        'user_id': current_user['_id'],
        'amount': booking['total_price'],
        'payment_method': data.get('payment_method', 'credit_card'),
        'status': 'completed',
        'transaction_id': f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'created_at': datetime.utcnow()
    }
    
    result = payments_collection.insert_one(payment)
    
    # Update booking status
    bookings_collection.update_one(
        {'_id': booking_id},
        {'$set': {'status': 'confirmed', 'payment_id': result.inserted_id}}
    )
    
    return jsonify({
        'message': 'Payment processed successfully',
        'transaction_id': payment['transaction_id'],
        'booking_id': str(booking_id)
    }), 200

# ==================== Admin Routes ====================

@app.route('/api/admin/bookings', methods=['GET'])
@token_required
@admin_required
def get_all_bookings(current_user):
    """Get all bookings (Admin only)"""
    bookings = list(bookings_collection.find().limit(100))
    for booking in bookings:
        serialize_document(booking)
    
    return jsonify({'bookings': bookings}), 200

@app.route('/api/admin/stats', methods=['GET'])
@token_required
@admin_required
def get_admin_stats(current_user):
    """Get admin statistics (Admin only)"""
    total_users = users_collection.count_documents({})
    total_bookings = bookings_collection.count_documents({})
    total_revenue = sum(payment['amount'] for payment in payments_collection.find({}))
    pending_bookings = bookings_collection.count_documents({'status': 'pending'})
    
    return jsonify({
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'pending_bookings': pending_bookings
    }), 200

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
