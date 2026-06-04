from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import init_db, save_game_result, get_leaderboard
from datetime import datetime

app = Flask(__name__)
CORS(app)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/save_result', methods=['POST'])
def save_result():
    data = request.json
    player_name = data.get('player_name')
    winner = data.get('winner')
    date = datetime.now().isoformat()
    save_game_result(player_name, winner, date)
    return jsonify({'status': 'success'}), 201

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    return jsonify(get_leaderboard())

if __name__ == '__main__':
    app.run(debug=True, port=5000)