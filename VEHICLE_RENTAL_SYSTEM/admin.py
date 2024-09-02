

from flask import Flask, render_template, request, redirect, url_for, flash
import file_handling

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/add_car', methods=['GET', 'POST'])
def add_car():
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
    cars = file_handling.get_cars()
    return render_template('view_cars.html', cars=cars)

@app.route('/admin/modify_car', methods=['GET', 'POST'])
def modify_car():
    if request.method == 'POST':
        car_id = request.form['car_id']
        mod_type = request.form['mod_type']
        new_value = request.form['new_value']
        file_handling.mod_car(car_id, mod_type, new_value)
        flash('Car details modified successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('modify_car.html')

if __name__ == '__main__':
    app.run(debug=True)
