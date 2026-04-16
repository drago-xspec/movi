# Quick Start Guide - Get CineBook Running in 5 Minutes

## ⚡ Prerequisites Checklist
- [ ] Python 3.8+ installed
- [ ] MongoDB installed and running
- [ ] Text editor or IDE ready
- [ ] Modern web browser

## 🚀 Quick Setup Steps

### 1️⃣ Install Backend Dependencies
```bash
cd movie-booking-api
pip install -r requirements.txt
```

### 2️⃣ Copy Environment File
```bash
cp .env.example .env
```

### 3️⃣ Start MongoDB
```bash
# Windows
mongod

# macOS with Homebrew
brew services start mongodb-community

# Or use MongoDB Compass GUI
```

### 4️⃣ Seed Database
```bash
python seed_db.py
```

You should see:
```
✅ Inserted 10 movies
✅ Inserted 5 theaters
📊 Database seeding complete!
```

### 5️⃣ Start Flask Backend
```bash
python app.py
```

Expected output:
```
 * Running on http://127.0.0.1:5000/
 * Debug mode: on
```

### 6️⃣ Open in Browser
- **Option A**: Double-click `index.html`
- **Option B**: Use local server:
  ```bash
  # In another terminal
  python -m http.server 8000
  # Visit http://localhost:8000/index.html
  ```

---

## 🎬 Try These First!

### Test User Account
Create a test account or use these optional credentials (after manual DB setup):

```
Email: test@example.com
Password: test123
```

### Try These Features:
1. ✅ **Browse Movies** - Scroll through movie listings with posters
2. ✅ **Search & Filter** - Try searching for "Matrix" or filtering by genre
3. ✅ **Register** - Create a new account
4. ✅ **Book a Movie** - Select a movie → Choose theater → Pick seats → Pay
5. ✅ **View Bookings** - Check your booking history
6. ✅ **Admin Panel** - (Need admin role in DB)

---

## 🎭 Movie Posters Included

The database seeding script automatically adds 10 movies with **real online poster images** from TMDB/IMDb:

- The Shawshank Redemption
- The Godfather
- The Dark Knight
- Pulp Fiction
- Forrest Gump
- Inception
- The Matrix
- Interstellar
- Avengers: Endgame
- Fight Club

All poster images load from online sources!

---

## ⚙️ Configuration

### Change Flask Port
Edit `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Change 5000 to 8080
```

### Change MongoDB Host
Edit `.env`:
```env
MONGO_URI=mongodb://your-host:27017/
```

### Change Secret Key
Generate new key:
```python
import secrets
print(secrets.token_hex(32))
```

Then update `.env`:
```env
SECRET_KEY=your-new-key-here
```

---

## 📊 Database Check

### View Database in MongoDB Compass:
1. Open MongoDB Compass
2. Connect to `mongodb://localhost:27017/`
3. View database: `movie_booking_db`
4. Collections:
   - `users`
   - `movies`
   - `theaters`
   - `shows`
   - `bookings`
   - `seats`
   - `payments`

### Or use MongoDB Shell:
```bash
# Connect
mongosh

# Use database
use movie_booking_db

# View collections
show collections

# Check movies
db.movies.find().pretty()

# Count bookings
db.bookings.countDocuments()
```

---

## 🔑 Admin Setup

### Make User Admin:
1. Register a user account normally
2. Connect to MongoDB:
   ```bash
   mongosh
   use movie_booking_db
   
   # Find your user
   db.users.findOne({email: "your-email@example.com"})
   
   # Make admin
   db.users.updateOne(
       {email: "your-email@example.com"},
       {$set: {role: "admin"}}
   )
   ```
3. Login - Admin menu will appear!

---

## 🐛 Common Issues & Fixes

### ❌ "Connection refused: 127.0.0.1:27017"
**Fix**: MongoDB not running
```bash
mongod  # or use MongoDB Compass
```

### ❌ "Address already in use"
**Fix**: Port 5000 is taken
```bash
# Kill existing process and restart
python app.py
```

### ❌ "ModuleNotFoundError: No module named 'flask'"
**Fix**: Dependencies not installed
```bash
pip install -r requirements.txt
```

### ❌ Movie posters not loading
**Fix**: Normal (loading from internet). Check connection or edit URLs in database.

### ❌ "CORS error"
**Fix**: Wrong frontend URL. Should be served on `localhost:8000` or similar, not file:// protocol.

---

## 📱 Test on Mobile

### Using the same network:
```bash
# Find your computer IP
# Windows: ipconfig | findstr "IPv4"
# Mac/Linux: ifconfig | grep inet

# Access from phone:
http://YOUR_IP:8000/index.html
```

---

## 🎯 What's Included

✅ **10 Movie Listings** with real poster images  
✅ **5 Theaters** in different cities  
✅ **Seat Selection** (10x10 grid)  
✅ **Mock Payments**  
✅ **Booking Confirmation**  
✅ **Admin Panel**  
✅ **User Profiles**  
✅ **Search & Filter**  
✅ **Responsive Design**  
✅ **Complete Database**  

---

## 📚 Next Steps

1. **Customize**: Edit movies, theaters, prices in database
2. **Integrate Real Payment**: Connect Stripe or PayPal
3. **Add Email**: Send booking confirmations
4. **Deploy**: Use Heroku, PythonAnywhere, or AWS
5. **Scale**: Add more features based on requirements

---

## 💡 Learning Resources

- **Flask Docs**: https://flask.palletsprojects.com/
- **MongoDB Docs**: https://docs.mongodb.com/
- **JWT Guide**: https://jwt.io/
- **REST API Design**: https://restfulapi.net/

---

## 🎉 You're All Set!

The application is now running and ready to use. Start browsing movies, making bookings, and exploring all features!

**Questions?** Check the full `README.md` for detailed API documentation and troubleshooting.

---

**Happy Booking! 🍿🎬**
