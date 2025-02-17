# Reservations System

## Setup Instructions

### 1️⃣ Create a Virtual Environment
To set up a virtual environment for the project, run:
```
python -m venv venv
```

### 2️⃣ Activate the Virtual Environment
#### macOS/Linux:
```
source venv/bin/activate
```

#### Windows (PowerShell):
```
venv\Scripts\Activate
```

### 3️⃣ Install Dependencies
Once the virtual environment is activated, install the required packages:
```
pip install -r requirements.txt
```

## Running Tests

### Discover and Run Unit Tests
From the top directory of the project, execute:
```
python -m unittest discover -s tests
```

### Coverage Testing
Run the tests with coverage tracking:
```
coverage run -m unittest discover
```

Generate a coverage report:
```
coverage report -m
```

Generate an HTML coverage report:
```
coverage html
```

### Viewing Coverage Results
To open the HTML coverage report, use the appropriate command for your operating system:

#### macOS:
```
open htmlcov/index.html
```

#### Linux:
```
xdg-open htmlcov/index.html
```

#### Windows:
```
start htmlcov\index.html
```
