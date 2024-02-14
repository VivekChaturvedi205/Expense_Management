# Reimbursement System

A web application that simplifies and automates the process of submitting and approving expenses for employees and managers. Built with Python and Django.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contribution](#contribution)
- [License](#license)

## Installation
To install and run this project, you will need:

- Python 3.8.5 or higher
- Django 4.2.9 or higher
- SQLite3 
- virtualenv

Follow these steps to set up the project:

1. Clone this repository to your local machine.
2. Create and activate a virtual environment using pipenv or virtualenv.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Create a PostgreSQL database and user for the project. Update the DATABASES setting in `settings.py` with your database credentials.
5. Run `python manage.py migrate` to create the database tables and schema.
6. Run `python manage.py createsuperuser` to create an admin user for the project.
7. Run `python manage.py runserver` to start the development server.

## Usage
To use this project, access the web application through your browser at http://localhost:8000/.

The application has three types of users: admin, manager, and candidate. The admin can create and manage other users, and approve any expenses. The manager can approve the expenses of the candidates under their supervision. The candidate can only submit their own expenses.

