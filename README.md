# OneFinProject
# Movie Collection API
A Django REST Framework-based API that allows users to create, manage, and retrieve movie collections. Includes authentication, external movie API integration, and request counting middleware

# Features:

User Authentication (JWT-based)

CRUD Operations for movie collections

External Movie API Integration with retry logic

Request Counter Middleware for monitoring API usage

Django REST Framework for API development

# Tech Stack:

Backend: Python, Django, Django REST Framework (DRF)

Authentication: JWT (Simple JWT)

Database: SQLite (Default, but can use PostgreSQL/MySQL)

Caching: Django Cache

Testing: Django Test Framework, Factory Boy, DRF API Testing

# Setup & Installation:
Clone the Repository
git clone https://github.com/Rakesh260/OneFinProject

Create and Activate a Virtual Environment

For Windows:

python -m venv venv

venv\Scripts\activate

For macOS/Linux:

python3 -m venv venv

source venv/bin/activate

#  Install Dependencies
pip install -r requirements.txt

#  Set Up Environment Variables
Create a .env file and add:

MOVIE_API_USERNAME=iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0
MOVIE_API_PASSWORD=Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1

# Apply Migrations
python manage.py makemigrations

python manage.py migrate

# Run the Server
python manage.py runserver

# API Endpoints
# Authentication APIs:

Register: POST /register/

Login: POST /api/token/

Refresh Token: POST /api/token/refresh/

# Movie Collection APIs:

Get Movies (From External API): GET /movies/

Get User Collections: GET /collection/

Create Collection: POST /collection/

Update Collection: PUT /collection/<uuid>/

Delete Collection: DELETE /collection/<uuid>/

# Request Counter Middleware APIs:

Get API Request Count: GET /request-count/

Reset Counter: POST /request-count/reset/

#  Running Tests

python manage.py test
