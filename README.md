# KanMind Backend API

## 📌 Project Description
KanMind is a backend API built with Django and Django REST Framework.

The project provides authentication, board management, and task management functionality for a Kanban-style productivity system.

It implements a multi-user architecture with authentication, authorization, and user-scoped data access.

---

## 🏗️ Tech Stack
- Python
- Django
- Django REST Framework
- DRF Token Authentication
- SQLite

---

## 📁 Project Structure
- auth_app → authentication system (registration/login/token)
- kanban_app → boards management system
- tasks_app → tasks and comments system

---

## 🔐 Authentication
The API uses Token Authentication.

All protected endpoints require:

Authorization: Token <your_token>

Users can:
- register
- login
- receive authentication tokens
- access protected endpoints

---

## 📡 API Endpoints

### 🔑 Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/registration/ | Register new user |
| POST | /api/login/ | Login and receive token |

---

### 📊 Boards

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/boards/ | List boards |
| POST | /api/boards/ | Create board |
| PUT/PATCH | /api/boards/<id>/ | Update board |
| DELETE | /api/boards/<id>/ | Delete board |

---

### ✅ Tasks

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/tasks/ | List user-accessible tasks |
| POST | /api/tasks/ | Create task (board member only) |
| GET | /api/tasks/<id>/ | Retrieve task |
| PUT/PATCH | /api/tasks/<id>/ | Update task |
| DELETE | /api/tasks/<id>/ | Delete task |

---

## 🔐 Authorization Model

The system implements a multi-layer security architecture:

### 1. Authentication Layer
- IsAuthenticated required for all protected endpoints

### 2. Read Access Control
Tasks are filtered per authenticated user:

board__members=self.request.user

### 3. Write Access Control
Task creation is restricted to board members only:

if self.request.user not in board.members.all():
    raise PermissionError("Not allowed")

---

## 🧠 Business Logic

### Board Model
- title
- owner (ForeignKey → User)
- members (ManyToMany → User)

### Task Model
- title
- description
- status
- board (ForeignKey → Board)
- assignee (optional ForeignKey → User)

---

## 🔑 Authentication Example

Authorization: Token your_token_here

---

## ⚙️ Key Features Implemented

### Authentication System
- User registration
- Login with token generation
- Password hashing (Django built-in)
- Secure authentication flow

### Board System
- Board CRUD operations
- Owner-based structure
- Member relationships

### Task System
- Full CRUD operations
- User-scoped queryset filtering
- Board membership validation
- Secure task creation rules

---

## 🚧 Future Improvements
- Role-based access control (Owner / Member / Admin)
- Task assignment (assignee workflow)
- Task status workflow (Kanban stages)
- Comments system
- Activity logging / audit trail

---

## ⚙️ Setup Instructions

### 1. Clone repository
git clone <repository_url>

### 2. Create virtual environment
python -m venv venv

### 3. Activate virtual environment

Windows:
venv\Scripts\activate

Linux / macOS:
source venv/bin/activate

### 4. Install dependencies
pip install -r requirements.txt

### 5. Run migrations
python manage.py migrate

### 6. Start server
python manage.py runserver

---

## 🧪 API Testing Tools
- Postman
- Insomnia
- cURL

---

## 🗄️ Database
Default SQLite database:
- db.sqlite3

---

## 📌 Architecture Summary

This project follows a RESTful layered architecture:

- Authentication layer (Token-based)
- Authorization layer (Permissions + membership checks)
- Business logic layer (ViewSets + serializers)
- Data access layer (ORM filtering per user)