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