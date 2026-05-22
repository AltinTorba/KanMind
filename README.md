# KanMind Backend API

## 📌 Project Overview

KanMind is a Kanban-style backend API built with Django and Django REST Framework.

The project provides a complete multi-user task and board management system with authentication, authorization, board collaboration, task assignment, commenting functionality, and secure user-scoped access control.

The backend follows RESTful API principles and is designed to integrate with an existing frontend application.

---

# 🏗️ Tech Stack

* Python
* Django
* Django REST Framework
* DRF Token Authentication
* SQLite

---

# 📁 Project Architecture

## Applications

### auth_app

Handles:

* registration
* login
* token authentication
* email validation

### kanban_app

Handles:

* board management
* board membership
* board statistics
* board ownership

### tasks_app

Handles:

* task management
* task assignments
* task reviews
* comments system

---

# 🔐 Authentication

The API uses DRF Token Authentication.

Protected endpoints require:

Authorization: Token <your_token>

---

# 👤 User Features

Users can:

* register
* login
* receive authentication tokens
* create boards
* join boards as members
* create and manage tasks
* assign reviewers and assignees
* create and delete comments
* access only authorized resources

---

# 📡 API Endpoints

# 🔑 Authentication

| Method | Endpoint                                                      | Description                   |
| ------ | ------------------------------------------------------------- | ----------------------------- |
| POST   | /api/registration/                                            | Register new user             |
| POST   | /api/login/                                                   | Login and receive token       |
| GET    | /api/email-check/?email=[test@test.com](mailto:test@test.com) | Check whether an email exists |

---

# 📊 Boards

| Method | Endpoint          | Description            |
| ------ | ----------------- | ---------------------- |
| GET    | /api/boards/      | List accessible boards |
| POST   | /api/boards/      | Create board           |
| GET    | /api/boards/{id}/ | Retrieve board details |
| PATCH  | /api/boards/{id}/ | Update board           |
| DELETE | /api/boards/{id}/ | Delete board           |

---

# ✅ Tasks

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| GET    | /api/tasks/      | List accessible tasks |
| POST   | /api/tasks/      | Create task           |
| GET    | /api/tasks/{id}/ | Retrieve task         |
| PATCH  | /api/tasks/{id}/ | Update task           |
| DELETE | /api/tasks/{id}/ | Delete task           |

---

# 📌 Task Filters

| Method | Endpoint                   | Description                                |
| ------ | -------------------------- | ------------------------------------------ |
| GET    | /api/tasks/assigned_to_me/ | Tasks assigned to authenticated user       |
| GET    | /api/tasks/reviewing/      | Tasks where authenticated user is reviewer |

---

# 💬 Comments

| Method | Endpoint                                    | Description            |
| ------ | ------------------------------------------- | ---------------------- |
| GET    | /api/tasks/{task_id}/comments/              | List comments for task |
| POST   | /api/tasks/{task_id}/comments/              | Create comment         |
| DELETE | /api/tasks/{task_id}/comments/{comment_id}/ | Delete comment         |

---

# 🧠 Core Business Logic

## Board Access Logic

Boards are only visible if the authenticated user:

* is the owner
* or is a board member

---

## Task Access Logic

Tasks are only visible if the authenticated user belongs to the related board.

---

## Task Creation Rules

Only board members are allowed to create tasks inside a board.

---

## Comment Rules

Comments belong to tasks and contain:

* author
* content
* timestamp

---

# 🧩 Data Models

## Board

* title
* owner
* members

### Additional Statistics

* member_count
* ticket_count
* tasks_to_do_count
* tasks_high_prio_count

---

## Task

* title
* description
* status
* priority
* due_date
* assignee
* reviewer
* board

---

## Comment

* task
* author
* content
* created_at

---

# 🔐 Permissions & Security

## Authentication Layer

* IsAuthenticated permissions for protected routes

## Membership Filtering

Users can only access:

* boards they belong to
* tasks inside accessible boards

## Ownership Logic

Board ownership is automatically assigned during creation.

## Secure Querysets

All querysets are filtered per authenticated user.

---

# ⚡ Features Implemented

## Authentication System

* registration
* login
* token generation
* password hashing

## Board System

* board CRUD
* member management
* board statistics
* ownership structure

## Task System

* task CRUD
* assignee workflow
* reviewer workflow
* due dates
* filtered endpoints

## Comment System

* create comments
* delete comments
* task-related comments

## Serializer Enhancements

* nested mini user serializers
* custom computed fields
* mentor-compatible response structures

---

# 📊 Example Board Response

```json
[
  {
    "id": 11,
    "title": "Test Board",
    "member_count": 1,
    "ticket_count": 5,
    "tasks_to_do_count": 5,
    "tasks_high_prio_count": 5,
    "owner_id": 12
  }
]
```

---

# ⚙️ Setup Instructions

## 1. Clone Repository

```bash
git clone <repository_url>
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Apply Migrations

```bash
python manage.py migrate
```

---

## 6. Start Development Server

```bash
python manage.py runserver
```

---

# 🧪 API Testing

The API was tested using:

* Postman
* Browser DevTools
* Existing frontend integration

---

# 🗄️ Database

Default database:

* SQLite

---

# 🏛️ Architectural Overview

The project follows a layered REST architecture:

* Authentication Layer
* Authorization Layer
* Business Logic Layer
* Serializer Layer
* ORM Data Layer

The system emphasizes:

* secure user-scoped data access
* modular architecture
* maintainable REST patterns
* frontend-compatible API responses
