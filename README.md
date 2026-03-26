# EduManage - Professional Student Management System

A production-ready, full-stack Student Management System built using Python (Flask), SQLite, HTML, and CSS (with Bootstrap 5 for modern UI). 
It features a robust User Authentication system seamlessly integrated with core CRUD operations, protected routes, and a premium SaaS-style developer experience.

## 🌟 Key Features
- **SaaS Dashboard UI**: A minimal, beautiful, and highly responsive user interface with floating labels, custom gradients, soft shadows, page fade-in animations, and professional card layouts.
- **Secure Authentication**: Built-in user Registration and Login using Werkzeug's `generate_password_hash` to safely encrypt credentials in the database.
- **Protected Routing**: A custom `@login_required` decorator secures the dashboard so unauthorized visitors are cleanly redirected to log in.
- **CRUD Operations**: Securely Add, View, Update, and Delete student records with SQLite.
- **Smart Search**: Quickly filter students by Name or Course.
- **Empty States**: Customized UI illustrations when no students exist or a search yields zero results.
- **Flash Notifications**: Beautiful pop-up alerts for success and error states using Font-Awesome icons.

## 📂 Project Structure

```text
Student Management System/
│
├── app.py               # The main Python backend (Flask server, Auth logic, Protected routes)
├── setup_db.py          # Script to initialize the SQLite database
├── database.db          # SQLite Database (auto-generated) containing `users` and `students` tables
├── requirements.txt     # Python dependencies list
│
├── static/
│   └── style.css        # Professional custom stylesheet enhancing Bootstrap 5 with SaaS themes
│
└── templates/
    ├── layout.html      # Base HTML template (Bootstrap CDN, Navbar, Dynamic Logged-in view)
    ├── login.html       # User Sign In interface
    ├── register.html    # User Registration interface
    ├── index.html       # Protected Home page (View all students & Search)
    ├── add.html         # Protected Form to add a new student
    └── edit.html        # Protected Form to update existing student details
```

## 🚀 Setup Instructions

Follow these step-by-step instructions to run the project on your machine.

### Prerequisites:
- Install [Python 3](https://www.python.org/downloads/) (Check "Add Python to PATH" during installation).

### Step 1: Install Dependencies
Open your terminal (or Command Prompt) inside the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 2: Initialize the Database
Before running the app, we need to generate the fresh database schema spanning `users` and `students`. Run:
```bash
python setup_db.py
```
*(You should see a success message indicating both tables were created).*

### Step 3: Run the Application
Start the Flask server by running:
```bash
python app.py
```

### Step 4: Open in your Browser
Navigate to **http://127.0.0.1:5000**.
You will immediately be prompted to register or login. Create an account, test the validations, and manage your students securely on the new dashboard!

---
*Built with Flask, SQLite, HTML5, Bootstrap 5, and Custom CSS.*
# Student-Management-System
A full-stack web application to manage student records with authentication and CRUD operations using
