# JobBoard

A job board web app built with Django (backend) and Vue 3 (frontend).

---

## Requirements

Make sure you have these installed before starting:

- Python 3.11+
- Node.js 18+
- Git

---

## Project Structure

```
jobboard/
├── backend/    # Django REST API
└── frontend/   # Vue 3 app
```

---

## Backend Setup

```bash
# 1. Go into the backend folder
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run database migrations
python manage.py makemigrations authentication job_board
python manage.py migrate

# 4. Create an admin account (optional)
python manage.py createsuperuser

# 5. Start the server
python manage.py runserver
```

Backend will be running at: `http://localhost:8000`  
Admin panel: `http://localhost:8000/admin`  
APIs List: `http://localhost:8000/docs/` 

---

## Frontend Setup

Open a **new terminal** and run:

```bash
# 1. Go into the frontend folder
cd frontend

# 2. Install dependencies
npm install

# 3. Start the dev server
npm run dev
```

Frontend will be running at: `http://localhost:5173`
