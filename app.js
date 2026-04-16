// ==================== API Configuration ====================
const API_BASE_URL = 'http://localhost:5000/api';
let authToken = localStorage.getItem('authToken') || null;
let currentUser = JSON.parse(localStorage.getItem('currentUser')) || null;

// ==================== User Management ====================
function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            authToken = data.token;
            currentUser = data.user;
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            updateUIAfterLogin();
            closeModal('loginModal');
            showNotification('Login successful!', 'success');
        } else {
            showNotification(data.message || 'Login failed', 'error');
        }
    })
    .catch(error => {
        console.error('Login error:', error);
        showNotification('Login error', 'error');
    });
}

function handleRegister(event) {
    event.preventDefault();
    
    const full_name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const phone = document.getElementById('registerPhone').value;
    
    fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ full_name, email, password, phone })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            authToken = data.token;
            currentUser = data.user;
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            updateUIAfterLogin();
            closeModal('registerModal');
            showNotification('Registration successful!', 'success');
        } else {
            showNotification(data.message || 'Registration failed', 'error');
        }
    })
    .catch(error => {
        console.error('Registration error:', error);
        showNotification('Registration error', 'error');
    });
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    updateUIAfterLogout();
    showNotification('Logged out successfully', 'success');
}

function updateUIAfterLogin() {
    document.getElementById('userNav').style.display = 'flex';
    document.getElementById('guestNav').style.display = 'none';
    
    if (currentUser.role === 'admin') {
        document.getElementById('adminNav').style.display = 'flex';
    }
}

function updateUIAfterLogout() {
    document.getElementById('userNav').style.display = 'none';
    document.getElementById('adminNav').style.display = 'none';
    document.getElementById('guestNav').style.display = 'flex';
}

function updateProfile(event) {
    event.preventDefault();
    
    const full_name = document.getElementById('profileName').value;
    const phone = document.getElementById('profilePhone').value;
    
    fetch(`${API_BASE_URL}/auth/profile`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({ full_name, phone })
    })
    .then(response => response.json())
    .then(data => {
        showNotification(data.message, 'success');
        closeModal('profileModal');
    })
    .catch(error => console.error('Error:', error));
}

// ==================== Movie Management ====================
let allMovies = [];
let filteredMovies = [];

function loadMovies() {
    fetch(`${API_BASE_URL}/movies`)
        .then(response => response.json())
        .then(data => {
            allMovies = data.movies;
            filteredMovies = allMovies;
            
            // Separate trending and non-trending movies
            const trendingMovies = allMovies.filter(m => m.is_trending);
            const regularMovies = allMovies.filter(m => !m.is_trending);
            
            // Display trending section if exists
            if (trendingMovies.length > 0) {
                displayTrendingMovies(trendingMovies);
            }
            
            // Display all movies in main section
            displayMovies();
        })
        .catch(error => console.error('Error loading movies:', error));
}

function displayTrendingMovies(movies) {
    const grid = document.getElementById('trendingMoviesGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    movies.slice(0, 8).forEach(movie => {  // Show first 8 trending
        const card = createMovieCard(movie);
        grid.appendChild(card);
    });
}

function createMovieCard(movie) {
    const card = document.createElement('div');
    card.className = 'movie-card';
    const trendingBadge = movie.is_trending ? '<span class="trending-badge">🔥 Trending</span>' : '';
    card.innerHTML = `
        ${trendingBadge}
        <div class="movie-poster">
            <img src="${movie.poster_url}" alt="${movie.title}" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 300 400%22><rect fill=%22%23333%22 width=%22300%22 height=%22400%22/><text x=%2250%25%22 y=%2250%25%22 font-size=%2224%22 fill=%22white%22 text-anchor=%22middle%22>No Image</text></svg>'">
        </div>
        <div class="movie-card-info">
            <div class="movie-title">${movie.title}</div>
            <div class="movie-meta">
                <span class="badge">${movie.genre.split(',')[0]}</span>
                <span class="rating">⭐ ${movie.rating}</span>
            </div>
            <div class="movie-duration">⏱️ ${movie.duration} min</div>
            <button class="btn-book" onclick="showMovieDetail('${movie.id}')">Book Now</button>
        </div>
    `;
    return card;
}

function displayMovies() {
    const grid = document.getElementById('moviesGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    filteredMovies.forEach(movie => {
        const card = createMovieCard(movie);
        grid.appendChild(card);
    });
}

function filterMovies() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const genre = document.getElementById('genreFilter').value;
    
    filteredMovies = allMovies.filter(movie => {
        const matchesSearch = movie.title.toLowerCase().includes(searchTerm) || 
                            movie.description.toLowerCase().includes(searchTerm);
        const matchesGenre = !genre || movie.genre.includes(genre);
        return matchesSearch && matchesGenre;
    });
    
    displayMovies();
}

function showMovieDetail(movieId) {
    const movie = allMovies.find(m => m.id === movieId);
    if (!movie) return;
    
    if (!authToken) {
        showNotification('Please login first', 'warning');
        showModal('loginModal');
        return;
    }
    
    document.getElementById('detailPoster').src = movie.poster_url;
    document.getElementById('detailTitle').textContent = movie.title;
    document.getElementById('detailGenre').textContent = movie.genre;
    document.getElementById('detailRating').textContent = `⭐ ${movie.rating}`;
    document.getElementById('detailDescription').textContent = movie.description;
    document.getElementById('detailDuration').textContent = `${movie.duration} minutes`;
    document.getElementById('detailCast').textContent = movie.cast.join(', ');
    document.getElementById('detailReleaseDate').textContent = movie.release_date;
    
    // Load theaters
    loadTheatersForMovie(movieId);
    
    currentMovie = movie;
    showModal('movieDetailModal');
}

let currentMovie = null;
let currentTheater = null;
let currentShow = null;
let selectedSeats = [];

function loadTheatersForMovie(movieId) {
    fetch(`${API_BASE_URL}/theaters`)
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('theatreSelect');
            select.innerHTML = '<option value="">Choose a Theater</option>';
            data.theaters.forEach(theater => {
                const option = document.createElement('option');
                option.value = theater.id;
                option.textContent = `${theater.name} - ${theater.city}`;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading theaters:', error));
}

function loadShows() {
    const theaterId = document.getElementById('theatreSelect').value;
    if (!theaterId) return;
    
    currentTheater = theaterId;
    
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const dateStr = tomorrow.toISOString().split('T')[0];
    
    fetch(`${API_BASE_URL}/shows?movie_id=${currentMovie.id}&theater_id=${theaterId}&date=${dateStr}`)
        .then(response => response.json())
        .then(data => {
            const grid = document.getElementById('showsGrid');
            grid.innerHTML = '';
            
            if (data.shows.length === 0) {
                grid.innerHTML = '<p style="color: #666;">No shows available</p>';
                return;
            }
            
            data.shows.forEach(show => {
                const slot = document.createElement('button');
                slot.className = 'show-slot';
                slot.textContent = show.show_time;
                slot.onclick = () => selectShow(show, slot);
                grid.appendChild(slot);
            });
        })
        .catch(error => console.error('Error loading shows:', error));
}

function selectShow(show, element) {
    document.querySelectorAll('.show-slot').forEach(slot => slot.classList.remove('selected'));
    element.classList.add('selected');
    currentShow = show;
}

function proceedToPayment() {
    if (!currentShow) {
        showNotification('Please select a show', 'warning');
        return;
    }
    
    if (selectedSeats.length === 0) {
        showNotification('Please select seats', 'warning');
        return;
    }
    
    closeModal('seatSelectionModal');
    
    // Create booking
    const seatIds = selectedSeats.map(s => s.id);
    
    fetch(`${API_BASE_URL}/bookings`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
            show_id: currentShow.id,
            seat_ids: seatIds
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.booking_id) {
            currentBooking = data;
            showPaymentForm(data.total_price);
        } else {
            showNotification(data.message || 'Booking failed', 'error');
        }
    })
    .catch(error => {
        console.error('Error creating booking:', error);
        showNotification('Error creating booking', 'error');
    });
}

function loadSeats() {
    if (!currentShow) return;
    
    fetch(`${API_BASE_URL}/seats/${currentShow.id}`)
        .then(response => response.json())
        .then(data => {
            const grid = document.getElementById('seatsGrid');
            grid.innerHTML = '';
            selectedSeats = [];
            
            if (data.seats.length === 0) {
                grid.innerHTML = '<p style="color: #666;">No seats available</p>';
                return;
            }
            
            // Calculate seat availability
            calculateSeatAvailability(data.seats);
            
            data.seats.forEach(seat => {
                const seatEl = document.createElement('div');
                const seatClasses = ['seat'];
                
                // Add seat type class
                seatClasses.push(`seat-${seat.seat_type || 'single'}`);
                
                if (seat.is_booked) {
                    seatClasses.push('seat-booked');
                } else {
                    seatClasses.push('seat-available');
                }
                
                seatEl.className = seatClasses.join(' ');
                seatEl.textContent = `${seat.row}${seat.column}`;
                seatEl.title = `${seat.seat_type} - ${seat.row}${seat.column}`;
                
                if (!seat.is_booked) {
                    seatEl.onclick = () => toggleSeat(seatEl, seat);
                } else {
                    seatEl.style.cursor = 'not-allowed';
                }
                
                grid.appendChild(seatEl);
            });
        })
        .catch(error => console.error('Error loading seats:', error));
}

function calculateSeatAvailability(seats) {
    let singleCount = 0, coupleCount = 0, familyCount = 0;
    
    seats.forEach(seat => {
        if (!seat.is_booked) {
            if (seat.seat_type === 'single') singleCount++;
            else if (seat.seat_type === 'couple') coupleCount++;
            else if (seat.seat_type === 'family') familyCount++;
        }
    });
    
    document.getElementById('singleSeatsCount').textContent = singleCount;
    document.getElementById('coupleSeatsCount').textContent = coupleCount;
    document.getElementById('familySeatsCount').textContent = familyCount;
}

function toggleSeat(element, seat) {
    if (element.classList.contains('seat-selected')) {
        element.classList.remove('seat-selected');
        selectedSeats = selectedSeats.filter(s => s.id !== seat.id);
    } else {
        element.classList.add('seat-selected');
        selectedSeats.push(seat);
    }
    
    updateBookingSummary();
}

function updateBookingSummary() {
    const seatsText = selectedSeats.map(s => {
        const type = s.seat_type === 'couple' ? '(2)' : (s.seat_type === 'family' ? '(4)' : '');
        return `${s.row}${s.column}${type}`;
    }).join(', ');
    document.getElementById('selectedSeatsDisplay').textContent = seatsText || 'None';
    
    // Calculate total price based on seat types
    let totalPrice = 0;
    selectedSeats.forEach(seat => {
        const basePrice = currentShow?.price || 0;
        const multiplier = seat.price_multiplier || 1.0;
        totalPrice += basePrice * multiplier;
    });
    
    document.getElementById('totalAmountDisplay').textContent = `₹${totalPrice}`;
}

let currentBooking = null;

function showPaymentForm(amount) {
    document.getElementById('paymentAmountDisplay').textContent = `₹${amount}`;
    showModal('paymentModal');
}

function processPayment(event) {
    event.preventDefault();
    
    const cardNumber = document.getElementById('cardNumber').value;
    const expiry = document.getElementById('expiry').value;
    const cvv = document.getElementById('cvv').value;
    
    fetch(`${API_BASE_URL}/payments`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
            booking_id: currentBooking.booking_id,
            card_number: cardNumber,
            expiry: expiry,
            cvv: cvv,
            payment_method: 'credit_card'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.transaction_id) {
            showConfirmation();
            closeModal('paymentModal');
        } else {
            showNotification(data.message || 'Payment failed', 'error');
        }
    })
    .catch(error => {
        console.error('Payment error:', error);
        showNotification('Payment error', 'error');
    });
}

function showConfirmation() {
    document.getElementById('bookingReference').textContent = currentBooking.booking_reference;
    document.getElementById('confirmationMovie').textContent = currentMovie.title;
    document.getElementById('confirmationTheater').textContent = currentTheater; // Should fetch theater name
    document.getElementById('confirmationTime').textContent = currentShow.show_time;
    document.getElementById('confirmationSeats').textContent = selectedSeats.map(s => `${s.row}${s.column}`).join(', ');
    document.getElementById('confirmationAmount').textContent = `₹${currentBooking.total_price}`;
    
    showModal('confirmationModal');
}

function loadUserBookings() {
    if (!authToken) return;
    
    fetch(`${API_BASE_URL}/bookings/user`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
    })
    .then(response => response.json())
    .then(data => {
        const list = document.getElementById('bookingsList');
        list.innerHTML = '';
        
        if (data.bookings.length === 0) {
            list.innerHTML = '<p style="color: #666;">No bookings found</p>';
            return;
        }
        
        data.bookings.forEach(booking => {
            const card = document.createElement('div');
            card.className = 'booking-card';
            const statusClass = `status-${booking.status}`;
            card.innerHTML = `
                <div class="booking-header">
                    <div class="booking-ref">${booking.booking_reference}</div>
                    <span class="booking-status ${statusClass}">${booking.status.toUpperCase()}</span>
                </div>
                <div class="booking-details">
                    <div class="booking-detail-item">
                        <strong>Show Time:</strong>
                        <span>${booking.show_time}</span>
                    </div>
                    <div class="booking-detail-item">
                        <strong>Seats:</strong>
                        <span>${booking.total_seats} seats</span>
                    </div>
                    <div class="booking-detail-item">
                        <strong>Amount:</strong>
                        <span>₹${booking.total_price}</span>
                    </div>
                    <div class="booking-detail-item">
                        <strong>Booked On:</strong>
                        <span>${new Date(booking.created_at).toLocaleDateString()}</span>
                    </div>
                </div>
                <div class="booking-actions">
                    ${booking.status === 'pending' ? `<button class="btn-cancel" onclick="cancelBooking('${booking.id}')">Cancel Booking</button>` : ''}
                </div>
            `;
            list.appendChild(card);
        });
    })
    .catch(error => console.error('Error loading bookings:', error));
}

function cancelBooking(bookingId) {
    if (!confirm('Are you sure you want to cancel this booking?')) return;
    
    fetch(`${API_BASE_URL}/bookings/${bookingId}/cancel`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${authToken}` }
    })
    .then(response => response.json())
    .then(data => {
        showNotification(data.message, 'success');
        loadUserBookings();
    })
    .catch(error => console.error('Error:', error));
}

// ==================== Admin Functions ====================
function loadAdminStats() {
    fetch(`${API_BASE_URL}/admin/stats`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('statsUsers').textContent = data.total_users;
        document.getElementById('statsBookings').textContent = data.total_bookings;
        document.getElementById('statsRevenue').textContent = `₹${data.total_revenue}`;
        document.getElementById('statsPending').textContent = data.pending_bookings;
    })
    .catch(error => console.error('Error:', error));
}

function addMovie(event) {
    event.preventDefault();
    
    const movie = {
        title: document.getElementById('addMovieTitle').value,
        genre: document.getElementById('addMovieGenre').value,
        duration: parseInt(document.getElementById('addMovieDuration').value),
        rating: parseFloat(document.getElementById('addMovieRating').value),
        description: document.getElementById('addMovieDescription').value,
        poster_url: document.getElementById('addMoviePoster').value
    };
    
    fetch(`${API_BASE_URL}/movies`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(movie)
    })
    .then(response => response.json())
    .then(data => {
        showNotification('Movie added successfully', 'success');
        event.target.reset();
        loadMovies();
    })
    .catch(error => console.error('Error:', error));
}

function addTheater(event) {
    event.preventDefault();
    
    const theater = {
        name: document.getElementById('addTheaterName').value,
        city: document.getElementById('addTheaterCity').value,
        address: document.getElementById('addTheaterAddress').value,
        screens: parseInt(document.getElementById('addTheaterScreens').value),
        total_seats: parseInt(document.getElementById('addTheaterSeats').value)
    };
    
    fetch(`${API_BASE_URL}/theaters`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(theater)
    })
    .then(response => response.json())
    .then(data => {
        showNotification('Theater added successfully', 'success');
        event.target.reset();
    })
    .catch(error => console.error('Error:', error));
}

function addShow(event) {
    event.preventDefault();
    
    const show = {
        movie_id: document.getElementById('addShowMovie').value,
        theater_id: document.getElementById('addShowTheater').value,
        show_date: document.getElementById('addShowDate').value,
        show_time: document.getElementById('addShowTime').value,
        price: parseFloat(document.getElementById('addShowPrice').value),
        language: document.getElementById('addShowLanguage').value,
        format: document.getElementById('addShowFormat').value
    };
    
    fetch(`${API_BASE_URL}/shows`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(show)
    })
    .then(response => response.json())
    .then(data => {
        if (data.show_id) {
            // Initialize seats
            fetch(`${API_BASE_URL}/seats`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify({
                    show_id: data.show_id,
                    rows: 10,
                    cols: 10
                })
            });
        }
        showNotification('Show added successfully', 'success');
        event.target.reset();
    })
    .catch(error => console.error('Error:', error));
}

// ==================== UI Helpers ====================
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add('show');
    
    // Load specific content when modal opens
    if (modalId === 'bookingsModal') {
        loadUserBookings();
    } else if (modalId === 'adminModal') {
        loadAdminStats();
        populateAdminSelects();
    } else if (modalId === 'profileModal') {
        document.getElementById('profileName').value = currentUser.full_name;
        document.getElementById('profileEmail').value = currentUser.email;
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('show');
}

function switchModal(closeId, openId) {
    closeModal(closeId);
    showModal(openId);
}

function switchAdminTab(tabName) {
    document.querySelectorAll('.admin-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.admin-tab-content').forEach(content => content.classList.remove('active'));
    
    event.target.classList.add('active');
    document.getElementById(tabName + 'Tab').classList.add('active');
}

function showNotification(message, type = 'info') {
    // Simple notification (you can enhance this)
    alert(`[${type.toUpperCase()}] ${message}`);
}

function scrollToMovies() {
    document.getElementById('movies').scrollIntoView({ behavior: 'smooth' });
}

function goHome() {
    closeModal('confirmationModal');
    location.reload();
}

function populateAdminSelects() {
    // Populate movie select
    fetch(`${API_BASE_URL}/movies`)
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('addShowMovie');
            select.innerHTML = '<option value="">Select Movie</option>';
            data.movies.forEach(movie => {
                const option = document.createElement('option');
                option.value = movie.id;
                option.textContent = movie.title;
                select.appendChild(option);
            });
        });
    
    // Populate theater select
    fetch(`${API_BASE_URL}/theaters`)
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('addShowTheater');
            select.innerHTML = '<option value="">Select Theater</option>';
            data.theaters.forEach(theater => {
                const option = document.createElement('option');
                option.value = theater.id;
                option.textContent = `${theater.name} - ${theater.city}`;
                select.appendChild(option);
            });
        });
}

// ==================== Event Listeners ====================
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    if (authToken && currentUser) {
        updateUIAfterLogin();
    }
    
    // Load movies on page load
    loadMovies();
    
    // Close modals on outside click
    window.onclick = function(event) {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.classList.remove('show');
            }
        });
    };
    
    // Update seat display when show is selected
    const movieDetailModal = document.getElementById('movieDetailModal');
    const observer = new MutationObserver(() => {
        if (movieDetailModal.classList.contains('show')) {
            // Show is selected, now load seat selection
            if (currentShow && !document.getElementById('seatSelectionModal').classList.contains('show')) {
                // Automatically show seat selection
            }
        }
    });
    
    // Navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            if (e.target.getAttribute('href') === '#bookings') {
                e.preventDefault();
                showModal('bookingsModal');
            } else if (e.target.getAttribute('href') === '#profile') {
                e.preventDefault();
                showModal('profileModal');
            } else if (e.target.getAttribute('href') === '#admin') {
                e.preventDefault();
                showModal('adminModal');
            }
        });
    });
});

// When proceeding to seat selection from movie detail
document.addEventListener('click', function(e) {
    if (e.target && e.target.textContent === 'Book Now') {
        // Movie card book button - handled by onclick
    }
});

// Override the shows grid click to show seat selection
const originalProceedToSeatSelection = function() {
    if (currentShow) {
        closeModal('movieDetailModal');
        loadSeats();
        showModal('seatSelectionModal');
    }
};

// Hook into show selection
document.addEventListener('click', function(e) {
    if (e.target && e.target.classList.contains('show-slot')) {
        setTimeout(() => {
            originalProceedToSeatSelection();
        }, 300);
    }
});
