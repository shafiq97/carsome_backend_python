from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'localhost',
    'database': 'carsome',
    'user': 'root',      # Replace with your MySQL username
    'password': ''   # Replace with your MySQL password
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/cars', methods=['GET'])
def get_cars():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM cars order by price desc")
        cars = cursor.fetchall()
        return jsonify(cars)
    finally:
        cursor.close()
        connection.close()

@app.route('/cars', methods=['POST'])
def add_car():
    car_data = request.get_json()
    required_fields = ['make', 'model', 'year', 'price', 'mileage', 'color']

    # Validate required fields
    if not all(field in car_data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = connection.cursor()
    try:
        insert_query = """
            INSERT INTO cars (make, model, year, price, mileage, color)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            car_data['make'],
            car_data['model'],
            car_data['year'],
            car_data['price'],
            car_data['mileage'],
            car_data['color']
        ))
        connection.commit()
        return jsonify({'message': 'Car added successfully'}), 201
    except Exception as e:
        print(f"Error adding car: {e}")
        return jsonify({'error': 'Failed to add car'}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        car = cursor.fetchone()
        if car:
            return jsonify(car)
        else:
            return jsonify({'message': 'Car not found'}), 404
    finally:
        cursor.close()
        connection.close()

@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car_data = request.get_json()
    required_fields = ['make', 'model', 'year', 'price', 'mileage', 'color']

    # Validate required fields
    if not all(field in car_data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = connection.cursor()
    try:
        update_query = """
            UPDATE cars SET make = %s, model = %s, year = %s, price = %s, mileage = %s, color = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (
            car_data['make'],
            car_data['model'],
            car_data['year'],
            car_data['price'],
            car_data['mileage'],
            car_data['color'],
            car_id
        ))
        connection.commit()
        return jsonify({'message': 'Car updated successfully'}), 200
    except Exception as e:
        print(f"Error updating car: {e}")
        return jsonify({'error': 'Failed to update car'}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = connection.cursor()
    try:
        delete_query = "DELETE FROM cars WHERE id = %s"
        cursor.execute(delete_query, (car_id,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Car not found'}), 404
        return jsonify({'message': 'Car deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting car: {e}")
        return jsonify({'error': 'Failed to delete car'}), 500
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)
