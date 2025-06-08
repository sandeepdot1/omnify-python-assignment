# 1. Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Initialize DB & seed
python seed_data.py

# 3. Start API
python app.py
