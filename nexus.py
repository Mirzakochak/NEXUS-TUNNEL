import os
import subprocess
import sys
import time

# --- CONFIGURATION ---
APP_NAME = "NEXUS TUNNEL"
BINARY_NAME = "sys-net-helper"
SERVICE_PREFIX = "linux-net-opt"

# --- COLORS ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(Colors.CYAN + Colors.BOLD + r"""
  _   _ ________   __  _    _  _____   _______ _    _ _   _ _   _ ______ _      
 | \ | |  ____\ \ / / | |  | |/ ____| |__   __| |  | | \ | | \ | |  ____| |     
 |  \| | |__   \ V /  | |  | | (___      | |  | |  | |  \| |  \| | |__  | |     
 | . ` |  __|   > <   | |  | |\___ \     | |  | |  | | . ` | . ` |  __| | |     
 | |\  | |____ / . \  | |__| |____) |    | |  | |__| | |\  | |\  | |____| |____ 
 |_| \_|______/_/ \_\  \____/|_____/     |_|   \____/|_| \_|_| \_|______|______|
                                                                                
    """ + Colors.ENDC)
    print(Colors.HEADER + f"   >>> {APP_NAME} PROFESSIONAL SUITE <<<   " + Colors.ENDC)
    print(Colors.BLUE + "   -----------------------------------------   " + Colors.ENDC)

def check_root():
    if os.geteuid() != 0:
        print(Colors.FAIL + "[!] Please run as root." + Colors.ENDC)
        sys.exit(1)

def install_core():
    bin_path = f"/usr/local/bin/{BINARY_NAME}"
    if not os.path.exists(bin_path):
        print(Colors.WARNING + "[*] Initializing System Core..." + Colors.ENDC)
        try:
            subprocess.run("wget -q https://github.com/ginuerzh/gost/releases/download/v2.11.5/gost-linux-amd64-2.11.5.gz", shell=True, check=True)
            subprocess.run("gunzip gost-linux-amd64-2.11.5.gz", shell=True, check=True)
            subprocess.run(f"mv gost-linux-amd64-2.11.5 {bin_path}", shell=True, check=True)
            subprocess.run(f"chmod +x {bin_path}", shell=True, check=True)
            print(Colors.GREEN + "[+] Core Ready." + Colors.ENDC)
        except:
            print(Colors.FAIL + "[!] Core Init Failed." + Colors.ENDC)
            sys.exit(1)

def create_service(suffix, command):
    full_service_name = f"{SERVICE_PREFIX}-{suffix}"
    service_content = f"""[Unit]
Description=System Network Optimizer ({suffix})
After=network.target

[Service]
Type=simple
User=root
ExecStart={command}
Restart=always
RestartSec=3
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""
    with open(f"/etc/systemd/system/{full_service_name}.service", "w") as f:
        f.write(service_content)
    
    subprocess.run("systemctl daemon-reload", shell=True, stdout=subprocess.DEVNULL)
    subprocess.run(f"systemctl enable {full_service_name}", shell=True, stdout=subprocess.DEVNULL)
    subprocess.run(f"systemctl restart {full_service_name}", shell=True, stdout=subprocess.DEVNULL)
    return True

def get_input(prompt, example=None):
    print(Colors.GREEN + f"[?] {prompt}" + Colors.ENDC)
    if example:
        print(Colors.BLUE + f"    (Example: {example})" + Colors.ENDC)
    return input(Colors.WARNING + "    >>> " + Colors.ENDC).strip()

def main():
    check_root()
    print_banner()
    install_core()
    print("\n")
    
    print(Colors.BOLD + "Select Server Location:" + Colors.ENDC)
    print("1. " + Colors.CYAN + "KHAREJ Server" + Colors.ENDC)
    print("2. " + Colors.WARNING + "IRAN Server" + Colors.ENDC)
    
    role = input("\n" + Colors.BOLD + "Enter Choice [1/2]: " + Colors.ENDC)

    bin_cmd = f"/usr/local/bin/{BINARY_NAME}"

    if role == "1":
        # --- KHAREJ SETUP ---
        print_banner()
        print(Colors.CYAN + "--- KHAREJ SERVER SETUP ---" + Colors.ENDC)
        tunnel_port = get_input("Enter Tunnel Port (Any random port)", "9999")
        cmd = f"{bin_cmd} -L relay+wss://:{tunnel_port}"
        create_service("master", cmd)
        print("\n" + Colors.GREEN + "✔ Kharej Server is Ready!" + Colors.ENDC)
        print(f"Connect from Iran using port {Colors.BOLD}{tunnel_port}{Colors.ENDC}")

    elif role == "2":
        # --- IRAN SETUP ---
        print_banner()
        print(Colors.WARNING + "--- IRAN SERVER SETUP ---" + Colors.ENDC)
        
        iran_ip = get_input("Enter IRAN Server IP (This Server)", "185.x.x.x")
        master_ip = get_input("Enter KHAREJ Server IP", "45.x.x.x")
        tunnel_port = get_input("Enter Tunnel Port (Set on Kharej)", "9999")
        
        print(Colors.GREEN + "[?] Enter Config Ports to Forward" + Colors.ENDC)
        print(Colors.BLUE + "    (e.g.: 2082, 443, 8080)" + Colors.ENDC)
        ports_input = input(Colors.WARNING + "    >>> " + Colors.ENDC).strip()
        
        port_list = [p.strip() for p in ports_input.split(',') if p.strip().isdigit()]
        
        if not port_list:
            sys.exit(Colors.FAIL + "No ports defined." + Colors.ENDC)
            
        print("\n" + Colors.CYAN + "[*] Starting Tunnel..." + Colors.ENDC)
        
        success_list = []
        for port in port_list:
            cmd = f"{bin_cmd} -L tcp://:{port}/{master_ip}:{port} -F relay+wss://{master_ip}:{tunnel_port}?insecure=true"
            if create_service(port, cmd):
                success_list.append(port)
                print(f"    -> Port {port}: {Colors.GREEN}CONNECTED{Colors.ENDC}")

        print("\n" + Colors.BOLD + "========================================" + Colors.ENDC)
        print(Colors.GREEN + "       TUNNEL ESTABLISHED SUCCESSFULLY      " + Colors.ENDC)
        print(Colors.BOLD + "========================================" + Colors.ENDC)
        for p in success_list:
            print(f"  • {Colors.WARNING}{iran_ip}:{p}{Colors.ENDC} <==> {Colors.CYAN}{master_ip}:{p}{Colors.ENDC}")
        print("-" * 40)
    else:
        print(Colors.FAIL + "Invalid selection." + Colors.ENDC)

if __name__ == "__main__":
    main()