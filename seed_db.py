"""
Database seed script - Populate initial data with movie posters from online sources
Run: python seed_db.py
"""

from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['movie_booking_db']

# Movie posters from online sources (using real URLs)
SAMPLE_MOVIES = [
    # Trending Movies (Current)
    {
        'title': 'Dune: Part Two',
        'genre': 'Action, Adventure, Sci-Fi',
        'duration': 166,
        'rating': 8.5,
        'description': 'Paul Atreides travels to the dangerous planet Arrakis to ensure the future of his family and people.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2FjNmVlMDctMWZkOS00ZmI5LWI4YWUtNWU3OTAxZTg3MTZlXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg',
        'release_date': '2024-02-28',
        'cast': ['Timothée Chalamet', 'Zendaya', 'Oscar Isaac'],
        'is_trending': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Godzilla x Kong: The New Empire',
        'genre': 'Action, Adventure, Sci-Fi',
        'duration': 115,
        'rating': 8.2,
        'description': 'The fearsome Godzilla and the mighty Kong face off in an epic battle as humanity looks to wipe out both creatures.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNjAwNzc3ZTktOTU1My00MDU2LWJhM2ItN2ZjZTViZjAxMjZjXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_SX300.jpg',
        'release_date': '2024-03-29',
        'cast': ['Rebecca Hall', 'Brian Tyree Henry'],
        'is_trending': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Inside Out 2',
        'genre': 'Animation, Adventure, Comedy',
        'duration': 96,
        'rating': 8.8,
        'description': 'Teenager Riley\'s emotions return when new emotions like Anxiety appear to complicate her life.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYTBzYjY2ZGItZjU3My00YjZkLWJhNzAtOThhMzQ0YWY3NTc3XkEyXkFqcGdeQXVyMDEyMDcwNQ@@._V1_SX300.jpg',
        'release_date': '2024-06-14',
        'cast': ['Amy Poehler', 'Phyllis Smith'],
        'is_trending': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Deadpool & Wolverine',
        'genre': 'Action, Adventure, Comedy',
        'duration': 128,
        'rating': 8.3,
        'description': 'Deadpool and Wolverine team up for a wild adventure across the multiverse.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BOTMyZjYyNjktZDAxZC00YWY4LThjMDItZjNmZDk3MzFjYzljXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_SX300.jpg',
        'release_date': '2024-07-26',
        'cast': ['Ryan Reynolds', 'Hugh Jackman'],
        'is_trending': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Trap',
        'genre': 'Drama, Mystery, Thriller',
        'duration': 104,
        'rating': 7.8,
        'description': 'A father and son go to a concert only to discover there is a police trap waiting for a killer.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYzk5YWZmOTItYWY1OC00MzFjLWFkM2ItOGY4ZWEwYjQ3ODVjXkEyXkFqcGdeQXVyMTQ3Mzc4NjI@._V1_SX300.jpg',
        'release_date': '2024-08-02',
        'cast': ['Josh Hartnett', 'Ariel Shaffir'],
        'is_trending': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'A Quiet Place: Day One',
        'genre': 'Action, Drama, Horror',
        'duration': 99,
        'rating': 8.1,
        'description': 'As New York is invaded by silent aliens, a woman and her son attempt to survive.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BZWIyOWVmNjUtNzViOS00NmZjLTk1MDItMDgzZTc1OTk0NTExXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_SX300.jpg',
        'release_date': '2024-06-28',
        'cast': ['Lupita Nyong\'o', 'Joseph Quinn'],
        'is_trending': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Joker: Folie à Deux',
        'genre': 'Crime, Drama, Musical',
        'duration': 138,
        'rating': 7.9,
        'description': 'Arthur Fleck meets Lady Gaga as Harley Quinn in this dark musical thriller.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BY2I0ZDhkNGMtMjBjMS00ZDc5LWFjNjItYWY3NzI5ZDYwNGZjXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_SX300.jpg',
        'release_date': '2024-10-04',
        'cast': ['Joaquin Phoenix', 'Lady Gaga'],
        'is_trending': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Wicked',
        'genre': 'Adventure, Fantasy, Musical',
        'duration': 160,
        'rating': 8.0,
        'description': 'The untold story of the Witches of the West as two girls form an unlikely friendship.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNTZjYzM4MjMtOWM3OC00ZDc0LWIzNDctZWVkZTIzZGUyNDA4XkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_SX300.jpg',
        'release_date': '2024-11-22',
        'cast': ['Cynthia Erivo', 'Ariana Grande'],
        'is_trending': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Mufasa: The Lion King',
        'genre': 'Animation, Adventure, Drama',
        'duration': 118,
        'rating': 8.2,
        'description': 'The story of how Mufasa became the king of Pride Rock.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BMDMxNzYzNzctMDNlZi00YWU4LWI2MzAtNjY0YjUwMzQ4NjI5XkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_SX300.jpg',
        'release_date': '2024-12-20',
        'cast': ['Aaron Pierre', 'Kelvin Harrison Jr.'],
        'is_trending': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Sonic 3',
        'genre': 'Action, Adventure, Comedy',
        'duration': 104,
        'rating': 7.7,
        'description': 'Sonic faces Shadow, a powerful new adversary, in an epic showdown.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BOTJlYzAzZTUtOGJlOS00ODljLWE2NDItODMxOTgyMTQzYTk5XkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_SX300.jpg',
        'release_date': '2024-12-20',
        'cast': ['Ben Schwartz', 'Keanu Reeves'],
        'is_trending': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    
    # Trending Classics
    {
        'title': 'The Shawshank Redemption',
        'genre': 'Drama',
        'duration': 142,
        'rating': 9.3,
        'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BMDFlYTk0NjItMDhhYjgtZTcwYS00MjE0LTk0YjctMmFhMGQyNjZkNDRjXkEyXkFqcGdeQXVyNjgzNzU4NjA@._V1_SX300.jpg',
        'release_date': '1994-10-14',
        'cast': ['Tim Robbins', 'Morgan Freeman'],
        'is_trending': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'The Godfather',
        'genre': 'Crime, Drama',
        'duration': 175,
        'rating': 9.2,
        'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant youngest son.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTIwZC00ODE0LTg4YjItODJjN2FkNWI1MzAwXkEyXkFqcGdeQXVyNzc4ODAxOA@@._V1_SX300.jpg',
        'release_date': '1972-03-24',
        'cast': ['Marlon Brando', 'Al Pacino'],
        'is_trending': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'The Dark Knight',
        'genre': 'Action, Crime, Drama',
        'duration': 152,
        'rating': 9.0,
        'description': 'When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest tests.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg',
        'release_date': '2008-07-18',
        'cast': ['Christian Bale', 'Heath Ledger'],
        'is_trending': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Pulp Fiction',
        'genre': 'Crime, Drama',
        'duration': 154,
        'rating': 8.9,
        'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItMDJmMThiMGVmNzFmXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
        'release_date': '1994-10-14',
        'cast': ['John Travolta', 'Samuel L. Jackson'],
        'is_trending': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Forrest Gump',
        'genre': 'Drama, Romance',
        'duration': 142,
        'rating': 8.8,
        'description': 'The presidencies of Kennedy and Johnson, the Vietnam War, and the Watergate scandal unfold from the perspective of an Alabama man.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNWIwODRlMTEtMzA3Mi00NTg4LTkzY2UtNjJlYjE1NjczZjE3XkEyXkFqcGdeQXVyNjc1NzM4NzQ@._V1_SX300.jpg',
        'release_date': '1994-07-06',
        'cast': ['Tom Hanks', 'Gary Sinise'],
        'is_trending': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Inception',
        'genre': 'Action, Adventure, Sci-Fi',
        'duration': 148,
        'rating': 8.8,
        'description': 'A skilled thief must plant an idea into the mind of a C.E.O. while his consciousness is vulnerable during a dream.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjExMjkwNTQ0Nl5BMl5BanBnXkFtZTcwOTk1MjU0OQ@@._V1_SX300.jpg',
        'release_date': '2010-07-16',
        'cast': ['Leonardo DiCaprio', 'Marion Cotillard'],
        'is_trending': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'The Matrix',
        'genre': 'Action, Sci-Fi',
        'duration': 136,
        'rating': 8.7,
        'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDl2OTg1OWVhZTMyXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
        'release_date': '1999-03-31',
        'cast': ['Keanu Reeves', 'Laurence Fishburne'],
        'is_trending': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Interstellar',
        'genre': 'Adventure, Drama, Sci-Fi',
        'duration': 169,
        'rating': 8.6,
        'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDAtMmE0Yi00ZDJmLTg5ZDItZjFjNzMzMzEwZTZhXkEyXkFqcGdeQXVyMzQ0MjM5NjM@._V1_SX300.jpg',
        'release_date': '2014-11-07',
        'cast': ['Matthew McConaughey', 'Anne Hathaway'],
        'is_trending': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Avengers: Endgame',
        'genre': 'Action, Adventure, Drama',
        'duration': 181,
        'rating': 8.4,
        'description': 'After the devastating events, the Avengers assemble once more to reverse Thanos\' actions and restore balance.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2AwDE._V1_SX300.jpg',
        'release_date': '2019-04-26',
        'cast': ['Robert Downey Jr.', 'Chris Evans'],
        'is_trending': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Fight Club',
        'genre': 'Drama',
        'duration': 139,
        'rating': 8.8,
        'description': 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into much more.',
        'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjJmYTZkY2UtMzYyZS00MzM1LTg4ZjItZjkwY2NiOTc1NzA3XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
        'release_date': '1999-10-15',
        'cast': ['Brad Pitt', 'Edward Norton'],
        'is_trending': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
]

SAMPLE_THEATERS = [
    {
        'name': 'PVR Cinemas - Downtown',
        'city': 'Mumbai',
        'address': '123 Marine Drive, Mumbai',
        'screens': 8,
        'total_seats': 100,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'name': 'INOX Plaza',
        'city': 'Delhi',
        'address': '456 Connaught Place, Delhi',
        'screens': 6,
        'total_seats': 95,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'name': 'Cinepolis Grand',
        'city': 'Bangalore',
        'address': '789 M.G. Road, Bangalore',
        'screens': 10,
        'total_seats': 100,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'name': 'Star Cinema',
        'city': 'Hyderabad',
        'address': '321 Hi-Tech City, Hyderabad',
        'screens': 7,
        'total_seats': 90,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'name': 'Raj Cinema Complex',
        'city': 'Pune',
        'address': '654 Baner Road, Pune',
        'screens': 5,
        'total_seats': 80,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
]

def seed_database():
    """Clear and populate database with sample data"""
    try:
        print("🗑️  Clearing existing collections...")
        db['movies'].delete_many({})
        db['theaters'].delete_many({})
        db['shows'].delete_many({})
        db['seats'].delete_many({})
        db['bookings'].delete_many({})
        db['payments'].delete_many({})
        
        print("📽️  Adding sample movies...")
        movies = db['movies'].insert_many(SAMPLE_MOVIES)
        print(f"✅ Inserted {len(movies.inserted_ids)} trending movies")
        
        print("🏢 Adding sample theaters...")
        theaters = db['theaters'].insert_many(SAMPLE_THEATERS)
        print(f"✅ Inserted {len(theaters.inserted_ids)} theaters")
        
        print("\n🎟️  Initializing seats for shows...")
        # Create sample shows and initialize seats
        init_sample_shows_and_seats(movies.inserted_ids, theaters.inserted_ids)
        
        print("\n📊 Database seeding complete!")
        print(f"   - Movies: {db['movies'].count_documents({})}")
        print(f"   - Theaters: {db['theaters'].count_documents({})}")
        print(f"   - Shows: {db['shows'].count_documents({})}")
        print(f"   - Seats: {db['seats'].count_documents({})}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")

def init_sample_shows_and_seats(movie_ids, theater_ids):
    """Create sample shows and initialize seats with different types"""
    tomorrow = datetime.utcnow() + timedelta(days=1)
    
    shows_data = [
        {'time': '09:30', 'price': 150, 'language': 'English', 'format': '2D'},
        {'time': '12:30', 'price': 180, 'language': 'English', 'format': '3D'},
        {'time': '15:30', 'price': 180, 'language': 'Hindi', 'format': '2D'},
        {'time': '18:30', 'price': 250, 'language': 'English', 'format': 'IMAX'},
        {'time': '21:30', 'price': 250, 'language': 'English', 'format': '2D'},
    ]
    
    for movie_id in movie_ids[:5]:  # Create 5 shows per movie
        for show_info in shows_data[:3]:  # 3 shows per day
            show = {
                'movie_id': movie_id,
                'theater_id': theater_ids[0],
                'show_date': tomorrow.strftime('%Y-%m-%d'),
                'show_time': show_info['time'],
                'price': show_info['price'],
                'language': show_info['language'],
                'format': show_info['format'],
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            result = db['shows'].insert_one(show)
            
            # Initialize seats with different types
            create_seats_with_types(result.inserted_id)

def create_seats_with_types(show_id):
    """Create seats with different types: Single, Couple (2))
    , Family (4 seats)"""
    seats = []
    seat_number = 1
    
    # Layout: 12 rows, 12 columns
    rows = 12
    cols = 12
    
    for row in range(rows):
        for col in range(cols):
            row_letter = chr(65 + row)  # A, B, C, ...
            
            # Determine seat type based on position
            if (row % 2 == 0 and col % 3 == 0):  # Family seats (4 together)
                seat_type = 'family'
                capacity = 4
                price_multiplier = 1.8
            elif (col % 2 == 1):  # Couple seats (2 together)
                seat_type = 'couple'
                capacity = 2
                price_multiplier = 1.3
            else:  # Single seats
                seat_type = 'single'
                capacity = 1
                price_multiplier = 1.0
            
            # Random booking for realism (70% available)
            is_booked = seat_number % 10 > 7  # 30% booked
            
            seats.append({
                'show_id': show_id,
                'seat_number': seat_number,
                'row': row_letter,
                'column': col + 1,
                'seat_type': seat_type,  # 'single', 'couple', 'family'
                'capacity': capacity,
                'price_multiplier': price_multiplier,
                'is_booked': is_booked,
                'booked_by': None,
                'booking_id': None,
                'created_at': datetime.utcnow()
            })
            seat_number += 1
    
    db['seats'].insert_many(seats)
    print(f"   ✅ Created {len(seats)} seats for show {show_id} with mixed types")

if __name__ == '__main__':
    seed_database()
