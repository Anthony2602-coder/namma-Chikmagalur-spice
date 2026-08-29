@echo off
echo Setting up Namma Chikmagaluru E-Commerce...
python -m venv venv 2>nul
call venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python generate_icons.py
echo.
echo Setup complete! Run: python manage.py runserver
echo Admin login: admin / admin123
echo Open: http://127.0.0.1:8000
