## Constructive Conversation Commenting.

### Notes:
This project will not support creating Comments in the prototype. For that, you'll need to run the backend and create the first comment via the Django Admin. This is intentional to reduce peer review overhead (and to stay within the allotted time).

Minimal Django REST Framework is being used in order to use less "magic" (us Python devs are bad for that ;). Some is still used to decouple the frontend and backend. And also because, theoretically, this project would eventually extend to use proper DRF (`djangorestframework`)

In the source code you will find A LOT of `TODO`'s. These are ideas or best practices. I've opted to write them out so people know what I'm thinking while working on this project.

I did _not_ focus too much on the design. I am not to be trusted with major design decisions 🙂

In order to test this repo, you'll want Python 3.9 or newer and an OpenAI API Key

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

### Why I chose this tech stack:
1. Database: After talking to a developer with NP and expressing interest in Postgres, I decided to use a codebase that favours Postgres. Despite this actually using sqlite3, swapping it out for Postgres is _very_ easy. If we need live conversations I would have opted in for Firebase.
2. Django: Proven to scale well, easy to write lots of code that _just works_.
3. React: Because it's the most friendly on my brain haha
