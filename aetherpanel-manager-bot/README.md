# AetherPanel Manager Bot
### Made by ZenseiBabe

A highly professional, secure, and production-ready Discord management interface specifically integrated with **AetherPanel** REST APIs. Inspired by high-end gaming node controllers (like Pterodactyl), this bot exposes full remote controls, diagnostic health grids, financial ledger credit adjustment screens, and container power switches directly to your Discord server.

---

## 🚀 Primary Features

*   **🖥️ Power Lifecycle Controllers:** Remotely signal `/server start`, `stop`, `restart`, or forced `kill` states directly from interaction buttons.
*   **💾 Snapshot Backup Managers:** Instantly spin, restore, or delete backup records saved on cluster SSD vaults.
*   **📜 Diagnostic Output Tail:** Review running server logs and easily dispatch console commands inside a secure interactive Discord Modal.
*   **👥 User Identity & Balance Ledgers:** Read developer accounts profiles, adjust financial credits, or toggle account suspensions.
*   **🌐 Cluster Telemetry Monitoring:** Browse physical compute nodes and analyze node specs, CPU thresholds, and heartbeats.
*   **🎨 Premium Components V2 UX:** Utilizes high-fidelity buttons, responsive selection lists, form modals, and safety confirmation gates.

---

## ⚙️ Repository Layout

```text
aetherpanel-manager-bot/
├── main.py                # Main orchestrator (handles live gateways and CLI previews)
├── requirements.txt      # Dependency lists
├── .env                  # Private credential secrets
├── .env.example          # Security keys template configuration
├── install.sh            # Universal Linux installer shell system
├── install.txt           # Documentation summary
├── README.md             # This help file
│
├── config/
│   └── config.py         # Credentials parses and validates
│
├── api/                  # Modular REST requests layer
│   ├── client.py         # Main Client session
│   ├── servers.py        # Servers endpoints
│   ├── nodes.py          # Nodes heartbeats
│   ├── users.py          # User balance profiles
│   ├── admin.py          # Metrics dashboards
│   ├── backups.py        # Backup snapshots
│   └── system.py         # Panel health checks
│
├── commands/             # Slash command payload generators
│   ├── server.py
│   ├── node.py
│   ├── admin.py
│   ├── user.py
│   ├── deploy.py
│   └── help.py
│
├── views/                # Discord Components V2 UI buttons & select menus
│   ├── dashboard.py
│   ├── server_views.py
│   ├── node_views.py
│   ├── admin_views.py
│   ├── pagination.py
│   └── help_views.py
│
└── utils/                # System helpers and attribution modules
    ├── embeds.py
    ├── permissions.py
    ├── errors.py
    ├── logger.py
    └── watermark.py      # Watermark branding "Made by ZenseiBabe"
```

---

## 📦 Requirements

*   **Python 3.10+** (Virtual environments recommended)
*   **discord.py** (Modern Components V2 support)
*   **aiohttp** (Asynchronous request sessions)
*   **python-dotenv** (Secure credential parses)

---

## 🛠️ Quick Installation

Deploying persistently to a Linux VPS or development terminal is simple:

1.  **Grant Execute permissions to the installer:**
    ```bash
    chmod +x install.sh
    ```
2.  **Execute the Installer:**
    ```bash
    ./install.sh
    ```
3.  **Choose Menu Option `1`** to create a virtual environment, update pip, and install dependency packages automatically.
4.  **Choose Menu Option `2`** to register bot tokens, URL hosts, and API keys securely into `.env`.
5.  Start, stop, or query the bot daemon status easily from the menu!

---

*Made by ZenseiBabe • AetherPanel Manager*
