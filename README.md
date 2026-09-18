# Best Banking App

A modern, full-stack digital banking application built with the **FARM stack** (FastAPI, React, MongoDB, and Tailwind CSS). This platform provides secure, real-time banking operations including account management, deposits, withdrawals, and instant fund transfers.

---

## 🚀 Tech Stack

* **Backend:** FastAPI (Python 3.11+), Uvicorn, PyMongo, Pydantic
* **Frontend:** React, Vite, Tailwind CSS, shadcn/ui
* **Database:** MongoDB / MongoDB Atlas
* **Authentication:** JWT (JSON Web Tokens) with BCrypt password hashing
* **Package Management:** `uv` (Python), `npm` (Node.js)

---

## 🛠️ Features

* **User Authentication:** Secure user registration, login, and stateless JWT authorization.
* **Account Management:** View account balances, details, and create new bank accounts.
* **Banking Operations:** Perform real-time deposits, withdrawals, and peer-to-peer transfers.
* **Transaction History:** Instant lookup and audit trail for user activity.
* **Interactive API Docs:** Built-in OpenAPI / Swagger documentation for backend testing.

---

## 💻 Local Development Setup

### Prerequisites

* [Python 3.11+](https://www.python.org/)
* [Node.js (v18+)](https://nodejs.org/) & `npm`
* [MongoDB](https://www.mongodb.com/) (running locally or a MongoDB Atlas connection string)
* [`uv`](https://docs.astral.sh/uv/) package manager

---

### 1. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Sync dependencies using uv
uv sync

# Create a .env file and configure your variables
echo 'MONGODB_URI="mongodb://localhost:27017/banking_db"' > .env
echo 'SECRET_KEY="your-super-secret-jwt-key"' >> .env

# Run the FastAPI server
uv run uvicorn app:app --reload
