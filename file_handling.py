import uuid

DEFAULT_CAR_IMAGE = "/static/vehicle-placeholder.svg"


def normalize_image_url(image_url):
    value = (image_url or "").strip()
    return value if value else DEFAULT_CAR_IMAGE

# Generate a unique ID for a car
def generate_unique_id():
    """Generate a unique ID for a car."""
    return str(uuid.uuid4().int)[:6]  # Shorter unique ID

# Save car data to 'cars.txt'
def save_car(car):
    with open('cars.txt', 'a') as f:
        f.write(
            f"{car['id']},{car['model']},{car['car_type']},{car['transmission']},{car['rate']},{normalize_image_url(car.get('image_url'))}\n"
        )

# Get all car details from 'cars.txt'
def get_all_cars():
    cars = []
    try:
        with open('cars.txt', 'r') as f:
            for line in f:
                parts = line.rstrip('\n').split(',', 5)
                if len(parts) >= 5:  # ID, Model, Type, Transmission, Rate, optional image_url
                    car_id, model, car_type, transmission, rate = parts[:5]
                    image_url = normalize_image_url(parts[5]) if len(parts) == 6 else DEFAULT_CAR_IMAGE
                    cars.append({
                        'id': car_id,
                        'model': model,
                        'car_type': car_type,
                        'transmission': transmission,
                        'rate': rate,
                        'image_url': image_url
                    })
                else:
                    print(f"Skipping line due to incorrect format: {line.strip()}")
    except FileNotFoundError:
        pass  # Handle case where file does not exist
    return cars

# Add a new car to 'cars.txt'
def add_car(model, car_type, transmission, rate, image_url=''):
    car_id = generate_unique_id()
    car = {
        'id': car_id,
        'model': model,
        'car_type': car_type,
        'transmission': transmission,
        'rate': rate,
        'image_url': normalize_image_url(image_url)
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
def update_car(car_id, new_model, new_car_type, new_transmission, new_rate, new_image_url=''):
    cars = get_all_cars()
    with open('cars.txt', 'w') as f:
        for car in cars:
            if car['id'] == car_id:
                updated_model = new_model.strip() if new_model.strip() else car['model']
                updated_type = new_car_type.strip() if new_car_type.strip() else car['car_type']
                updated_transmission = new_transmission.strip() if new_transmission.strip() else car['transmission']
                updated_rate = new_rate.strip() if new_rate.strip() else car['rate']
                updated_image_url = normalize_image_url(new_image_url) if new_image_url.strip() else normalize_image_url(car.get('image_url'))
                f.write(
                    f"{car_id},{updated_model},{updated_type},{updated_transmission},{updated_rate},{updated_image_url}\n"
                )
            else:
                f.write(
                    f"{car['id']},{car['model']},{car['car_type']},{car['transmission']},{car['rate']},{normalize_image_url(car.get('image_url'))}\n"
                )

# Remove a car by ID
def remove_car(car_id):
    cars = get_all_cars()
    with open('cars.txt', 'w') as f:
        for car in cars:
            if car['id'] != car_id:
                f.write(
                    f"{car['id']},{car['model']},{car['car_type']},{car['transmission']},{car['rate']},{normalize_image_url(car.get('image_url'))}\n"
                )

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


