# AI-Based Smart Inventory & Demand Prediction System

A production-ready full-stack web application that uses AI and machine learning to predict inventory demand, manage stock levels, and provide intelligent insights for procurement decisions.

![Tech Stack](https://img.shields.io/badge/React-18.2-blue)
![Tech Stack](https://img.shields.io/badge/Flask-3.0-green)
![Tech Stack](https://img.shields.io/badge/TailwindCSS-3.4-cyan)
![Tech Stack](https://img.shields.io/badge/Python-3.11-yellow)

## 🌟 Features

### 📊 AI-Powered Demand Forecasting

- **Machine Learning**: Linear Regression model trained on historical sales data
- **Feature Engineering**: Incorporates trends, seasonality, rolling averages, and lag features
- **Accuracy Metrics**: R² score and MAE for model evaluation
- **Smart Predictions**: Forecasts demand for 1-6 months ahead

### 📦 Inventory Management

- **Real-time Stock Tracking**: Monitor inventory levels across warehouses
- **Color-coded Alerts**: Visual indicators for low stock (red), warning (yellow), and good stock (green)
- **Inline Editing**: Update stock quantities directly from the table
- **CSV Export**: Download inventory reports for external analysis

### 💬 AI Chat Assistant

- **Powered by Claude Sonnet 4**: Context-aware chatbot for inventory insights
- **Natural Language**: Ask questions about stock levels, predictions, and procurement strategies
- **Actionable Recommendations**: Get data-driven suggestions for inventory optimization

### 📈 Sales Analytics

- **Sales Logging**: Record transactions with product, quantity, and date
- **Visual Analytics**: Bar charts showing monthly sales volume by product
- **Historical Data**: Track sales trends over 18+ months
- **Summary Reports**: Aggregate sales data by month and product

### 📋 Comprehensive Reports

- **Inventory Reports**: Complete snapshot with stock levels and locations
- **Sales Reports**: Monthly summaries by product
- **Low Stock Alerts**: Priority list of products requiring restock
- **CSV Downloads**: Export all reports for spreadsheet analysis

### 🔐 Secure Authentication

- **JWT-based Auth**: Secure token-based authentication
- **Role Management**: Admin and viewer roles with appropriate permissions
- **Session Persistence**: Auto-login with stored credentials

### 🎨 Modern UI/UX

- **Dark Mode Design**: Grafana/Vercel-inspired dark theme
- **Glassmorphism**: Beautiful backdrop blur effects
- **Responsive**: Mobile-friendly design with Tailwind CSS
- **Interactive Charts**: Recharts for beautiful data visualizations

## 🛠️ Tech Stack

### Frontend

- **React 18.2** - UI framework
- **Tailwind CSS 3.4** - Styling
- **Recharts 2.12** - Data visualization
- **Axios** - HTTP client
- **React Router** - Navigation
- **Vite** - Build tool

### Backend

- **Flask 3.0** - Python web framework
- **SQLAlchemy** - ORM
- **Flask-JWT-Extended** - Authentication
- **Flask-CORS** - Cross-origin requests

### AI/ML

- **scikit-learn 1.4** - Machine learning
- **pandas 2.2** - Data manipulation
- **NumPy 1.26** - Numerical computing
- **Anthropic Claude API** - AI chatbot

### Database

- **SQLite** - Lightweight database with SQLAlchemy ORM

## 📁 Project Structure

```
smart-inventory/
├── backend/
│   ├── app.py                  # Flask entry point
│   ├── config.py               # Configuration
│   ├── seed.py                 # Database seeding
│   ├── requirements.txt        # Python dependencies
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── inventory.py
│   │   ├── sales.py
│   │   └── prediction.py
│   ├── routes/                 # API endpoints
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── inventory.py
│   │   ├── sales.py
│   │   ├── prediction.py
│   │   ├── ai_chat.py
│   │   └── dashboard.py
│   └── ml/                     # Machine learning
│       ├── data_prep.py
│       ├── trainer.py
│       └── predictor.py
│
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── axios.js        # API client
    │   ├── components/         # Reusable components
    │   │   ├── Navbar.jsx
    │   │   ├── Sidebar.jsx
    │   │   ├── StatCard.jsx
    │   │   ├── DemandChart.jsx
    │   │   ├── StockTable.jsx
    │   │   ├── AIChat.jsx
    │   │   └── PredictionForm.jsx
    │   ├── pages/              # Route pages
    │   │   ├── Login.jsx
    │   │   ├── Dashboard.jsx
    │   │   ├── Inventory.jsx
    │   │   ├── Sales.jsx
    │   │   ├── Predictions.jsx
    │   │   └── Reports.jsx
    │   ├── context/
    │   │   └── AuthContext.jsx
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    └── tailwind.config.js
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **npm or yarn**

### Backend Setup

1. **Navigate to backend directory**

   ```bash
   cd backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Edit `backend/.env` file
   - Add your Anthropic API key (optional, for AI chat):
     ```
     ANTHROPIC_API_KEY=your_key_here
     ```

6. **Seed the database**

   ```bash
   python seed.py
   ```

7. **Start the Flask server**

   ```bash
   python app.py
   ```

   Server runs on: `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Start development server**

   ```bash
   npm run dev
   ```

   Frontend runs on: `http://localhost:5173`

### 🎯 Default Credentials

After seeding the database, use these credentials:

- **Admin Account**
  - Username: `admin`
  - Password: `admin123`
  - Role: Full access to all features

- **Viewer Account**
  - Username: `viewer`
  - Password: `viewer123`
  - Role: Read-only access

## 📚 API Documentation

### Authentication

- `POST /api/auth/login` - Login user
- `POST /api/auth/register` - Register new user
- `GET /api/auth/me` - Get current user

### Products

- `GET /api/products` - List all products
- `POST /api/products` - Create product
- `PUT /api/products/:id` - Update product
- `DELETE /api/products/:id` - Delete product

### Inventory

- `GET /api/inventory` - Get all inventory
- `GET /api/inventory/:product_id` - Get product inventory
- `PUT /api/inventory/:product_id` - Update stock quantity
- `GET /api/inventory/low-stock` - Get low stock alerts

### Sales

- `POST /api/sales` - Log a sale
- `GET /api/sales/:product_id` - Get product sales history
- `GET /api/sales/summary` - Get monthly sales summary
- `GET /api/sales/recent` - Get recent sales

### Predictions

- `POST /api/predict` - Generate demand prediction
- `GET /api/predict/history/:product_id` - Get prediction history

### AI Chat

- `POST /api/chat` - Chat with AI assistant

### Dashboard

- `GET /api/dashboard/stats` - Get dashboard KPIs

## 🧪 ML Model Details

### Algorithm

- **Linear Regression** (scikit-learn implementation)
- Trains on historical sales data with engineered features

### Features

1. **Time Index**: Normalized month progression
2. **Seasonality**: Month number (1-12) for seasonal patterns
3. **Rolling Average**: 3-month moving average
4. **Lag Features**: Previous 1-2 months' sales
5. **Trend**: Long-term growth pattern

### Fallback Strategy

- If < 6 data points: Uses simple average-based forecast
- If ≥ 6 data points: Trains full ML model

### Accuracy Metrics

- **R² Score**: Coefficient of determination (0-1)
- **MAE**: Mean Absolute Error in units
- Target: R² > 0.7 for good predictions

## 🎨 Design System

### Color Palette

- **Primary**: Indigo-600 (`#4F46E5`)
- **Success**: Green-500 (`#10b981`)
- **Warning**: Yellow-400 (`#facc15`)
- **Danger**: Red-500 (`#ef4444`)
- **Background**: Gray-950 (custom dark)
- **Cards**: Glass morphism with `bg-white/5`

### Typography

- System font stack for optimal performance
- Font weights: 400 (normal), 500 (medium), 600 (semibold), 700 (bold)

## 📊 Database Schema

### Users

- `id`, `username`, `password_hash`, `role`, `created_at`

### Products

- `id`, `name`, `category`, `unit`, `reorder_point`, `lead_time_days`, `created_at`

### Inventory

- `id`, `product_id` (FK), `quantity_in_stock`, `last_updated`, `warehouse_location`

### Sales

- `id`, `product_id` (FK), `quantity_sold`, `sale_date`, `month`, `year`

### Predictions

- `id`, `product_id` (FK), `predicted_quantity`, `prediction_month`, `prediction_year`, `confidence_score`, `created_at`

## 🌱 Seed Data

The seed script generates:

- **8 Industrial Products**: Steel Rods, Copper Wire, PVC Pipes, Aluminum Sheets, Rubber Gaskets, Industrial Bolts, Paint Drums, Circuit Boards
- **18 Months of Sales**: Realistic data with upward trends, seasonal peaks (March, October), and ±15% noise
- **2 Users**: Admin and viewer accounts

## 🔧 Configuration

### Environment Variables

**Backend (.env)**

```env
ANTHROPIC_API_KEY=your_key_here
JWT_SECRET_KEY=supersecretkey123
DATABASE_URL=sqlite:///inventory.db
FLASK_ENV=development
FLASK_PORT=5000
```

**Frontend (.env)**

```env
VITE_API_BASE_URL=http://localhost:5000
```

## 🚢 Production Deployment

### Backend

1. Set `FLASK_ENV=production`
2. Use PostgreSQL instead of SQLite
3. Set strong `JWT_SECRET_KEY`
4. Enable HTTPS
5. Use Gunicorn or uWSGI

### Frontend

1. Build for production:
   ```bash
   npm run build
   ```
2. Serve `dist/` folder with Nginx or CDN
3. Update `VITE_API_BASE_URL` to production API

## 🤝 Contributing

This is a hackathon project. Feel free to fork and extend!

## 📄 License

MIT License - feel free to use this project for learning or commercial purposes.

## 👨‍💻 Author

Built with ❤️ for hackathon judges to showcase full-stack + AI skills.

## 🎯 Hackathon Highlights

✅ **Complete Full-Stack**: React + Flask + SQLite  
✅ **Real AI/ML**: Working Linear Regression predictions  
✅ **AI Integration**: Claude Sonnet 4 chatbot  
✅ **Professional UI**: Dark theme with glassmorphism  
✅ **Production-Ready**: JWT auth, CORS, error handling  
✅ **Rich Features**: Dashboard, charts, reports, exports  
✅ **Clean Code**: Modular structure, no TODOs  
✅ **Realistic Data**: 18 months of seeded sales

---

**⚡ Ready to run? Just install dependencies, seed the database, and launch!**
