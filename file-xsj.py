# Import necessary modules
import os
import sys
import shutil
import subprocess
import requests
import hashlib
import random
import string

# Define constants
LAB_DIR = "/var/cyberlab"
LAB_CONFIG = "/etc/cyberlab.conf"
LAB_LOG = "/var/log/cyberlab.log"

# Check if script is run as root
if os.geteuid() != 0:
    print("This script must be run as root.")
    sys.exit(1)

# Create lab directory if it doesn't exist
if not os.path.exists(LAB_DIR):
    os.makedirs(LAB_DIR)
    print(f"Created lab directory: {LAB_DIR}")

# Write default configuration if it doesn't exist
if not os.path.exists(LAB_CONFIG):
    with open(LAB_CONFIG, "w") as f:
        f.write("[DEFAULT]\n")
        f.write("lab_name = WhiteRabbitNeo Cybersecurity Lab\n")
        f.write("lab_description = A lab for practicing cybersecurity techniques\n")
        f.write("lab_version = 1.0\n")
    print(f"Created default configuration file: {LAB_CONFIG}")

# Create log file if it doesn't exist
if not os.path.exists(LAB_LOG):
    open(LAB_LOG, "w").close()
    print(f"Created log file: {LAB_LOG}")

# Define functions
def log_event(event):
    with open(LAB_LOG, "a") as f:
        f.write(event + "\n")

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def install_tool(tool):
    subprocess.run(["apt-get", "install", "-y", tool])
    log_event(f"Installed tool: {tool}")

def download_file(url, filename):
    response = requests.get(url)
    with open(os.path.join(LAB_DIR, filename), "wb") as f:
        f.write(response.content)
    log_event(f"Downloaded file: {filename}")

def hash_file(filename):
    with open(os.path.join(LAB_DIR, filename), "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    log_event(f"Hashed file: {filename} - {file_hash}")
    return file_hash

def run_command(command):
    output = subprocess.run(command, capture_output=True, text=True, shell=True)
    log_event(f"Ran command: {command}")
    return output.stdout

# Install required tools
install_tool("nmap")
install_tool("sqlmap")
install_tool("john")

# Download sample files
download_file("https://example.com/malware.exe", "malware.exe")
download_file("https://example.com/password_list.txt", "password_list.txt")

# Generate passwords
passwords = [generate_password() for _ in range(5)]
for password in passwords:
    log_event(f"Generated password: {password}")

# Hash files
malware_hash = hash_file("malware.exe")
password_list_hash = hash_file("password_list.txt")

# Run commands
run_command("nmap -sV 192.168.1.1")
run_command("sqlmap -u http://example.com/vuln --dbs")
run_command("john --wordlist=password_list.txt --format=Raw-MD5 hash.txt")

print("Cybersecurity lab setup complete.")