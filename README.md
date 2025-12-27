# UID-Generator
![Python](https://img.shields.io/badge/Python-3.11%2B-brightgreen?logo=python&logoColor=white)
![License](https://img.shields.io/github/license/ExnoxCH/UID-Generator?logo=github)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20(WSL)%20%7C%20Android-lightgrey?logo=linux&logoColor=white)
## 🛡️ Military Grade UID Generator & Licensing System

A powerful Python-based security tool to generate unique, hardware-bound UIDs for device authentication. It features a built-in time-based access control system to manage and restrict device-specific entry.

### 🚀 Key Features
* **Hardware Binding**: UIDs are uniquely generated based on device fingerprinting (OS, Hostname, Architecture).
* **Dynamic Expiration**: Custom time duration from Seconds, Minutes, Hours, Days, Months, to Years.
* **XOR Encryption**: Protects UID passwords using XOR encryption and Base64 encoding.
* **Responsive Progress Bar**: Beautiful terminal UI that adapts to your screen size (Termux/Linux/PC).

⚙️ Usage:
1. Generate new UID
```bash
python generateUID.py --create
```
2. Check Validity & Remaining Time
```bash
python generateUID.py --check
```
3. Renew License
```bash
python generateUID.py --renew <PASSWORD>
```
4. Show Recovered Password
```bash
python generateUID.py --show-password
```
## Command to run .so file
* **Indonesia**
```bash
python3 -c "import UIDGenerator"
```
* **English**
```bash
python3 -c "import UIDGeneratorEN"
```
## Screenshot
![Screenshot](.assets/ss.png)
