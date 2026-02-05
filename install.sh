#!/bin/bash

# Define Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}   NEXUS TUNNEL INSTALLER               ${NC}"
echo -e "${CYAN}========================================${NC}"

# 1. Check Root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[!] Please run as root (sudo su)${NC}"
  exit
fi

# 2. Update & Install Dependencies
echo -e "${GREEN}[+] Installing Python3 and Wget...${NC}"
apt-get update -qq > /dev/null 2>&1
apt-get install -y python3 python3-pip wget -qq > /dev/null 2>&1

# 3. Download the Python Script
GITHUB_URL="https://raw.githubusercontent.com/Mirzakochak/NEXUS-TUNNEL/main/nexus.py"
FILE_NAME="nexus.py"

echo -e "${GREEN}[+] Downloading core files from GitHub...${NC}"

# Delete old file
rm -f $FILE_NAME

# Download new file
wget -O $FILE_NAME "$GITHUB_URL"

# 4. Check and Run
if [ -f "$FILE_NAME" ]; then
    echo -e "${GREEN}[+] Download Successful. Launching NEXUS...${NC}"
    sleep 1
    python3 "$FILE_NAME"
else
    echo -e "${RED}[!] ERROR: Download failed. Check your GitHub URL.${NC}"
    exit 1
fi
