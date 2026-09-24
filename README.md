# 📚 Liane's Library Management System

A personal library management system built with **Python**, **MySQL** and **Streamlit**. Features book tracking, friend management, loan tracking with automatic fines, trust scores, wishlist and reviews. Database connected to Python using **SQLAlchemy** and deployed using **Docker**.

---

## 🚀 Features

- 🔐 **Secure Login** — Username and password protected
- 📖 **Book Management** — Add, update, remove and search books by genre or mood tag
- 👥 **Friend Management** — Track borrowers with trust scores and preferred genres
- 📋 **Loan Tracking** — Every loan gets a unique Tracker ID (e.g. LIB-000001)
- 💰 **Automatic Fines** — Calculated live at £0.50 per day overdue
- 🔄 **Loan Renewal** — Extend due dates with renewal tracking
- 🎁 **Wishlist** — Friends can request books Liane doesn't own yet
- ⭐ **Reviews** — Star ratings and written reviews after reading
- 📊 **Dashboard** — Live overview of books, loans, overdue and unpaid fines

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| MySQL | Database |
| Streamlit | Web interface |
| SQLAlchemy | Python-MySQL connection |
| PyMySQL | MySQL driver |
| Docker | Containerisation |
| Docker Compose | Multi-container orchestration |

---

## 🗄️ Database Schema

Six tables designed with normalisation principles:

| Table | Description |
|---|---|
| `books` | Book collection with condition and mood tags |
| `friends` | Borrowers with trust scores and preferred genres |
| `loans` | Loan records with tracker ID, due date, renewal date and fines |
| `reviews` | Star ratings and written reviews per loan |
| `wishlist` | Book requests from friends |

### Innovative Features in the Schema
- **Trust Score** — starts at 100, drops for late or damaged returns
- **Mood Tags** — tag books as cosy, dark, inspiring etc. for recommendations
- **Tracker ID** — unique ID per loan (LIB-000001) for status tracking
- **Live Fine Calculation** — fines calculated in real time, not just on return

---

## 🐳 Running with Docker

### Prerequisites
- Docker Desktop installed and running

### Steps

**1 — Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/Liane-s-Library-Management-System.git
cd Liane-s-Library-Management-System
```

**2 — Create your .env file**
```bash
cat > src/.env << EOF
MYSQL_HOST=db
MYSQL_PASSWORD=liane123
LIBRARY_USERNAME=liane
LIBRARY_PASSWORD=liane123
EOF
```

**3 — Add your database export**

Export your MySQL database and place it in the root folder:
```bash
mysqldump -u root -p lianes_library > lianes_library.sql
```

**4 — Build and run**
```bash
docker compose up --build
```

**5 — Open in browser**
```
http://localhost:8501
```

**Login credentials:**
- Username: `liane`
- Password: `liane123`

---

## 📁 Project Structure

```
lianes-library-app/
  ├── Dockerfile
  ├── docker-compose.yml
  ├── .dockerignore
  ├── .gitignore
  ├── README.md
  └── src/
       ├── app.py
       └── requirements.txt
```

---

## 🔧 Useful Docker Commands

| Command | What it does |
|---|---|
| `docker compose up --build` | Build and start everything |
| `docker compose up -d` | Run in background |
| `docker compose down` | Stop everything |
| `docker compose down -v` | Stop and delete database volume |
| `docker compose logs app` | See app logs |
| `docker compose logs db` | See database logs |

---

## 📸 App Pages

| Page | Description |
|---|---|
| 📊 Dashboard | Live summary of books, loans, overdue and fines |
| 📖 Books | Browse, filter, add, update and remove books |
| 👥 Friends | Manage borrowers and trust scores |
| 📋 Active Loans | See all current loans with overdue status |
| ➕ Lend a Book | Record a new loan with due date |
| 📬 Return a Book | Mark books as returned with condition |
| 🔍 Track a Loan | Look up any loan by tracker ID |
| 🔄 Renew a Loan | Extend loan deadlines |
| ⭐ Leave a Review | Rate and review books |
| 🎁 Wishlist | Manage book requests |

---

## 👨‍💻 Built By

Shyam Sunder Chiliveri
WBS Coding School — Data Science & AI Programme

---

## 📄 License

This project is for educational purposes.
