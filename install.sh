#!/bin/bash

# Clear screen
clear

echo "========================================"
echo "   NEXUS TUNNEL INSTALLER               "
echo "========================================"

# 1. Check Root
if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run as root (sudo su)"
  exit
fi

# 2. Update & Install Dependencies
echo "[+] Installing Python3 and Wget..."
apt-get update -qq > /dev/null 2>&1
apt-get install -y python3 python3-pip wget -qq > /dev/null 2>&1

# 3. Download the Python Script
# Direct link to your raw file
GITHUB_URL="https://raw.githubusercontent.com/Mirzakochak/NEXUS-TUNNEL/main/nexus.py"
FILE_NAME="nexus.py"

echo "[+] Downloading core files from GitHub..."

# Remove old file if exists
rm -f $FILE_NAME

# Download the file
wget -O $FILE_NAME "$GITHUB_URL"

# 4. Check and Run
if [ -s "$FILE_NAME" ]; then
    echo "[+] Download Successful. Launching NEXUS..."
    sleep 1
    python3 "$FILE_NAME"
else
    echo "[!] ERROR: Download failed or file is empty."
    echo "[!] Please check: $GITHUB_URL"
    exit 1
fi
