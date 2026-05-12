# KanMind Backend API

## 📌 Project Description
KanMind is a backend API built with Django and Django REST Framework.  
It provides functionality for managing boards, tasks, and comments.

---

## 🏗️ Tech Stack
- Python
- Django
- Django REST Framework
- SQLite

---

## 📁 Project Structure
- auth_app → authentication (login/register)
- kanban_app → boards management
- tasks_app → tasks and comments

---

## 🧠 Core Features (in progress)
- User registration & login (token authentication)
- Board creation with owner and members
- Task management inside boards
- Comments on tasks

---

## 🗄️ Database
Default SQLite database is used:
- db.sqlite3

---

## ⚙️ Current Models
### Board
- title
- owner (ForeignKey → User)
- members (ManyToMany → User)

---

## 🚀 Setup Instructions
(To be completed later)
