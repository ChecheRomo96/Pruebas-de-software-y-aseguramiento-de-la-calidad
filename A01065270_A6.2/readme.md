# 1️⃣ Create a virtual environment
python -m venv venv

# 2️⃣ Activate the virtual environment:
# macOS/Linux:
source venv/bin/activate

# Windows (PowerShell):
venv\Scripts\Activate

# install requirements.txt
pip install -r requirements.txt

# discover and run unit tests (run from top dir)
python -m unittest discover -s tests

# coverage tests tests (run from top dir)
coverage run -m unittest discover

coverage report -m

coverage html

# open coverage test results (graphic)
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov\index.html  # Windows
