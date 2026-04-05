# Vehicle Rental System

A Flask-based web application for managing vehicle rentals with separate admin and customer flows.

## Features

- Admin login and dashboard
- Add, view, modify, and remove cars
- Customer registration and login
- View available cars with vehicle images
- Book vehicles by duration (hourly)
- Rental history and payment tracking
- INR currency display (`₹`) in UI
- Modern responsive interface (HTML/CSS/JS)

## Tech Stack

- Python
- Flask
- HTML (Jinja templates)
- CSS
- JavaScript
- Text-file based storage (`cars.txt`, `users.txt`, `rentals.txt`)

## Project Structure

```text
VEHICLE_RENTAL_SYSTEM/
├── app.py
├── file_handling.py
├── admin.py
├── cars.txt
├── users.txt
├── rentals.txt
├── static/
│   ├── styles.css
│   ├── app.js
│   └── vehicle-placeholder.svg
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── admin_dashboard.html
    ├── add_car.html
    ├── view_cars.html
    ├── modify_car.html
    ├── remove_car.html
    ├── customer_dashboard.html
    ├── new_user.html
    ├── registered_user.html
    ├── customer_menu.html
    ├── view_cars_customer.html
    ├── book_car.html
    ├── payment.html
    ├── view_rentals.html
    └── view_history.html
```

## Setup and Run

### 1. Create virtual environment

```powershell
python -m venv .venv
```

### 2. Activate virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install flask
```

### 4. Start the app

```powershell
python app.py
```

App runs at:

```text
http://127.0.0.1:5000
```

## Default Admin Login

Current hardcoded admin credentials in `app.py`:

- Username: `abhi`
- Password: `123`

## Data Files

- `cars.txt`: car records (includes image URL column)
- `users.txt`: customer credentials
- `rentals.txt`: booking/payment status

## Notes

- This project currently uses plain-text files for storage.
- Passwords are not hashed yet.
- For production use, migrate to a database and secure authentication.

## License

This project is for educational/demo purposes.
