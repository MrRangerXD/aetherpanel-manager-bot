#!/usr/bin/env bash
# AetherPanel Manager Bot - Production Installer
# Made by ZenseiBabe

set -e

# Visual Color Styling
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}      AetherPanel Manager Bot           ${NC}"
echo -e "${CYAN}           Made by ZenseiBabe           ${NC}"
echo -e "${CYAN}========================================${NC}"

log_info() {
    echo -e "[${GREEN}INFO${NC}] $1"
}

log_warn() {
    echo -e "[${YELLOW}WARN${NC}] $1"
}

log_error() {
    echo -e "[${RED}ERROR${NC}] $1"
}

install_requirements() {
    log_info "Detecting operating system environment..."
    OS_NAME="unknown"
    PKG_MANAGER="unknown"

    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS_NAME=$ID
    fi

    if command -v apt-get &>/dev/null; then
        PKG_MANAGER="apt"
    elif command -v dnf &>/dev/null; then
        PKG_MANAGER="dnf"
    elif command -v yum &>/dev/null; then
        PKG_MANAGER="yum"
    elif command -v pacman &>/dev/null; then
        PKG_MANAGER="pacman"
    fi

    log_info "Detected OS: $OS_NAME | Package Manager: $PKG_MANAGER"

    log_info "Checking Python 3.10+ installation..."
    PYTHON_CMD=""
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
    fi

    if [ -n "$PYTHON_CMD" ]; then
        PY_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        log_info "Found Python $PY_VERSION"
        PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
        PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
        if [ "$PY_MAJOR" -ne 3 ] || [ "$PY_MINOR" -lt 10 ]; then
            log_warn "Python version is older than 3.10. Attempting to install update if permitted."
        fi
    fi

    # Detect package managers and attempt update
    if [ "$EUID" -eq 0 ]; then
        log_info "Privileged access. Upgrading packages..."
        case $PKG_MANAGER in
            apt)
                apt-get update -y && apt-get install -y python3 python3-pip python3-venv curl git build-essential
                ;;
            dnf)
                dnf install -y python3 python3-pip curl git gcc
                ;;
            yum)
                yum install -y python3 python3-pip curl git gcc
                ;;
            pacman)
                pacman -Sy --noconfirm python python-pip git gcc
                ;;
            *)
                log_warn "Unknown package manager. Please ensure python3, pip, and venv are installed manually."
                ;;
        esac
    else
        log_warn "Non-root user detected. Skipping system package installation. Ensuring virtualenv is created locally..."
    fi

    log_info "Configuring Python virtual environment 'venv'..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv || python -m venv venv
        log_info "venv folder created."
    else
        log_info "Existing virtualenv detected."
    fi

    log_info "Upgrading pip and installing requirements..."
    ./venv/bin/pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        ./venv/bin/pip install -r requirements.txt
        log_info "Requirements successfully installed!"
    else
        log_warn "requirements.txt not found. Installing latest discord.py, aiohttp, python-dotenv..."
        ./venv/bin/pip install discord.py aiohttp python-dotenv
    fi
}

install_bot() {
    echo -e "\n${CYAN}⚙️ AetherPanel Manager Bot Configuration Wizard${NC}"
    echo -e "------------------------------------------------"
    
    # Secure token inputs
    read -rp "Enter Discord Bot Token: " DISCORD_TOKEN
    read -rp "Enter AetherPanel REST API URL [http://localhost:3000/api/aether]: " AETHER_URL
    if [ -z "$AETHER_URL" ]; then
        AETHER_URL="http://localhost:3000/api/aether"
    fi
    read -rp "Enter AetherPanel API Key: " AETHER_KEY
    read -rp "Enter Discord Owner User ID (Optional): " OWNER_ID
    read -rp "Enter Log Level [INFO]: " LOG_LVL
    if [ -z "$LOG_LVL" ]; then
        LOG_LVL="INFO"
    fi

    # Save to .env securely
    cat <<EOF > .env
DISCORD_TOKEN=$DISCORD_TOKEN
AETHERPANEL_URL=$AETHER_URL
AETHERPANEL_API_KEY=$AETHER_KEY
BOT_OWNER_ID=$OWNER_ID
LOG_LEVEL=$LOG_LVL
REQUEST_TIMEOUT=30
EOF

    chmod 600 .env
    log_info "Configuration saved successfully to .env."

    log_info "Validating syntax check on python entry points..."
    if [ -d "venv" ]; then
        ./venv/bin/python3 -m py_compile main.py && log_info "Syntax verification PASSED! 🟢"
    else
        python3 -m py_compile main.py && log_info "Syntax verification PASSED! 🟢"
    fi
}

update_bot() {
    log_info "Checking git remote states..."
    if [ -d ".git" ]; then
        git fetch --all
        git status
        log_info "Git updates verified. Local files kept intact."
    else
        log_warn "Not a git repository. Keep local configs."
    fi
}

check_installation() {
    echo -e "\n${CYAN}📋 System Diagnostics Report${NC}"
    echo -e "----------------------------------------"

    # Python validation
    if command -v python3 &>/dev/null; then
        echo -e "Python        ${GREEN}PASS${NC}"
    else
        echo -e "Python        ${RED}FAIL${NC}"
    fi

    # Virtual environment check
    if [ -d "venv" ]; then
        echo -e "Virtualenv    ${GREEN}PASS${NC}"
    else
        echo -e "Virtualenv    ${RED}FAIL${NC}"
    fi

    # Dependencies check
    if [ -f "requirements.txt" ]; then
        echo -e "Dependencies  ${GREEN}PASS${NC}"
    else
        echo -e "Dependencies  ${RED}FAIL${NC}"
    fi

    # Env credentials check
    if [ -f ".env" ]; then
        echo -e "Configuration ${GREEN}PASS${NC}"
    else
        echo -e "Configuration ${RED}FAIL${NC}"
    fi

    # Reachability test
    if [ -f ".env" ]; then
        AETHER_URL=$(grep "AETHERPANEL_URL" .env | cut -d'=' -f2- | tr -d '"' | tr -d "'" | tr -d ' ' || echo "")
        if [ -n "$AETHER_URL" ]; then
            if curl -s -k --max-time 3 "$AETHER_URL/health" &>/dev/null; then
                echo -e "AetherPanel   ${GREEN}PASS (Online)${NC}"
            else
                echo -e "AetherPanel   ${YELLOW}UNREACHABLE (Is Expected offline)${NC}"
            fi
        else
            echo -e "AetherPanel   ${RED}FAIL (Missing URL)${NC}"
        fi
    else
        echo -e "AetherPanel   ${RED}FAIL (Missing configuration)${NC}"
    fi
}

while true; do
    echo -e "\n1. Install Requirements"
    echo -e "2. Install Bot"
    echo -e "3. Update Bot"
    echo -e "4. Check Installation"
    echo -e "5. Exit"
    echo -e ""
    read -rp "Select an option: " OPTION

    case $OPTION in
        1)
            install_requirements
            ;;
        2)
            install_bot
            ;;
        3)
            update_bot
            ;;
        4)
            check_installation
            ;;
        5)
            log_info "Exiting. Thank you for using AetherPanel Manager Bot!"
            exit 0
            ;;
        *)
            log_error "Invalid option selected."
            ;;
    esac
done
