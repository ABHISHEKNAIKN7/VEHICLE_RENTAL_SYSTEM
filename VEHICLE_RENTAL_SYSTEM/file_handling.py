import uuid

# Generate a unique ID for a car
def generate_unique_id():
    """Generate a unique ID for a car."""
    return str(uuid.uuid4().int)[:6]  # Shorter unique ID

# Save car data to 'cars.txt'
def save_car(car):
    with open('cars.txt', 'a') as f:
        f.write(f"{car['id']},{car['model']},{car['car_type']},{car['transmission']},{car['rate']}\n")

# Get all car details from 'cars.txt'
def get_all_cars():
    cars = []
    try:
        with open('cars.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 5:  # ID, Model, Type, Transmission, Rate
                    car_id, model, car_type, transmission, rate = parts
                    cars.append({
                        'id': car_id,
                        'model': model,
                        'car_type': car_type,
                        'transmission': transmission,
                        'rate': rate
                    })
                else:
                    print(f"Skipping line due to incorrect format: {line.strip()}")
    except FileNotFoundError:
        pass  # Handle case where file does not exist
    return cars

# Add a new car to 'cars.txt'
def add_car(model, car_type, transmission, rate):
    car_id = generate_unique_id()
    car = {
        'id': car_id,
        'model': model,
        'car_type': car_type,
        'transmission': transmission,
        'rate': rate
    }
    save_car(car)

# Get a car by its ID
def get_car_by_id(car_id):
    cars = get_all_cars()
    for car in cars:
        if car['id'] == car_id:
            return car
    return None

# Update car details by ID
def update_car(car_id, new_model, new_car_type, new_transmission, new_rate):
    cars = get_all_cars()
    with open('cars.txt', 'w') as f:
        for car in cars:
            if car['id'] == car_id:
                f.write(f"{car_id},{new_model},{new_car_type},{new_transmission},{new_rate}\n")
            else:
                f.write(f"{car['id']},{car['model']},{car['car_type']},{car['transmission']},{car['rate']}\n")

# Remove a car by ID
def remove_car(car_id):
    cars = get_all_cars()
    with open('cars.txt', 'w') as f:
        for car in cars:
            if car['id'] != car_id:
                f.write(f"{car['id']},{car['model']},{car['car_type']},{car['transmission']},{car['rate']}\n")

# Register a new user in 'users.txt'
def register_user(username, password):
    with open('users.txt', 'a') as f:
        f.write(f"{username},{password}\n")

# Validate user login credentials from 'users.txt'
def validate_user(username, password):
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    user, pwd = parts
                    if user == username and pwd == password:
                        return True
                else:
                    print(f"Skipping line due to incorrect format: {line.strip()}")
    except FileNotFoundError:
        print("User file not found.")
    return False


# Save booking details


# Get rental history for a user

def book_car(username, car_id, duration_hours, total_cost):
    with open('rentals.txt', 'a') as f:
        f.write(f"{username},{car_id},{duration_hours},{total_cost},pending\n")

def get_rental_history(username):
    history = []
    try:
        with open('rentals.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    user, car_id, duration_hours, total_cost, status = parts
                    if user == username:
                        history.append({'car_id': car_id, 'duration_hours': duration_hours, 'total_cost': total_cost, 'status': status})
    except FileNotFoundError:
        pass
    return history

def get_pending_payments(username):
    pending_payments = []
    try:
        with open('rentals.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    user, car_id, duration_hours, total_cost, status = parts
                    if user == username and status == 'pending':
                        pending_payments.append({'car_id': car_id, 'duration_hours': duration_hours, 'total_cost': total_cost})
    except FileNotFoundError:
        pass
    return pending_payments

def process_payment(username, payment_amount):
    rentals = get_rental_history(username)
    pending_rentals = [rental for rental in rentals if rental['status'] == 'pending']

    total_pending_amount = sum(float(rental['total_cost']) for rental in pending_rentals)

    if payment_amount >= total_pending_amount:
        for rental in pending_rentals:
            update_rental_status(username, rental['car_id'], 'paid')
        return True
    else:
        return False


def update_rental_status(username, car_id, new_status):
    rentals = get_rental_history(username)
    with open('rentals.txt', 'w') as f:
        for rental in rentals:
            if rental['car_id'] == car_id:
                f.write(f"{username},{car_id},{rental['duration_hours']},{rental['total_cost']},{new_status}\n")
            else:
                f.write(f"{rental['user']},{rental['car_id']},{rental['duration_hours']},{rental['total_cost']},{rental['status']}\n")


def remove_car(car_id):
    cars = get_all_cars()
    with open('cars.txt', 'w') as f:
        for car in cars:
            if car['id'] != car_id:
                f.write(f"{car['id']},{car['model']},{car['car_type']},{car['transmission']},{car['rate']}\n")