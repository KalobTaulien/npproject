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

### Where I got to in the prototype:
* Frontend authentication was skipped in the name of time to show what an MVP like this could do.
* GPT 3.5 turbo helps assess replies to comments and guide it towards being constructive.
* GPT 3.5 uses a prompt rather than fine tuned model or custom GPT. A custom GPT or fine tuned model would be ideal here.
* Backend is functional in Django. Comments are to be created in the Django Admin to highlight the use case of an admin system such as Django.
* Frontend is functional in React. New replies are generated and saved via React components.
* Feelings are added as a sliding scale. Aggregation was not added (ie. "Facebook's 100 people liked this" feature). However aggregation for the 5 emotional states could be added easily.
* CORS is disabled for a decoupled system. Good for apps, extensions, and custom JS librarier for partner websites.
* There are A LOT of comments in the codebase. Most of them are _not_ necessary, but instead help highlight my thinking in the moment and where we could take this prototype.

### Useful app metrics:
Aside from starndard tech metrics that most apps or websites track, here are some additional ones this prototype could help discover:

* Sliding scale emojis rather than thumbs up/thumbs down. That can help us assess the overall view of people who leave a comment (initiators) and the people who reply (responders). Ie. Are people _happy_, _confused_ or _upset_ about a particular topic?
* Looking at the aggregated sliding scale values (the emotion slider) we can determine what emotions are most often illicited by particular articles that partners write.
* Using an A.I. system to determine if the words match the selected emotion.
* Tracking the change in mood when someone initially reacts to a comment or topic, and then seeing where they are after some guidance, and then seeing where they are after some healthy conversation.. I think _that_ would be a WILD dataset to track. I'd bet the overall mood becomes more balanced.
* Tracking the non-constructive comments that GPT catches vs. the re-written comments that are approved could be a useful metric in sharing how useful this tool is for guiding healthy conversations.

A lot of metrics that I'm thinking about surround human behaviour. Where did they start their emotional journey, and where did they end?
