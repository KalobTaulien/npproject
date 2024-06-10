## Constructive Conversation Commenting.

### Notes:
This project will not support creating Comments in the prototype. For that, you'll need to run the backend and create the first comment via the Django Admin. This is intentional to reduce peer review overhead (and to stay within the allotted time).

Minimal Django REST Framework is being used in order to use less "magic" (us Python devs are bad for that ;). Some is still used to decouple the frontend and backend. And also because, theoretically, this project would eventually extend to use proper DRF (`djangorestframework`)

### Developer installation

#### Backend
```
python3 -m venv .venv/
source .venv/bin/activate # Different for Windows
cp .env.example .env # Update the .env file as needed
pip install -r requirements.txt
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
# load http://localhost:8000/admin/ to access the backend
```

#### Frontend
There is no webpack to hot reload changes. You'll need to open `prod/index.html` in your browser.
```
npm i
npm run js:dev
npm run css:dev
```
