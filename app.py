import functools
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Secret key is needed to use flash messages and session cookies securely
app.secret_key = "super_secret_student_management_key_v2"

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    # Row factory allows us to access columns by name (like dictionaries)
    conn.row_factory = sqlite3.Row
    return conn

# --- Authentication functionality ---

@app.before_request
def load_logged_in_user():
    """Load user before each request if logged in."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        conn = get_db_connection()
        g.user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()

def login_required(view):
    """Decorator to require login for a specific route."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/register', methods=('GET', 'POST'))
def register():
    """User registration route."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        error = None
        
        if not username or not email or not password:
            error = 'All fields are required.'
        else:
            try:
                # Hash the password for security
                conn.execute(
                    'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                    (username, email, generate_password_hash(password))
                )
                conn.commit()
            except sqlite3.IntegrityError:
                error = f"User {username} or email {email} is already registered."
        
        conn.close()
        
        if error is None:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        flash(error, 'error')
        
    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    """User login route."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        conn.close()
        
        error = None
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('index'))
            
        flash(error, 'error')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout route."""
    session.clear()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('login'))

# --- Protected Routes ---

@app.route('/')
@login_required
def index():
    """View all students & handle search"""
    conn = get_db_connection()
    search_query = request.args.get('search', '')
    
    # If search query exists, filter by name or course
    if search_query:
        students = conn.execute(
            'SELECT * FROM students WHERE name LIKE ? OR course LIKE ?', 
            (f'%{search_query}%', f'%{search_query}%')
        ).fetchall()
    else:
        # Retrieve all students if no search
        students = conn.execute('SELECT * FROM students').fetchall()
        
    conn.close()
    return render_template('index.html', students=students, search_query=search_query)

@app.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Add a new student to the database"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        phone = request.form['phone']
        
        if not name or not email or not course or not phone:
            flash('All fields are required!', 'error')
        else:
            conn = get_db_connection()
            try:
                conn.execute(
                    'INSERT INTO students (name, email, course, phone) VALUES (?, ?, ?, ?)',
                    (name, email, course, phone)
                )
                conn.commit()
                flash('Student added successfully!', 'success')
                return redirect(url_for('index'))
            except sqlite3.IntegrityError:
                flash('Email already exists. Please use a different email.', 'error')
            finally:
                conn.close()
                
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    """Update an existing student's details"""
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    
    if student is None:
        flash('Student not found!', 'error')
        conn.close()
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        phone = request.form['phone']
        
        if not name or not email or not course or not phone:
            flash('All fields are required!', 'error')
        else:
            try:
                conn.execute(
                    'UPDATE students SET name = ?, email = ?, course = ?, phone = ? WHERE id = ?',
                    (name, email, course, phone, id)
                )
                conn.commit()
                flash('Student updated successfully!', 'success')
                return redirect(url_for('index'))
            except sqlite3.IntegrityError:
                flash('Email already exists relative to another user.', 'error')
            finally:
                conn.close()
                
    conn.close()
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    """Delete a student from the database"""
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
