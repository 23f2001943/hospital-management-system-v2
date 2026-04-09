# hospital-management-system-v2

This is a web-based Hospital Management System (HMS) developed to efficiently manage patients, doctors, appointments, and treatment records. The system supports role-based access for Admin, Doctor, and Patient, enabling smooth coordination and management of hospital operations.

---

# Folder Structure

HOSPITAL-MANAGEMENT-SYSTEM/
│
├── backend/
│   ├── app.py                  # Flask application entry point
│   ├── config.py               # Configuration settings
│   ├── extensions.py           # DB, security, cache setup
│   ├── models.py               # Database models
│   │
│   ├── resources/              # API routes (Blueprints)
│   │   ├── admin_resources.py
│   │   ├── doctor_resources.py
│   │   ├── patient_resources.py
│   │   └── auth_resources.py
│   │
│   ├── services/               # Business logic layer
│   │   ├── admin_service.py
│   │   ├── doctor_service.py
│   │   └── patient_service.py
│   │
│   ├── tasks/                  # Celery background jobs
│   │   └── test.py
│   │
│   ├── instance/
│   │   └── database.sqlite3    # SQLite database
│   │
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── pages/              # Role-based pages (Admin, Doctor, Patient)
│   │   ├── components/         # Reusable components (Navbar, Sidebar)
│   │   ├── router/             # Vue router with route guards
│   │   ├── assets/             # Static assets
│   │   ├── App.vue
│   │   └── main.js
│   │
│   ├── public/
│   └── package.json           # Frontend dependencies
│
├── MAD2report.pdf             # Project report (PDF)
├── README.md                  # Project documentation
└── .gitignore

---

# Features

- Role-based authentication (Admin, Doctor, Patient)
- Admin dashboard with doctor, patient, and appointment management
- Doctor dashboard for managing appointments and treatments
- Patient dashboard for booking and viewing appointments
- Appointment scheduling with conflict prevention
- Treatment history tracking
- Redis caching for API performance optimization
- Celery background jobs (reminders, reports, CSV export)
- Responsive UI using Bootstrap and Vue.js

---

# Technologies Used

- Flask (Backend)
- Flask-SQLAlchemy (ORM)
- Flask-Security (Authentication & RBAC)
- SQLite (Database)
- Vue.js (Frontend)
- Bootstrap (UI Styling)
- Axios (API communication)
- Redis (Caching)
- Celery (Background jobs)

---

# How to Run

terminal 1 :
backend > python app.py

terminal 2 : 
backend > celery -A celery_worker.celery worker --loglevel=info -P eventlet

terminal 3 :
backend > celery -A celery_worker.celery beat --loglevel=info

terminal 4 : 
frontend > npm run dev

Also open mainhog before workers and
open mailhog in browser by the link -   http://localhost:8025


## Backend Setup

pip install -r requirements.txt
