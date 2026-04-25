#!/bin/bash
# Deployment script for Mariachi Todo Terreno to Ubuntu staging server
# Usage: ./deployment/deploy.sh [server_user@server_ip]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REMOTE_USER="${1:-ubuntu}"  # Default to 'ubuntu' if not provided
PROJECT_NAME="mariachi-website"
REMOTE_DIR="/var/www/${PROJECT_NAME}"
REPO_URL="https://github.com/g0ochoa/python-mariachi-website.git"
BRANCH="dev"

echo -e "${GREEN}=== Mariachi Todo Terreno Deployment Script ===${NC}"
echo -e "${YELLOW}Deploying to: ${REMOTE_USER}${NC}"
echo ""

# Check if server address provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Please provide server address${NC}"
    echo "Usage: ./deployment/deploy.sh user@server_ip"
    echo "Example: ./deployment/deploy.sh ubuntu@192.168.1.100"
    exit 1
fi

SERVER="$1"

echo -e "${YELLOW}Step 1: Testing SSH connection...${NC}"
if ! ssh -o ConnectTimeout=5 "$SERVER" "echo 'Connection successful'"; then
    echo -e "${RED}Failed to connect to server${NC}"
    exit 1
fi

echo -e "${GREEN}✓ SSH connection successful${NC}"
echo ""

echo -e "${YELLOW}Step 2: Setting up directory structure on server...${NC}"
ssh "$SERVER" << 'ENDSSH'
    # Create directories
    sudo mkdir -p /var/www/mariachi-website
    sudo mkdir -p /var/log/mariachi-website
    
    # Set ownership
    sudo chown -R $USER:$USER /var/www/mariachi-website
    
    echo "✓ Directories created"
ENDSSH

echo -e "${GREEN}✓ Directory structure ready${NC}"
echo ""

echo -e "${YELLOW}Step 3: Cloning/updating repository...${NC}"
ssh "$SERVER" << ENDSSH
    cd /var/www
    
    if [ -d "mariachi-website/.git" ]; then
        echo "Repository exists, pulling latest changes..."
        cd mariachi-website
        git fetch origin
        git checkout ${BRANCH}
        git pull origin ${BRANCH}
    else
        echo "Cloning repository..."
        git clone -b ${BRANCH} ${REPO_URL} mariachi-website
        cd mariachi-website
    fi
    
    echo "✓ Code updated"
ENDSSH

echo -e "${GREEN}✓ Code deployed${NC}"
echo ""

echo -e "${YELLOW}Step 4: Setting up Python virtual environment...${NC}"
ssh "$SERVER" << 'ENDSSH'
    cd /var/www/mariachi-website
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate and install dependencies
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements-prod.txt
    
    echo "✓ Dependencies installed"
ENDSSH

echo -e "${GREEN}✓ Virtual environment ready${NC}"
echo ""

echo -e "${YELLOW}Step 5: Configuring environment variables...${NC}"
echo "Please ensure .env file exists on server with production settings"
ssh "$SERVER" << 'ENDSSH'
    cd /var/www/mariachi-website
    
    if [ ! -f ".env" ]; then
        echo "Warning: .env file not found!"
        echo "Creating template from .env.example..."
        cp .env.example .env
        echo "⚠ Please edit /var/www/mariachi-website/.env with production values"
    else
        echo "✓ .env file exists"
    fi
ENDSSH

echo -e "${GREEN}✓ Environment configured${NC}"
echo ""

echo -e "${YELLOW}Step 6: Running database migrations...${NC}"
ssh "$SERVER" << 'ENDSSH'
    cd /var/www/mariachi-website
    source venv/bin/activate
    
    python manage.py migrate --noinput
    echo "✓ Migrations applied"
ENDSSH

echo -e "${GREEN}✓ Database updated${NC}"
echo ""

echo -e "${YELLOW}Step 7: Collecting static files...${NC}"
ssh "$SERVER" << 'ENDSSH'
    cd /var/www/mariachi-website
    source venv/bin/activate
    
    python manage.py collectstatic --noinput
    echo "✓ Static files collected"
ENDSSH

echo -e "${GREEN}✓ Static files ready${NC}"
echo ""

echo -e "${YELLOW}Step 8: Setting up system services...${NC}"
echo "Please run these commands manually on the server (requires sudo):"
echo ""
echo "  # Install nginx if not installed"
echo "  sudo apt update && sudo apt install -y nginx"
echo ""
echo "  # Copy service file"
echo "  sudo cp /var/www/mariachi-website/deployment/mariachi-website.service /etc/systemd/system/"
echo ""
echo "  # Copy nginx config"
echo "  sudo cp /var/www/mariachi-website/deployment/nginx.conf /etc/nginx/sites-available/mariachi-website"
echo "  sudo ln -sf /etc/nginx/sites-available/mariachi-website /etc/nginx/sites-enabled/"
echo ""
echo "  # Set permissions"
echo "  sudo chown -R www-data:www-data /var/www/mariachi-website"
echo ""
echo "  # Start services"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable mariachi-website"
echo "  sudo systemctl start mariachi-website"
echo "  sudo systemctl restart nginx"
echo ""

echo -e "${GREEN}=== Deployment Complete! ===${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. SSH to server: ssh $SERVER"
echo "2. Edit .env file: sudo nano /var/www/mariachi-website/.env"
echo "3. Run the manual setup commands above"
echo "4. Check service status: sudo systemctl status mariachi-website"
echo "5. View logs: sudo journalctl -u mariachi-website -f"
echo "6. Access site at: http://YOUR_SERVER_IP"
echo ""
