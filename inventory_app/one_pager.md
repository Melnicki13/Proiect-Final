Inventory Management System
Description

This is a Flask-based web application for managing company inventory. The system allows administrators to add, delete, and manage inventory items, while regular users can view and assign items to themselves.
Features

    User authentication (Admin and Regular users)
    Inventory management (Add, Delete, View items)
    Item assignment system
    Search functionality
    Responsive design

Prerequisites

    Python 3.x
    pip (Python package installer)

Project Structure

    
inventory_app/
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
    
│   ├── base.html

│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── inventory.html
│   └── add_item.html
│
├── instance/
│   └── inventory.db
│
├── app.py
├── models.py
└── requirements.txt
 one_pager.md


Installation

  1. Clone the repository or download the project files

  2. Create a virtual environment (recommended):

    
   python -m venv venv
  3. Activate the virtual environment:

    Windows:

    
venv\Scripts\activate

    

    Linux/Mac:

    
source venv/bin/activate
  4. Install required packages:

    
pip install -r requirements.txt


Running the Application

    Make sure your virtual environment is activated

    Run the application:

    
python app.py

    

    Open a web browser and navigate to:

    
http://localhost:5000

    

Default Admin Account

When you first run the application, a default admin account is created:

    Username: admin
    Password: admin123

Usage Examples
Admin Functions:

    Login as admin

    Register new users:
        Click "Register User"
        Fill in username and password
        Check "Register as Administrator" if needed

    Add new items:
        Click "Add Item"
        Fill in item details:
            Inventory Number
            Company
            Model
            Purchase Year
            Purchase Amount
            Department

    Delete items:
        From the dashboard, click "Delete" next to any item

User Functions:

    Login with user credentials

    View inventory:
        All items are displayed in the dashboard

    Search items:
        Use the search bar to find items by:
            Company
            Model
            Inventory number

    Assign/Return items:
        Click "Assign to me" to take an item
        Click "Return Item" to return an assigned item

Security Features

    Password hashing
    Login required for all operations
    Admin-only areas protected
    Session management

Notes

    Only administrators can register new users
    Only administrators can add/delete items
    Users can only assign/return items to themselves
    The SQLite database is automatically created on first run

Error Handling

The application includes error handling for:

    Invalid login attempts
    Duplicate usernames
    Invalid form submissions
    Unauthorized access attempts

Responsive Design

The application is fully responsive and works on:

    Desktop browsers


To contribute to this project:

    Fork the repository
    Create a new branch
    Make your changes
    Submit a pull request

For any other information follow me on GitHub.


