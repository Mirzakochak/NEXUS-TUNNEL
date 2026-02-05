#!/bin/bash

# Define Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Clear Screen
clear

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}   NEXUS TUNNEL INSTALLER INITIALIZED   ${NC}"
echo -e "${CYAN}========================================${NC}"

# 1. Check Root
if [ "$EUID" -ne 0 ]; then
  echo -e "${GREEN}[!] Please run as root (sudo su)${NC}"
  exit
fi

# 2. Update & Install Dependencies (Python + Wget)
echo -e "${GREEN}[+] Updating repositories and installing dependencies...${NC}"
apt-get update -qq > /dev/null 2>&1
apt-get install -y python3 python3-pip wget -qq > /dev/null 2>&1

echo -e "${GREEN}[+] Dependencies installed successfully.${NC}"

# 3. Download the Python Script (Replace USERNAME with your github username)
# IMPORTANT: Change 'YOUR_GITHUB_USER' below to your actual username!
GITHUB_URL="GITHUB_URL="https://raw.githubusercontent.com/Mirzakochak/NEXUS-TUNNEL/main/nexus.py""
FILE_NAME="nexus.py"

echo -e "${GREEN}[+] Fetching NEXUS Core...${NC}"
wget -q -O $FILE_NAME $GITHUB_URL

if [ -f "$FILE_NAME" ]; then
    # 4. Run the Python Script
    echo -e "${GREEN}[+] Starting NEXUS Interface...${NC}"
    sleep 1
    python3 $FILE_NAME
else
    echo -e "${RED}[!] Error: Failed to download installation file.${NC}"
    exit 1
fi
