#!/bin/bash

# --- COLORS ---
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# --- BANNER ---
clear
echo -e "${CYAN}=============================================${NC}"
echo -e "${CYAN}       NEXUS TUNNEL INSTALLER v2.0           ${NC}"
echo -e "${CYAN}=============================================${NC}"
echo ""

# 1. Check Root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[!] Please run as root (sudo su)${NC}"
  exit
fi

# 2. Update & Install Dependencies
echo -e "${YELLOW}[*] Updating system and installing dependencies...${NC}"
apt-get update -qq > /dev/null 2>&1
apt-get install -y python3 python3-pip wget -qq > /dev/null 2>&1
echo -e "${GREEN}[+] Dependencies installed.${NC}"

# 3. Download the Python Script
GITHUB_URL="https://raw.githubusercontent.com/Mirzakochak/NEXUS-TUNNEL/main/nexus.py"
FILE_NAME="nexus.py"

echo -e "${YELLOW}[*] Fetching NEXUS Core from GitHub...${NC}"

# Remove old file
rm -f $FILE_NAME

# Download new file
wget -O $FILE_NAME "$GITHUB_URL"

# 4. Verification & Run
if [ -s "$FILE_NAME" ]; then
    echo -e "${GREEN}[+] Download Successful. Launching...${NC}"
    echo ""
    sleep 1
    python3 "$FILE_NAME"
else
    echo -e "${RED}[!] ERROR: Download failed!${NC}"
    echo -e "${RED}[!] Check your internet or GitHub URL.${NC}"
    exit 1
fi
