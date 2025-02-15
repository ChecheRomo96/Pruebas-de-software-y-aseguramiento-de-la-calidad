# 1️⃣ Create a virtual environment
python -m venv venv

# 2️⃣ Activate the virtual environment:
# 🔹 macOS/Linux:
source venv/bin/activate

# 🔹 Windows (PowerShell):
venv\Scripts\Activate

# 3️⃣ Install dependencies
pip install -r requirements.txt


python -m unittest discover -s tests

