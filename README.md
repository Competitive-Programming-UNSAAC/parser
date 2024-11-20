# Parser

# DOM Judge Parser

A lightweight Flask-based application for parsing DOM Judge metadata and providing API access to the parsed data.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Competitive-Programming-UNSAAC/parser.git
cd parser
```

2. Install the required dependencies:
```bash
pip3 install -r requirements.txt
```

## Configuration

Before running the server, ensure that the configuration file points to the correct DOM Judge metadata. Update any necessary paths or settings in the configuration file.

## Running the Server

1. Start the Flask server:
```bash
python3 server.py
```

2. Access the API in your browser or with tools like curl or Postman:
```bash
http://127.0.0.1:5000/data
```

## API Endpoints

- `GET /data`: Fetches and returns the parsed DOM Judge metadata.

```json
{
  "contestMetadata": {
    "duration": 180,
    "frozenTimeDuration": 45,
    "name": "Cuscontest",
    "type": "ICPC"
  },
  "problems": [
    { "index": "A" },
    { "index": "B" },
    { "index": "C" },
    { "index": "D" },
    { "index": "E" },
    { "index": "F" },
    { "index": "G" },
    { "index": "H" },
    { "index": "I" },
    { "index": "J" }
  ],
  "contestants": [
    { "id": 1, "name": "Team A" },
    { "id": 2, "name": "Team B" },
    { "id": 3, "name": "Team C" }
  ],
  "verdicts": {
    "accepted": ["Accepted"],
    "wrongAnswerWithPenalty": ["Wrong answer"],
    "wrongAnswerWithoutPenalty": ["Compilation error"]
  },
  "submissions": [
    {
      "timeSubmitted": 12,
      "contestantName": "Team A",
      "problemIndex": "A",
      "verdict": "Accepted"
    },
    {
      "timeSubmitted": 23,
      "contestantName": "Team B",
      "problemIndex": "H",
      "verdict": "Wrong answer"
    },
    {
      "timeSubmitted": 43,
      "contestantName": "Team C",
      "problemIndex": "A",
      "verdict": "Accepted"
    }
  ]
}
```