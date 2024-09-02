from flask import Flask, render_template, request, redirect, url_for, flash, session
import file_handling

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Example users dictionary (you might load this from users.txt)
USERS = {
    'abhi': '123'  # Example username and password
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if USERS.get(username) == password:
            session['username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/admin/add_car', methods=['GET', 'POST'])
def add_car():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        car_model = request.form['car_model']
        car_type = request.form['car_type']
        car_transmission = request.form['car_transmission']
        hourly_rate = request.form['hourly_rate']
        file_handling.add_car(car_model, car_type, car_transmission, hourly_rate)
        flash('Car added successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_car.html')

@app.route('/admin/view_cars')
def view_cars():
    if 'username' not in session:
        return redirect(url_for('login'))
    cars = file_handling.get_all_cars()
    return render_template('view_cars.html', cars=cars)

@app.route('/admin/modify_car', methods=['GET', 'POST'])
def modify_car():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        car_id = request.form['car_id']
        new_model = request.form['new_model']
        new_car_type = request.form['new_car_type']
        new_transmission = request.form['new_transmission']
        new_rate = request.form['new_rate']
        file_handling.update_car(car_id, new_model, new_car_type, new_transmission, new_rate)
        flash('Car details modified successfully!')
        return redirect(url_for('admin_dashboard'))
    cars = file_handling.get_all_cars()
    return render_template('modify_car.html', cars=cars)

@app.route('/admin/remove_car', methods=['GET', 'POST'])
def remove_car():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        car_id = request.form['car_id']
        file_handling.remove_car(car_id)
        flash('Car removed successfully!')
        return redirect(url_for('admin_dashboard'))
    cars = file_handling.get_all_cars()
    return render_template('remove_car.html', cars=cars)

@app.route('/customer')
def customer_dashboard():
    return render_template('customer_dashboard.html')

@app.route('/customer/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        age = request.form['age']
        username = request.form['username']
        password = request.form['password']
        file_handling.register_user(username, password)  # Register user
        flash('Registration successful! Please log in.')
        
    return render_template('new_user.html')

@app.route('/customer/registered_user', methods=['GET', 'POST'])
def registered_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if file_handling.validate_user(username, password):
            session['username'] = username
            return redirect(url_for('customer_menu'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('registered_user.html')

@app.route('/customer/menu')
def customer_menu():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('customer_menu.html')

@app.route('/customer/view_cars')
def customer_view_cars():
    if 'username' not in session:
        return redirect(url_for('login'))
    cars = file_handling.get_all_cars()
    return render_template('view_cars_customer.html', cars=cars)

def view_history():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    history = file_handling.get_rental_history(username)  # Assuming this function returns rental history
    return render_template('view_history.html', history=history)

@app.route('/customer/book_car', methods=['GET', 'POST'])
def book_car():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        car_id = request.form['car_id']
        duration_hours = int(request.form['duration_hours'])
        car = file_handling.get_car_by_id(car_id)
        if car:
            hourly_rate = float(car['rate'])
            total_cost = hourly_rate * duration_hours
            file_handling.book_car(session['username'], car_id, duration_hours, total_cost)
            flash(f'Car booked successfully! Total cost: ${total_cost:.2f}')
            return redirect(url_for('customer_menu'))
        else:
            flash('Car not found.')
    cars = file_handling.get_all_cars()
    return render_template('book_car.html', cars=cars)

@app.route('/customer/payment', methods=['GET', 'POST'])
def payment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if request.method == 'POST':
        payment_amount = float(request.form['payment_amount'])
        file_handling.process_payment(username, payment_amount)
        flash('Payment successful!')
        return redirect(url_for('customer_menu'))

    pending_payments = file_handling.get_pending_payments(username)
    return render_template('payment.html', pending_payments=pending_payments)

@app.route('/customer/view_rentals')
def view_rentals():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    rentals = file_handling.get_rental_history(username)
    return render_template('view_rentals.html', rentals=rentals)
if __name__ == '__main__':
    app.run(debug=True)
