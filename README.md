# KanMind Backend API

## 📌 Project Description
KanMind is a backend API built with Django and Django REST Framework.

The project provides authentication, board management, and task management functionality for a Kanban-style productivity system.

---

## 🏗️ Tech Stack
- Python
- Django
- Django REST Framework
- DRF Token Authentication
- SQLite

---

## 📁 Project Structure
- auth_app → authentication system
- kanban_app → boards management
- tasks_app → tasks and comments

---

## 🔐 Authentication
The API uses Token Authentication.

Users can:
- register
- login
- receive authentication tokens
- access protected endpoints

---

## 📡 Current API Endpoints

### Authentication
- POST `/api/auth/register/`
- POST `/api/auth/login/`

### Boards
- GET `/api/boards/`
- POST `/api/boards/`
- PUT `/api/boards/<id>/`
- DELETE `/api/boards/<id>/`

---

## 🔑 Authorization Example

```http
Authorization: Token your_token_here
```

---

## 🗄️ Current Models

### Board
- title
- owner (ForeignKey → User)
- members (ManyToMany → User)

---

## ✅ Implemented Features
- User registration
- User login
- Password hashing
- Token authentication
- Protected API endpoints
- Board CRUD operations

---

## 🚧 Features In Progress
- Task model
- Task CRUD
- Comments system
- Board permissions
- User-specific board filtering

---

## ⚙️ Setup Instructions

### 1. Clone repository
```bash
git clone <repository_url>
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

#### Windows
```bash
venv\Scripts\activate
```

#### Linux / macOS
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Start development server
```bash
python manage.py runserver
```

---

## 🧪 API Testing
API endpoints can be tested using:
- Postman
- Insomnia
- cURL

---

## 🗄️ Database
Default SQLite database:
- `db.sqlite3`
