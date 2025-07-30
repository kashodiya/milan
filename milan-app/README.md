

# Milan - Matrimonial Service

Milan is a comprehensive matrimonial service web application designed to help individuals find suitable marriage partners based on various compatibility factors.

## Features

- User registration and profile management
- Detailed matrimonial profile creation
- Preference-based match searching and suggestions
- Secure communication between users
- Tiered membership plans
- Success story sharing
- Administrative tools for platform management

## Technology Stack

- **Frontend**: React with Material-UI, built using Vite
- **Backend**: Python FastAPI
- **Database**: SQLite

## Project Structure

```
milan-app/
├── backend/              # FastAPI backend
│   ├── database.py       # Database connection and session management
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic schemas for request/response validation
│   ├── auth.py           # Authentication utilities
│   ├── crud.py           # CRUD operations
│   └── main.py           # Main application file with API routes
│
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── context/      # React context for state management
│   │   ├── pages/        # Page components
│   │   ├── services/     # API service functions
│   │   ├── App.jsx       # Main application component
│   │   └── main.jsx      # Entry point
│   └── public/           # Static assets
│
└── start.sh              # Script to start both frontend and backend servers
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/milan.git
   cd milan
   ```

2. Set up the backend:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```
   cd ../frontend
   npm install
   ```

### Running the Application

You can start both the backend and frontend servers using the provided script:

```
./start.sh
```

Alternatively, you can start them separately:

1. Start the backend server:
   ```
   cd backend
   python main.py
   ```

2. Start the frontend development server:
   ```
   cd frontend
   npm run dev
   ```

The backend API will be available at http://localhost:56396, and the frontend will be available at http://localhost:53254.

## API Documentation

Once the backend server is running, you can access the API documentation at http://localhost:56396/docs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

