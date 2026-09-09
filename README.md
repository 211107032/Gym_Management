# Complete Gym Management System — Full-Stack Python Project

A production-ready, full-stack **Gym Management System** built with Python 3.11+, Django 5+, Django REST Framework (DRF), SimpleJWT, PostgreSQL/SQLite, WhiteNoise, Bootstrap 5, and Chart.js.

Designed with enterprise-grade modular architecture, Role-Based Access Control (RBAC), printable payment receipts, interactive fitness progress tracking, dynamic dashboard analytics, REST APIs, CSV reporting, and Vercel serverless deployment support.

---

## 🌟 Key Features

* **Role-Based Access Control (RBAC)**: Distinct permissions and custom dashboards for **Admin**, **Staff**, **Trainer**, and **Member**.
* **Member Management**: Complete CRUD operations, auto-generated Member IDs (`MEM-0001`), height/weight tracking, medical notes, emergency contacts, filter by status or expiry.
* **Membership Plans & Subscriptions**: Flexible plan durations (30, 90, 180, 365 days), automatic start/end date calculations, remaining days counter, and 7-day expiry warning alerts.
* **Daily Attendance System**: Quick barcode/ID check-in with duplicate daily check-in prevention, late status detection, check-out timestamps, and monthly attendance breakdown.
* **Payment Management & Print Receipts**: Track payments (Cash, UPI, Card, Online), auto-generated Payment IDs (`PAY-000001`), transaction IDs, and clean print-friendly payment receipts (`window.print()`).
* **Trainer & Workout Routine Builder**: Assign members to personal trainers, build multi-exercise workout routines with sets, reps, weight, and rest time.
* **Body Progress & BMI Charting**: Interactive Chart.js graphs tracking member weight evolution and BMI over time.
* **Executive Reports & CSV Export**: Export Members, Payments, Attendance logs, and Subscriptions into CSV format with a single click.
* **Notifications & Audit Logging**: System activity log tracking user actions, logins, and IP addresses alongside in-app notification dropdowns.
* **REST APIs**: Full DRF API viewsets with SimpleJWT authentication (`Bearer <token>`) and custom endpoints.

---

## 🛠️ Technology Stack

* **Backend**: Python 3.11+, Django 5.2+, Django REST Framework, SimpleJWT, Pillow, WhiteNoise, `dj-database-url`.
* **Frontend**: Django Templates, Bootstrap 5, Bootstrap Icons, Chart.js, HTML5, CSS3, JavaScript.
* **Database**: SQLite (Local development) / PostgreSQL (Production).
* **Deployment**: Vercel Serverless (`vercel.json`), WhiteNoise Static Asset Compression.

---

## 📁 Project Architecture

```text
Gym/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── vercel.json
│
├── config/             # Main Django settings, urls, wsgi, asgi
├── accounts/           # Custom User model, RBAC, Auth, User management
├── gym_settings/       # Gym facility info, logo, address, currency settings
├── members/            # Member profile CRUD, directory & details
├── memberships/        # Membership plans & subscription logic
├── attendance/         # Check-in, check-out & attendance logs
├── payments/           # Financial transactions & printable receipts
├── trainers/           # Trainer profiles & member assignments
├── workouts/           # Workout routines & body progress Chart.js
├── notifications/      # System & user notification alerts
├── audit_logs/         # Security audit logging middleware & views
├── reports/            # Analytics dashboard & CSV export center
├── dashboard/          # Role-tailored dashboards & Chart.js API
├── api/                # DRF REST API ViewSets & SimpleJWT endpoints
│
├── templates/          # Responsive Bootstrap 5 HTML templates
└── static/             # Custom CSS, JS micro-animations, icons
```

---

## 🔐 Default Demo Accounts (Seeded Data)

The project includes a `seed_data` management command that populates 20+ realistic demo members, 5 trainers, membership plans, attendance logs, and transactions:

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | Full administrative control & settings |
| **Staff** | `staff1` | `staff123` | Member registration, attendance & payments |
| **Trainer** | `trainer1` | `trainer123` | View assigned members & workout plans |
| **Member** | `member1` | `member123` | View personal subscription, workout & progress |

---

## 🚀 Local Installation & Setup

### 1. Clone & Setup Virtual Environment

```powershell
# Navigate into project directory
cd Gym

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

### 4. Database Migrations & Data Seeding

```powershell
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Seed sample demo data (Members, Trainers, Plans, Payments, Attendance)
python manage.py seed_data
```

### 5. Run Development Server

```powershell
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/` and sign in!

---

## 🧪 Running Automated Tests

Run the Django automated test suite:

```powershell
python manage.py test
```

---

## 📡 REST API Documentation

The system includes REST API endpoints authenticated via SimpleJWT tokens.

### Authentication Endpoints

* `POST /api/auth/login/` — Obtain JWT access and refresh token pair.
* `POST /api/auth/refresh/` — Refresh access token.

### Core Data Endpoints (Bearer Token Header Required)

* `GET /api/members/` | `POST /api/members/` — Member directory.
* `GET /api/membership-plans/` | `POST /api/membership-plans/` — Membership plans.
* `GET /api/subscriptions/` | `POST /api/subscriptions/` — Subscriptions.
* `POST /api/attendance/check-in/` — Perform quick attendance check-in.
* `POST /api/attendance/check-out/` — Perform check-out.
* `GET /api/payments/` | `POST /api/payments/` — Payments.
* `GET /api/trainers/` — Trainer directory.
* `GET /api/workouts/` — Workout plans.
* `GET /api/dashboard/stats/` — System executive stats.

---

## 🌐 GitHub Setup & Instructions

1. Initialize Git in the project root:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: Complete Gym Management System"
   ```

2. Link your GitHub repository and push:
   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/Gym-Management-System.git
   git branch -M main
   git push -u origin main
   ```

*(Ensure `.env` and `db.sqlite3` are not pushed to public repositories as configured in `.gitignore`.)*

---

## ☁️ Vercel Production Deployment

The project contains a preconfigured `vercel.json` for seamless serverless deployment.

### Vercel Deployment Steps:

1. Push your project to GitHub.
2. Log in to [Vercel](https://vercel.com) and click **Add New Project**.
3. Import your `Gym-Management-System` GitHub repository.
4. Set **Framework Preset** to **Other**.
5. Add the following **Environment Variables** in Vercel settings:

   | Variable | Value Example |
   | :--- | :--- |
   | `SECRET_KEY` | `your-secure-production-secret-key` |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `.vercel.app` |
   | `CSRF_TRUSTED_ORIGINS` | `https://your-project.vercel.app` |
   | `DATABASE_URL` | `postgres://user:pass@ep-server.postgres.database.azure.com:5432/gymdb` |

6. Deploy! Vercel will automatically build the WSGI application and serve static assets via WhiteNoise.
