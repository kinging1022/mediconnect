MediConnect 🏥💬

AI-Powered Telemedicine Platform

MediConnect is a web-based telemedicine platform that connects patients with doctors for real-time consultations via chat and video calls. It uses AI-powered doctor matching, vector search, and WebSockets for real-time interactions.

🚀 Features

✅ Patients
	•	Book Appointments – Schedule a session with available doctors.
	•	AI-Powered Doctor Matching – AI recommends the best doctor based on symptoms.
	•	Live Chat & Video Calls – Secure, real-time communication with doctors.
	•	Notifications – Get updates on appointment status and doctor availability.

✅ Doctors
	•	Accept or Reject Appointments – Manage consultations efficiently.
	•	One Active Session Rule – Prevents handling multiple patients at once.



🛠️ Tech Stack

Backend (Django + DRF)
	•	Django REST Framework (DRF) – API development.
	•	Django Channels – WebSockets for real-time chat & video calls.
	•	Celery + Redis – Background tasks (notifications, AI processing).
	•	FAISS + OpenAI – AI-powered doctor matching via vector search.
	•	JWT Authentication – Secure user sessions.

Frontend (Vue.js + Pinia)
	•	Vue 3 + Vite – Fast and lightweight frontend.
	•	Pinia – State management.
	•	Axios – API calls.
	•	WebSockets – Live chat and notifications.

🔧 Installation & Setup

1️⃣ Clone the Repository

git clone https://github.com/kinging1022/mediconnect.git
cd mediconnect

2️⃣ Backend Setup (Django)

cd backend
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

3️⃣ Frontend Setup (Vue.js)

cd ../frontend
npm install
npm run dev

Visit http://localhost:5173/ to access the app.

🌍 Deployment Guide
	•	Backend: Can be deployed on Heroku, AWS, or DigitalOcean with Gunicorn & Nginx.
	•	Frontend: Deploy via Vercel, Netlify, or Cloudflare Pages.
	•	WebSockets: Requires Daphne or Uvicorn with ASGI.



## 🎥 Demo Video  
Watch the full demo: [Click here to view](https://drive.google.com/file/d/1tS2QFpqr4nLFbg_DEP7Qxgx-6-AZM2z3/view)




⭐ Star This Repo

If you like this project, give it a star ⭐ on GitHub!