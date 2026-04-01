# AI-Based Smart Inventory & Demand Prediction System (Production)

A professional, monolithic Flask web application built for industrial inventory management and AI-driven demand forecasting.

## 🚀 Features
- **User Authentication**: Secure Login/Register system for Admins and Viewers.
- **Inventory Management**: Add products, track stock levels, and set reorder points.
- **AI Demand Forecasting**: Integrated Linear Regression model to predict future demand.
- **Interactive Dashboard**: Health KPIs and dynamic visualizations using Chart.js.
- **Alert System**: Visual cues for low-stock and high-demand items.

## 🛠️ Tech Stack
- **Backend**: Flask 3.0, SQLAlchemy ORM
- **Database**: MySQL (Production Ready)
- **Frontend**: HTML5, CSS3 (Modern UI), Chart.js
- **ML Engine**: Scikit-Learn (Linear Regression)

## 📦 Setup Instructions

### 1. Database Setup (MySQL)
1.  Create a MySQL database named `smart_inventory`.
2.  Update `app/config.py` with your MySQL credentials:
    ```python
    DB_USER = "your_user"
    DB_PASSWORD = "your_password"
    DB_HOST = "localhost"
    ```

### 2. Installation
1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate     # Windows
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Seed the database with sample data:
    ```bash
    python seed_db.py
    ```
4.  Run the application:
    ```bash
    python run.py
    ```
    Access at `http://localhost:5000`

## ☁️ Deployment Instructions (Render)

### Step 1: Connect GitHub
1.  Push this code to a Private/Public GitHub repository.
2.  Login to [Render.com](https://render.com) and create a **New Web Service**.

### Step 2: Configure Web Service
1.  **Runtime**: Python
2.  **Build Command**: `pip install -r requirements.txt`
3.  **Start Command**: `gunicorn run:app`

### Step 3: Set Environment Variables
In the Render Dashboard, go to **Environment** and add:
- `SECRET_KEY`: A long random string.
- `DATABASE_URL`: Your MySQL connection string (e.g., `mysql+pymysql://user:pass@host/db`).
- `FLASK_ENV`: `production`

### Step 4: Managed MySQL (Optional)
If you don't have a MySQL database, create a **New MySQL** on Render, then copy the internal Database URL and paste it into the `DATABASE_URL` environment variable of your web service.

---
**Developed by Ujjwal Mohanka | Senior Full-Stack & ML Engineer Simulation**
