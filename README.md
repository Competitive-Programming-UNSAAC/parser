# Parser

# DOM Judge Parser for 9.0.0 (latest)  version

A lightweight Flask-based application for parsing DOM Judge metadata and providing API access to the parsed data. This information is retrieved from the DOMJudge APIs:

- http://localhost/api/v4/contests/dj-1/problems
- http://localhost/api/v4/contests/dj-1/teams
- http://localhost/api/v4/contests/dj-1/judgements
- http://localhost/api/v4/contests/dj-1/submissions

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

## Config changes

#### Local development
```
[Metadata]
path = metadata22                    # Directory containing metadata files
problems = problems.json             # Problems JSON filename
submissions = submissions.json       # Submissions JSON filename
contestants = teams.json             # Teams JSON filename
judgements = judgements.json         # Judgements JSON filename

[Contest]
duration: 300                        # Contest duration in minutes
start: 06-12-2024 09:00:00          # Contest start time (DD-MM-YYYY HH:MM:SS)
frozenTimeDuration: 60              # Scoreboard freeze time in minutes
name: CUSCONTEST                    # Contest name
mode: ICPC                          # Contest format
```

#### Contest Online
```
[Judge]
mode = server                       # Set to "server" for online mode
host = localhost                    # DOM Judge server hostname
admin = admin                       # Admin username
password = -rt6byC4dd_A1kQh        # Admin password
id = dj-1                          # Contest ID

[Contest]
duration: 300                       # Contest duration in minutes
start: 06-12-2024 09:00:00         # Contest start time (DD-MM-YYYY HH:MM:SS)
frozenTimeDuration: 60             # Scoreboard freeze time in minutes
name: CUSCONTEST                   # Contest name
mode: ICPC                         # Contest format
```


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