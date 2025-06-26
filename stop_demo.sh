#!/bin/bash

# 🧹 SauberHeldPro - Stop Demo Script

echo "🛑 Stopping SauberHeldPro Demo Platform..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Kill processes if PID file exists
if [ -f ".demo_pids" ]; then
    echo -e "${YELLOW}📋 Found running demo processes...${NC}"
    
    # Read PIDs and kill processes
    while read -r pid; do
        if [ -n "$pid" ]; then
            if kill -0 $pid 2>/dev/null; then
                kill $pid 2>/dev/null
                echo -e "${GREEN}✅ Stopped process $pid${NC}"
            fi
        fi
    done < .demo_pids
    
    # Remove PID file
    rm -f .demo_pids
    echo -e "${GREEN}✅ Cleaned up PID file${NC}"
else
    echo -e "${YELLOW}⚠️  No PID file found, killing by port...${NC}"
fi

# Kill any remaining processes on demo ports
echo -e "${YELLOW}🔍 Checking for processes on demo ports...${NC}"

# Kill processes on port 3000 (Frontend)
FRONTEND_PID=$(lsof -ti:3000)
if [ -n "$FRONTEND_PID" ]; then
    kill -9 $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✅ Stopped frontend (port 3000)${NC}"
fi

# Kill processes on port 5000 (Backend API)
BACKEND_PID=$(lsof -ti:5000)
if [ -n "$BACKEND_PID" ]; then
    kill -9 $BACKEND_PID 2>/dev/null
    echo -e "${GREEN}✅ Stopped backend API (port 5000)${NC}"
fi

# Kill processes on port 8501 (Admin Portal)
ADMIN_PID=$(lsof -ti:8501)
if [ -n "$ADMIN_PID" ]; then
    kill -9 $ADMIN_PID 2>/dev/null
    echo -e "${GREEN}✅ Stopped admin portal (port 8501)${NC}"
fi

# Clean up log files
echo -e "${YELLOW}🧹 Cleaning up log files...${NC}"
rm -f admin_portal.log
rm -f cleaning-service-app/frontend.log
rm -f cleaning-service-app/backend.log

echo ""
echo -e "${GREEN}🎉 SauberHeldPro Demo Platform stopped successfully!${NC}"
echo -e "${YELLOW}💡 To restart the demo, run: ./start_demo.sh${NC}"
echo ""
