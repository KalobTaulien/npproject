### Developer installation

#### Backend
```
python3 -m venv .venv/
source .venv/bin/activate # Different for Windows
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
