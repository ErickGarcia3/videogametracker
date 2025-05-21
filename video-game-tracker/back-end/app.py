from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

@app.route('/api/games', methods=['GET'])
def get_games():
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(games)

@app.route('/api/games', methods=['POST'])
def add_game():
    data = request.json
    if not data or 'title' not in data or 'platform' not in data or 'play_status' not in data or 'hours_played' not in data or 'rating' not in data or 'store_url' not in data:
        return jsonify({'error': 'Missing required fields (title, platform, play status, hours played, rating, store url)'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO games (title, platform, play_status, hours_played, rating, store_url) VALUES (%s, %s, %s, %s, %s, %s)",
            (data['title'], data['platform'], data['play_status'], data['hours_played'], data['rating'], data['store_url'])
        )
        connection.commit()
        game_id = cursor.lastrowid
        cursor.close()
        connection.close()

        return jsonify({
            'id': game_id,
            'title': data['title'],
            'platform': data['platform'],
            'play_status': data['play_status'],
            'hours_played': data['hours_played'],
            'rating': data['rating'],
            'store_url': data['store_url']
        }), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/games/<int:id>', methods=['GET'])
def get_game(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM games WHERE id = %s", (id,))
    game = cursor.fetchone()
    cursor.close()
    connection.close()

    if not game:
        return jsonify({'error': 'Game not found'}), 404

    return jsonify(game)

@app.route('/api/games/<int:id>', methods=['PUT'])
def update_game(id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        updates = []
        values = []
        if 'title' in data:
            updates.append("title = %s")
            values.append(data['title'])
        if 'platform' in data:
            updates.append("platform = %s")
            values.append(data['platform'])
        if 'play_status' in data:
            updates.append("play_status = %s")
            values.append(data['play_status'])
        if 'hours_played' in data:
            updates.append("hours_played = %s")
            values.append(data['hours_played'])
        if 'rating' in data:
            updates.append("rating = %s")
            values.append(data['rating'])
        if 'store_url' in data:
            updates.append("store_url = %s")
            values.append(data['store_url'])


        if not updates:
            return jsonify({'error': 'No valid fields to update'}), 400

        query = f"UPDATE games SET {', '.join(updates)} WHERE id = %s"
        values.append(id)
        cursor.execute(query, tuple(values))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Game not found'}), 404

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Game updated successfully'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/games/<int:id>', methods=['DELETE'])
def delete_game(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM games WHERE id = %s", (id,))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Game not found'}), 404

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Game deleted successfully'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)