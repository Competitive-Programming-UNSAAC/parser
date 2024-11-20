from flask import Flask, jsonify
from flask_cors import CORS
from domjudge import domjudgeScoreboard

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route('/data', methods=['GET'])
def get_data():
    scoreboardJson = domjudgeScoreboard()
    return jsonify(scoreboardJson)

if __name__ == '__main__':
    app.run(debug=True)
