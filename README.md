# 🏢 Leave Management System – Automation Project

An internal **Leave Management System** built as an **Automation Engineer technical assessment for Harri – Palestine**.

The system provides employee and leave management, approval workflows, automated operations, reporting, and AI-powered recommendations.

---

## 📖 Table of Contents

* [Overview](#-overview)
* [Features](#-features)
* [System Architecture](#️-system-architecture)
* [Leave Request Workflow](#-leave-request-workflow)
* [Technology Stack](#️-technology-stack)
* [Installation](#-installation)
* [Authentication](#-authentication)
* [API Endpoints](#-api-endpoints)
* [Example API Requests](#-example-api-requests)
* [Automation & AI](#-automation--ai)
* [API Testing](#-api-testing)
* [Deployment](#-deployment)
* [Production Security](#-production-security)
* [Project Status](#-project-status)

---

## 🎯 Overview

The **Leave Management System** is a Django-based internal automation platform designed to simplify and automate employee leave management.

The project demonstrates practical experience with:

* Backend development using **Django**
* REST API development using **Django REST Framework**
* Relational database design using **MySQL**
* Employee and leave request management
* Approval and rejection workflows
* Automated leave processing
* AI-powered recommendations
* Automated daily reporting
* RESTful API architecture
* Environment-based configuration
* Docker-based deployment

---

## ✨ Features

### 👥 Employee Management

* Create employees
* View employee details
* Update employee information
* Delete employees
* Department and position management
* Employee hire-date tracking
* Contact information management

### 📝 Leave Request Management

* Create leave requests
* View leave requests
* Update leave requests
* Delete leave requests
* Track leave type
* Track start and end dates
* Track request status
* Store leave reasons

### 🔄 Approval Workflow

Leave requests follow a simple status workflow:

```text
PENDING
   │
   ├──► APPROVED
   │
   └──► REJECTED
```

Managers can:

* Review leave requests
* Approve leave requests
* Reject leave requests
* Get AI-powered recommendations

---

## 🏗️ System Architecture

```text
                    ┌─────────────────┐
                    │     Client      │
                    │  Postman / API  │
                    └────────┬────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │ Django REST Framework │
                 └──────────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        Employees      Leave Requests   Automation
                                      │
                         ┌────────────┼────────────┐
                         │            │            │
                         ▼            ▼            ▼
                    Approval     Auto-Approve    Reporting
                    Workflow     Emergency       │
                                      │           │
                                      ▼           ▼
                                  AI / LLM    Daily Reports

                            │
                            ▼
                     ┌─────────────┐
                     │    MySQL    │
                     └─────────────┘
```

### Main Components

| Component             | Responsibility                           |
| --------------------- | ---------------------------------------- |
| Django                | Core backend application                 |
| Django REST Framework | REST API layer                           |
| Employees App         | Employee and leave request management    |
| Automation Module     | Automated workflows and reporting        |
| AI Integration        | AI-powered summaries and recommendations |
| MySQL                 | Persistent data storage                  |
| Postman               | API testing                              |
| Docker                | Containerized application deployment     |

---

## 🔄 Leave Request Workflow

```text
Employee
   │
   ▼
Submit Leave Request
   │
   ▼
Check Request
   │
   ├── Emergency Leave ≤ 2 Days
   │          │
   │          ▼
   │     Auto Approval
   │
   └── Normal Leave
              │
              ▼
        Manager Review
              │
        ┌─────┴─────┐
        ▼           ▼
    APPROVED     REJECTED
```

### Emergency Leave Automation

Emergency leave requests with a duration of **2 days or less** can be automatically approved.

Requests exceeding 2 days follow the normal manager approval workflow.

---

## 🛠️ Technology Stack

### Backend

| Technology            | Version | Purpose              |
| --------------------- | ------: | -------------------- |
| Python                |   3.12+ | Programming Language |
| Django                |     6.1 | Web Framework        |
| Django REST Framework |    3.18 | REST API Development |
| MySQL                 |     9.0 | Database             |
| PyMySQL               |     1.2 | MySQL Connector      |

### Libraries

| Library               | Purpose                         |
| --------------------- | ------------------------------- |
| `django-cors-headers` | CORS handling                   |
| `python-dotenv`       | Environment variable management |
| `openai`              | AI / LLM integration            |

### Development Tools

| Tool            | Purpose             |
| --------------- | ------------------- |
| Git             | Version Control     |
| GitHub          | Code Hosting        |
| Postman         | API Testing         |
| MySQL Workbench | Database Management |
| Docker          | Containerization    |

---

# 🚀 Installation

## Prerequisites

Make sure the following are installed:

* Python 3.12+
* MySQL 9.0+
* Git
* pip
* Virtual Environment

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/WafaaAlshaikh/automation-project-.git
cd automation-project-
```

---

## Step 2: Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Configure MySQL

Open MySQL and create the database:

```sql
CREATE DATABASE automation_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Create the database user:

```sql
CREATE USER 'django_user'@'localhost'
IDENTIFIED BY 'your-secure-password';
```

Grant permissions:

```sql
GRANT ALL PRIVILEGES
ON automation_db.*
TO 'django_user'@'localhost';

FLUSH PRIVILEGES;
```

> For production environments, use a strong database password and never commit credentials to GitHub.

---

## Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here

DATABASE_NAME=automation_db
DATABASE_USER=django_user
DATABASE_PASSWORD=your-secure-password
DATABASE_HOST=localhost
DATABASE_PORT=3306

OPENAI_API_KEY=your-openai-key-here
```

The `OPENAI_API_KEY` is optional if AI functionality is not enabled.

> Never commit the `.env` file to GitHub.

---

## Step 6: Run Database Migrations

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

---

## Step 7: Create Test Data

Populate the database using:

```bash
python manage.py shell < create_test_data.py
```

Or:

```bash
python create_test_data.py
```

---

## Step 8: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

API base URL:

```text
http://127.0.0.1:8000/api/
```

---

# 🔐 Authentication

The project currently supports:

* Session Authentication
* Basic Authentication

The architecture can be extended with JWT authentication in future iterations.

For production environments, authentication and authorization should be properly configured.

---

# 📡 API Endpoints

Base URL:

```text
http://127.0.0.1:8000/api/
```

---

## 👥 Employee Endpoints

| Method   | Endpoint           | Description               |
| -------- | ------------------ | ------------------------- |
| `GET`    | `/employees/`      | List all employees        |
| `POST`   | `/employees/`      | Create an employee        |
| `GET`    | `/employees/{id}/` | Get employee details      |
| `PUT`    | `/employees/{id}/` | Update employee           |
| `PATCH`  | `/employees/{id}/` | Partially update employee |
| `DELETE` | `/employees/{id}/` | Delete employee           |

---

## 📝 Leave Request Endpoints

| Method   | Endpoint                | Description               |
| -------- | ----------------------- | ------------------------- |
| `GET`    | `/leave-requests/`      | List all leave requests   |
| `POST`   | `/leave-requests/`      | Create leave request      |
| `GET`    | `/leave-requests/{id}/` | Get leave request details |
| `PUT`    | `/leave-requests/{id}/` | Update leave request      |
| `DELETE` | `/leave-requests/{id}/` | Delete leave request      |

---

## ⚙️ Custom Workflow Endpoints

| Method | Endpoint                                  | Description                   |
| ------ | ----------------------------------------- | ----------------------------- |
| `POST` | `/leave-requests/{id}/approve/`           | Approve a leave request       |
| `POST` | `/leave-requests/{id}/reject/`            | Reject a leave request        |
| `GET`  | `/leave-requests/summary/`                | Generate AI-powered summary   |
| `GET`  | `/leave-requests/{id}/ai_recommendation/` | Get AI recommendation         |
| `POST` | `/leave-requests/send_report/`            | Send daily report             |
| `POST` | `/leave-requests/auto_approve_emergency/` | Auto-approve emergency leaves |

---

# 📌 Example API Requests

## 1. Create Employee

### Request

```http
POST /api/employees/
Content-Type: application/json
```

### Body

```json
{
    "user": 1,
    "department": "Engineering",
    "position": "Software Engineer",
    "hire_date": "2024-01-15",
    "phone_number": "0599123456"
}
```

---

## 2. Create Leave Request

### Request

```http
POST /api/leave-requests/
Content-Type: application/json
```

### Body

```json
{
    "employee": 1,
    "leave_type": "ANNUAL",
    "start_date": "2024-01-20",
    "end_date": "2024-01-23",
    "reason": "Family vacation"
}
```

---

## 3. Approve Leave Request

```http
POST /api/leave-requests/1/approve/
```

Example using cURL:

```bash
curl -X POST \
http://127.0.0.1:8000/api/leave-requests/1/approve/
```

---

## 4. Reject Leave Request

```http
POST /api/leave-requests/1/reject/
```

Example:

```bash
curl -X POST \
http://127.0.0.1:8000/api/leave-requests/1/reject/
```

---

## 5. Get AI Summary

```http
GET /api/leave-requests/summary/
```

Example:

```bash
curl http://127.0.0.1:8000/api/leave-requests/summary/
```

---

## 6. Get AI Recommendation

```http
GET /api/leave-requests/1/ai_recommendation/
```

Example:

```bash
curl http://127.0.0.1:8000/api/leave-requests/1/ai_recommendation/
```

---

# 🤖 Automation & AI

The system combines automated workflows, reporting, and AI-powered capabilities.

## AI Features

The system supports:

* AI-powered leave request summaries
* AI-powered approval recommendations
* Smart insights for managers
* Leave request analysis

The AI integration is implemented in:

```text
automation/
└── ai_integration.py
```

### AI Processing Flow

```text
Leave Requests
      │
      ▼
AI Analysis
      │
      ├──► Summary
      │
      ├──► Recommendation
      │
      └──► Manager Insights
```

---

## ⚡ Automated Workflows

The system includes:

* Emergency leave auto-approval for requests of **2 days or less**
* Automated daily reports
* Scheduled reporting through Django management commands
* Automated leave processing
* AI-powered request analysis

---

## 📊 Reporting

The system supports:

* Daily leave reports
* Weekly leave summaries
* Department-wise leave breakdowns
* Leave request statistics
* AI-generated summaries

---

## 🤖 AI Configuration

To enable AI functionality, add your OpenAI API key to `.env`:

```env
OPENAI_API_KEY=your-openai-key-here
```

AI functionality is optional and the system can operate without an OpenAI API key.

---

## 📅 Daily Reporting

The project includes a custom Django management command:

```text
automation/
└── management/
    └── commands/
        └── send_daily_report.py
```

Run the report manually:

```bash
python manage.py send_daily_report
```

The reporting workflow can be integrated with scheduling tools such as:

* Linux Cron
* Windows Task Scheduler
* Cloud Scheduler
* CI/CD pipelines
* Celery / Celery Beat

---

# 🧪 API Testing

The API can be tested manually using **cURL** or **Postman**.

## Test Data

```bash
python create_test_data.py
```

---

## Get Employees

```bash
curl http://127.0.0.1:8000/api/employees/
```

---

## Get Leave Requests

```bash
curl http://127.0.0.1:8000/api/leave-requests/
```

---

## Approve Leave Request

```bash
curl -X POST \
http://127.0.0.1:8000/api/leave-requests/1/approve/
```

---

## Reject Leave Request

```bash
curl -X POST \
http://127.0.0.1:8000/api/leave-requests/1/reject/
```

---

## Postman Testing Flow

```text
1. Create Employee
        ↓
2. Create Leave Request
        ↓
3. Get Leave Request
        ↓
4. Test Update / Delete
        ↓
5. Test Approve / Reject
        ↓
6. Test AI Recommendation
        ↓
7. Test AI Summary
        ↓
8. Test Automation
```

---

# 🚢 Deployment

## Docker

The project can be containerized using Docker.

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Build the Docker Image

```bash
docker build -t automation-project .
```

### Run the Container

```bash
docker run -p 8000:8000 automation-project
```

The application will then be available at:

```text
http://127.0.0.1:8000/
```

> The Docker configuration above uses Django's development server. For production deployments, use Gunicorn with a production-ready reverse proxy such as Nginx.

---

# 🔒 Production Security

Before deploying to production:

* [ ] Set `DEBUG=False`
* [ ] Use a strong Django `SECRET_KEY`
* [ ] Never commit `.env`
* [ ] Use strong database credentials
* [ ] Configure `ALLOWED_HOSTS`
* [ ] Configure HTTPS
* [ ] Use proper authentication and authorization
* [ ] Replace `AllowAny` with appropriate permissions
* [ ] Configure CORS securely
* [ ] Use Gunicorn or another production WSGI server
* [ ] Configure Nginx or another reverse proxy
* [ ] Configure database backups
* [ ] Store API keys securely

---

# 📊 Project Status

**Status:** Completed ✅

This project was developed as an **Automation Engineer technical assessment for Harri – Palestine**.

### Implemented Areas

* Employee management
* Leave request management
* RESTful API endpoints
* Approval and rejection workflows
* Emergency leave automation
* AI-powered recommendations
* AI-powered summaries
* Daily reporting
* MySQL database integration
* Environment-based configuration
* Docker support

---

## ⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub!
