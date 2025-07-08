#!/bin/bash

# 🧹 SauberHeldPro - Client Demo Startup Script
# This script starts all components needed for the client demonstration

echo "🧹 Starting SauberHeldPro Demo Platform..."
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if port is available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${RED}❌ Port $1 is already in use${NC}"
        return 1
    else
        return 0
    fi
}

# Function to wait for service to start
wait_for_service() {
    local port=$1
    local service_name=$2
    local max_attempts=60  # Increased max attempts
    local attempt=1
    
    echo -e "${YELLOW}⏳ Waiting for ${service_name} to start on port ${port}...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:$port > /dev/null 2>&1; then
            echo -e "${GREEN}✅ ${service_name} is ready!${NC}"
            return 0
        fi
        sleep 2
        ((attempt++))
    done
    
    echo -e "${RED}❌ ${service_name} failed to start within expected time${NC}"
    return 1
}

# Check prerequisites
echo -e "${BLUE}🔍 Checking prerequisites...${NC}"

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
else
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is required but not installed${NC}"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is required but not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites found${NC}"

# Check ports availability
echo -e "${BLUE}🔍 Checking port availability...${NC}"
check_port 3000 || exit 1
check_port 5000 || exit 1
check_port 8501 || exit 1
echo -e "${GREEN}✅ All required ports are available${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo -e "${BLUE}🐍 Creating Python virtual environment...${NC}"
    $PYTHON_CMD -m venv .venv || {
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        exit 1
    }
fi

# Activate virtual environment
echo -e "${BLUE}🐍 Activating Python virtual environment...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    source .venv/bin/activate
else
    source .venv/Scripts/activate
fi

# Install Python requirements
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install Python dependencies${NC}"
    exit 1
fi

# Setup database if needed
if [ ! -f "cleaning_service.db" ]; then
    echo -e "${BLUE}🗄️  Setting up demo database...${NC}"
    python migrate_db.py > /dev/null 2>&1
    python populate_demo_data.py > /dev/null 2>&1
    echo -e "${GREEN}✅ Demo database created${NC}"
fi

# Start Backend API (Port 5000)
echo -e "${BLUE}🚀 Starting Backend API (Port 5000)...${NC}"
cd cleaning-service-app/backend || {
    echo -e "${RED}❌ Backend directory not found${NC}"
    exit 1
}
echo -e "${BLUE}📦 Installing backend dependencies...${NC}"

# Clean npm cache and reinstall dependencies for backend
npm cache clean --force > /dev/null 2>&1
rm -rf node_modules package-lock.json > /dev/null 2>&1
npm install --legacy-peer-deps

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backend dependencies installed${NC}"
    npm start > ../backend.log 2>&1 &
else
    echo -e "${RED}❌ Failed to install backend dependencies${NC}"
    exit 1
fi
BACKEND_PID=$!
cd ../..

# Start Admin Portal (Port 8501)
echo -e "${BLUE}🚀 Starting Admin Portal (Port 8501)...${NC}"
python -m streamlit run admin_portal_multilingual.py --logger.level=debug > admin_portal.log 2>&1 &
ADMIN_PID=$!

# Start Frontend (Port 3000)
echo -e "${BLUE}🚀 Starting Frontend Website (Port 3000)...${NC}"
cd cleaning-service-app/frontend
echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"

# Clean npm cache and reinstall dependencies for frontend
npm cache clean --force > /dev/null 2>&1
rm -rf node_modules package-lock.json > /dev/null 2>&1
npm install

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
    npm start > ../frontend.log 2>&1 &
else
    echo -e "${RED}❌ Failed to install frontend dependencies${NC}"
    exit 1
fi
FRONTEND_PID=$!
cd ../..

# Wait for all services to start
wait_for_service 5000 "Backend API"
wait_for_service 8501 "Admin Portal"
wait_for_service 3000 "Frontend Website"

# Display demo information
echo ""
echo -e "${GREEN}🎉 SauberHeldPro Demo Platform is ready!${NC}"
echo "=============================================="
echo ""
echo -e "${BLUE}📱 Customer Website:${NC} http://localhost:3000"
echo -e "${BLUE}🔧 Admin Portal:${NC}     http://localhost:8501"
echo -e "${BLUE}⚡ Backend API:${NC}      http://localhost:5000"
echo ""
echo -e "${YELLOW}Demo Features:${NC}"
echo "• 🌍 Full English/German multilingual support"
echo "• 📱 Responsive customer website"
echo "• 🛠️  Complete admin management system"
echo "• 🔄 Real-time data synchronization"
echo "• 📊 Business analytics and reporting"
echo ""
echo -e "${YELLOW}Demo Credentials:${NC}"
echo "• Admin Portal: admin / admin123"
echo "• Customer Registration: Available on website"
echo ""
echo -e "${YELLOW}Language Testing:${NC}"
echo "• Use language selector in top-right corner"
echo "• Switch between 🇬🇧 English and 🇩🇪 Deutsch"
echo "• All content translates in real-time"
echo ""
echo -e "${GREEN}Press Ctrl+C to stop all services${NC}"
echo ""

# Create PID file for cleanup
echo "$BACKEND_PID $ADMIN_PID $FRONTEND_PID" > .demo_pids

# Wait for interrupt signal
trap 'echo -e "\n${YELLOW}🛑 Stopping all demo services...${NC}"; kill $(cat .demo_pids) 2>/dev/null; rm -f .demo_pids; echo -e "${GREEN}✅ Demo stopped successfully${NC}"; exit 0' INT

# Keep script running
while true; do
    sleep 1
done
