# 🏢 Leave Management System – Automation Project

An internal **Leave Management System** built as an **Automation Engineer technical assessment for Harri – Palestine**.

The system provides employee and leave management, approval workflows, automated background tasks, reporting, and AI-powered recommendations.

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
* [Celery & Background Tasks](#-celery--background-tasks)
* [API Testing](#-api-testing)

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
* Background task processing with **Celery**
* AI-powered recommendations using **Groq**
* Automated daily reporting
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
* Get AI-powered approval recommendations

### ⚡ Automation

* Emergency leave auto-approval
* Automated daily reports
* Scheduled background tasks
* Automatic evaluation of pending leave requests
* AI-generated summaries
* Background task processing using Celery

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
                                  Groq AI      Celery
                                      │
                                      ▼
                                AI Analysis

                            │
                            ▼
                     ┌─────────────┐
                     │    MySQL    │
                     └─────────────┘
```

### Main Components

| Component             | Responsibility                        |
| --------------------- | ------------------------------------- |
| Django                | Core backend application              |
| Django REST Framework | REST API layer                        |
| Employees App         | Employee and leave request management |
| Automation Module     | Automated workflows and reporting     |
| Groq AI               | AI summaries and recommendations      |
| Celery                | Background task processing            |
| MySQL                 | Persistent data storage               |
| Postman               | API testing                           |
| Docker                | Containerization                      |

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
        AI Evaluation
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

### Automation & AI

| Technology | Purpose                                    |
| ---------- | ------------------------------------------ |
| Groq       | AI / LLM integration                       |
| Llama      | AI model for recommendations and summaries |
| Celery     | Background task processing                 |
| Redis      | Celery message broker / result backend     |

### Libraries

| Library               | Purpose                         |
| --------------------- | ------------------------------- |
| `django-cors-headers` | CORS handling                   |
| `python-dotenv`       | Environment variable management |
| `groq`                | Groq API client                 |
| `celery`              | Background task processing      |

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
* Redis (required for Celery background tasks)

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

If the project dependencies have not been installed yet, the main packages include:

```bash
pip install django djangorestframework pymysql python-dotenv groq celery redis django-cors-headers
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

> For production environments, use strong database credentials and never commit them to GitHub.

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

GROQ_API_KEY=gsk_your_api_key_here
GROQ_MODEL=your-groq-model
```

> Never commit `.env` to GitHub.

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

## ⚙️ Workflow & Automation Endpoints

| Method | Endpoint                                  | Description                             |
| ------ | ----------------------------------------- | --------------------------------------- |
| `POST` | `/leave-requests/{id}/approve/`           | Approve a leave request                 |
| `POST` | `/leave-requests/{id}/reject/`            | Reject a leave request                  |
| `GET`  | `/leave-requests/summary/`                | Generate AI-powered summary             |
| `GET`  | `/leave-requests/{id}/ai_recommendation/` | Get AI recommendation                   |
| `POST` | `/leave-requests/auto_evaluate/`          | Automatically evaluate pending requests |
| `POST` | `/leave-requests/send_report/`            | Send daily report                       |
| `POST` | `/leave-requests/auto_approve_emergency/` | Auto-approve emergency leaves           |

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

Example:

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

## 7. Auto-Evaluate Pending Requests

```http
POST /api/leave-requests/auto_evaluate/
```

Example:

```bash
curl -X POST \
http://127.0.0.1:8000/api/leave-requests/auto_evaluate/
```

---

# 🤖 Automation & AI

The project combines automated workflows, AI-powered analysis, and background processing.

## 🤖 AI Integration with Groq

The project uses **Groq** for AI-powered features.

Groq provides a fast API for running large language models and is used in this project to analyze leave requests and generate recommendations.

### AI Features

| Feature                     | Description                                    | Endpoint                                          |
| --------------------------- | ---------------------------------------------- | ------------------------------------------------- |
| **Request Summary**         | AI-generated summary of pending leave requests | `GET /api/leave-requests/summary/`                |
| **Approval Recommendation** | AI recommendation for a specific request       | `GET /api/leave-requests/{id}/ai_recommendation/` |
| **Auto Evaluation**         | Automatic evaluation of pending requests       | `POST /api/leave-requests/auto_evaluate/`         |

### AI Workflow

```text
Employee submits leave request
           │
           ▼
      AI Analysis
           │
     ┌─────┴─────┐
     ▼           ▼
Emergency      Normal
≤ 2 days       > 2 days
     │           │
     ▼           ▼
Auto-Approve   AI Recommendation
                   │
                   ▼
              Manager Review
```

### AI Configuration

Add the following variables to `.env`:

```env
GROQ_API_KEY=gsk_your_api_key_here
GROQ_MODEL=your-groq-model
```

Install the Groq Python client:

```bash
pip install groq
```

### AI Integration Files

```text
automation/
├── groq_client.py
└── ai_integration.py
```

### Testing AI Features

Open the Django shell:

```bash
python manage.py shell
```

Then:

```python
from automation.ai_integration import summarize_pending_requests

summary = summarize_pending_requests()

print(summary)
```

### Example AI Response

```json
{
    "recommendation": "APPROVE",
    "reasoning": "Employee has a valid reason and the requested duration is reasonable.",
    "risk_level": "LOW",
    "suggested_action": "Approve the request"
}
```

> AI recommendations are decision-support features and should not replace appropriate managerial review.

---

## 📊 Automated Reporting

The project supports automated reporting, including:

* Daily leave reports
* Weekly leave summaries
* Department-wise leave breakdowns
* Leave request statistics
* AI-generated summaries

A custom Django management command is available:

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

---

# ⚡ Celery & Background Tasks

The project uses **Celery** for background task processing.

Celery allows long-running and scheduled operations to execute outside the main Django request cycle.

### Background Tasks

* Automated daily reports
* Emergency leave auto-approval
* AI summary generation
* Automated pending-request evaluation
* Email notifications ready for integration

---

## ⏰ Celery Beat Schedule

| Task                     | Schedule             | Description                         |
| ------------------------ | -------------------- | ----------------------------------- |
| `send_daily_report`      | Every day at 9:00 AM | Sends daily leave report            |
| `auto_approve_emergency` | Every 30 minutes     | Processes eligible emergency leaves |
| `generate_ai_summary`    | Every day at 5:00 PM | Generates AI-powered summary        |

> The exact schedules depend on the Celery Beat configuration in the project.

---

## ▶️ Running Celery

### Start the Celery Worker

```bash
python -m celery -A core worker --loglevel=info --pool=solo
```

### Start Celery Beat

Open another terminal:

```bash
python -m celery -A core beat --loglevel=info
```

Both the worker and Beat scheduler should be running for scheduled background tasks to execute.

---

## 🧪 Running Tasks Manually

Open the Django shell:

```bash
python manage.py shell
```

Then:

```python
from automation.tasks import (
    send_daily_report,
    auto_approve_emergency,
    generate_ai_summary
)

send_daily_report.delay()
auto_approve_emergency.delay()
generate_ai_summary.delay()
```

---

## ⚙️ Celery Configuration

Example configuration:

```python
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_TIMEZONE = "UTC"
```

For local development without Redis, Celery can be configured differently, but a real message broker such as **Redis** is recommended for actual background processing.

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
8. Test Auto Evaluation
        ↓
9. Test Background Tasks
```
