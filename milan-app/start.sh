
#!/bin/bash

# Start the backend server
echo "Starting backend server on port 56396..."
cd backend
python main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID"

# Wait a moment for the backend to initialize
sleep 2

# Start the frontend server
echo "Starting frontend server on port 53254..."
cd ../frontend
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend server started with PID: $FRONTEND_PID"

echo "Both servers are running!"
echo "Backend server log: backend/backend.log"
echo "Frontend server log: frontend/frontend.log"
echo "Press Ctrl+C to stop both servers"

# Function to kill both processes on exit
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Register the cleanup function for when script receives SIGINT (Ctrl+C)
trap cleanup SIGINT

# Keep the script running
while true; do
    sleep 1
done
