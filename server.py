from flask import Flask, jsonify
from domjudge import domjudgeScoreboard

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    scoreboardJson = domjudgeScoreboard()
    return jsonify(scoreboardJson)

if __name__ == '__main__':
    app.run(debug=True)
