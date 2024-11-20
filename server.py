from flask import Flask, jsonify
from flask_cors import CORS
from domjudge import domjudgeScoreboard

app = Flask(__name__)
# Allows the scoreboard to call the defined API
CORS(app, origins=["http://localhost:5173"])

@app.route('/data', methods=['GET'])
def get_data():
    try:
        scoreboardJson = domjudgeScoreboard()
        return jsonify(scoreboardJson), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
