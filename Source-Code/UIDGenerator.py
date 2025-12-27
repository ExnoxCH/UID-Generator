import os
import sys
import uuid
import base64
import hashlib
import platform
import struct
import socket
import time
import random
from colorama import Fore, Style, init
from datetime import datetime, timedelta

init(autoreset=True)

# ================= CONFIG =================
FILE_NAME = "UID.md"
XOR_KEY = "key"

EXPIRE_TIME = {
    "years": 0,
    "months": 0,
    "days": 0,
    "hours": 0,
    "minutes": 0,
    "seconds": 0,
}

BOLD = Style.BRIGHT
RESET = Style.RESET_ALL

def INFO(msg):
    print(f"{Fore.CYAN}{BOLD}[INFO]{RESET} {BOLD}{msg}{RESET}")

def WARN(msg):
    print(f"{Fore.YELLOW}{BOLD}[WARN]{RESET} {Fore.YELLOW}{BOLD}{msg}{RESET}")

def ERROR(msg):
    print(f"{Fore.RED}{BOLD}[ERROR]{RESET} {Fore.RED}{BOLD}{msg}{RESET}")

def SUCCESS(msg):
    print(f"{Fore.GREEN}{BOLD}[SUCCESS]{RESET} {Fore.GREEN}{BOLD}{msg}{RESET}")

# ================= HELP MESSAGE =================
def help_msg():
    print("-" * 54)
    print(f"\n{Fore.MAGENTA}{BOLD}╔══════════════════════════════════════════════════════╗")
    print(f"{Fore.MAGENTA}{BOLD}║                    UID GENERATOR                     ║")
    print(f"{Fore.MAGENTA}{BOLD}╚══════════════════════════════════════════════════════╝{RESET}")
    
    print(f"\n{Fore.GREEN}{BOLD}▶ CARA PENGGUNAAN:{RESET}")
    print(f"  {Fore.WHITE}python generateUID.py {Fore.YELLOW}{BOLD}--create{RESET}         {Fore.WHITE}# Buat UID baru")
    print(f"  {Fore.WHITE}python generateUID.py {Fore.YELLOW}{BOLD}--check{RESET}          {Fore.WHITE}# Cek masa aktif")
    print(f"  {Fore.WHITE}python generateUID.py {Fore.YELLOW}{BOLD}--renew{RESET} {Fore.CYAN}<PWD>{RESET}   {Fore.WHITE}# Perpanjang waktu")
    print(f"  {Fore.WHITE}python generateUID.py {Fore.YELLOW}{BOLD}--show-password{RESET}  {Fore.WHITE}# liat sandi")
    print(f"  {Fore.WHITE}python generateUID.py {Fore.YELLOW}{BOLD}--delete{RESET}         {Fore.WHITE}# Hapus UID")

    print(f"\n{Fore.RED}{BOLD}⚠ PERINGATAN:{RESET}")
    print(f"  {Fore.YELLOW}{BOLD}DEVICE UID{RESET} akan tetap {Fore.RED}{BOLD}sama{RESET} pada perangkat yg telah membuat uid sebelumnya!.")
    print("-" * 54 + "\n")

# ================= LOGIC =================
def xor_encrypt(text, key):
    return base64.b64encode("".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text)).encode()).decode()

def xor_decrypt(encoded, key):
    data = base64.b64decode(encoded).decode()
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def device_fingerprint():
    raw = platform.system() + platform.release() + platform.machine() + str(struct.calcsize("P") * 8) + socket.gethostname()
    return hashlib.sha256(raw.encode()).hexdigest()

def progress_bar(task="Processing"):
    try:
        term_width = os.get_terminal_size().columns
    except:
        term_width = 50

    bar_width = max(10, term_width - 35)

    spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    print(f"{Fore.BLUE}{BOLD}● {task}{RESET}")
    start_time = time.time()

    for i in range(bar_width + 1):
        percent = int((i / bar_width) * 100)
        elapsed_time = time.time() - start_time
        eta = (elapsed_time / i) * (bar_width - i) if i > 0 else 0
        bar = f"{Fore.GREEN}█" * i + f"{Fore.BLACK}{BOLD}░" * (bar_width - i)
        spin = spinner[i % len(spinner)]
        output = f"\r  {bar} {Fore.WHITE}{BOLD}{percent:3d}% {Fore.CYAN}{spin} {Fore.MAGENTA}{BOLD}ETA: {eta:.1f}s{RESET}"
        print(output.ljust(term_width), end="", flush=True)
        base_delay = random.uniform(0.01, 0.03)

        if random.random() < 0.10:
            base_delay += random.uniform(0.2, 0.6)

        if random.random() < 0.03:
            base_delay += random.uniform(0.8, 1.5)

        time.sleep(base_delay)

    #print("")

def device_uid():
    return device_fingerprint()[:16]

def arch_info():
    m = platform.machine().lower()
    bits = struct.calcsize("P") * 8

    if "aarch64" in m or "armv8" in m:
        return f"ARMv8 / {bits}-bit"
    elif "arm" in m:
        return f"ARMv7 / {bits}-bit"
    elif "x86_64" in m or "amd64" in m:
        return f"x64 / {bits}-bit"
    elif "i386" in m or "i686" in m or "x86" in m:
        return f"x86 / {bits}-bit"
    else:
        return f"{bits}-bit Architecture"

def get_expire_text():
    parts = []
    for unit, value in EXPIRE_TIME.items():
        if value > 0:
            name_map = {
                "years": "Tahun",
                "months": "Bulan",
                "days": "Hari",
                "hours": "Jam",
                "minutes": "Menit",
                "seconds": "Detik"
            }
            name = name_map.get(unit, unit)
            parts.append(f"{value} {name}")

    return ", ".join(parts) if parts else "0 detik"
    
def military_uid():
    seed = device_fingerprint() + uuid.uuid4().hex
    raw = hashlib.sha256(seed.encode()).hexdigest().upper()[:32]
    return f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:32]}"

def gen_password():
    return uuid.uuid4().hex[:12]

def get_expire_text():
    parts = []
    name_map = {
        "years": "Tahun", "months": "Bulan", "days": "Hari",
        "hours": "Jam", "minutes": "Menit", "seconds": "Detik"
    }
    for unit, value in EXPIRE_TIME.items():
        if value > 0:
            name = name_map.get(unit, unit)
            parts.append(f"{value} {name}")
    return ", ".join(parts) if parts else "0 detik"

def expire_delta_from_file(expire_text):
    try:
        parts = expire_text.split()
        num = int(parts[0])
        unit = parts[1] 

        unit = unit.lower() 

        if "tahun" in unit: return timedelta(days=num * 365)
        if "bulan" in unit: return timedelta(days=num * 30)
        if "hari" in unit: return timedelta(days=num)
        if "jam" in unit: return timedelta(hours=num)
        if "menit" in unit: return timedelta(minutes=num)
        if "detik" in unit: return timedelta(seconds=num)
    except:
        return timedelta(days=365)
    return timedelta(0)

def human_time(seconds):
    units = [("Tahun", 31536000), ("Bulan", 2592000), ("Hari", 86400),
             ("Jam", 3600), ("Menit", 60), ("Detik", 1)]
    out = []
    for name, size in units:
        val, seconds = divmod(seconds, size)
        if val:
            out.append(f"{val} {name}")
    return " ".join(out) or "0 detik"
def extract(text, key):
    for line in text.splitlines():
        if line.startswith(key): return line.split(":", 1)[1].strip()
    return None

# ================= MAIN =================
args = sys.argv[1:]

if args == ["--create"]:
    if os.path.exists(FILE_NAME):
        WARN("UID SUDAH ADA DI PERANGKAT INI!")
        sys.exit(0)

    print(f"\n{Fore.CYAN}{BOLD} PILIH SATUAN WAKTU (Default jumlah: 1):{RESET}")
    print(f" {Fore.WHITE}1. Detik   2. Menit   3. Jam")
    print(f" {Fore.WHITE}4. Hari    5. Bulan   6. Tahun")

    try:
        Input = input(f"\n{Fore.WHITE} Masukkan nomor (1-6): {Fore.YELLOW}")

        for k in EXPIRE_TIME: EXPIRE_TIME[k] = 0

        unit_map = {
            "1": "seconds", "2": "minutes", "3": "hours",
            "4": "days", "5": "months", "6": "years"
        }

        display_map = {
            "1": "Detik", "2": "Menit", "3": "Jam",
            "4": "Hari", "5": "Bulan", "6": "Tahun"
        }

        if Input in unit_map:
            unit_key = unit_map[Input]
            unit_display = display_map[Input]
            user_input = input(f"{Fore.WHITE} Masukkan jumlah {Fore.CYAN}{unit_display}{Fore.WHITE} (Default 1): {Fore.YELLOW}")
            jumlah = int(user_input) if user_input.strip() != "" else 1

            EXPIRE_TIME[unit_key] = jumlah
            print(f"{RESET}")
        else:
            print("")
            ERROR("PILIHAN TIDAK VALID!")
            sys.exit(1)

    except ValueError:
        print("")
        ERROR("INPUT HARUS BERUPA ANGKA!")
        sys.exit(1)

    # -----------------------------------
    progress_bar("MEMBUAT UID...")

    uid = military_uid()
    password = gen_password()
    created = datetime.now()
    expire_text_val = get_expire_text()

    with open(FILE_NAME, "w") as f:
        f.write(f"# INFORMASI UID ANDA\n\n"
                f"UID        : {uid}\n"
                f"PASSWORD   : {xor_encrypt(password, XOR_KEY)} (Password terenkripsi!)\n"
                f"DEVICE UID : {device_uid()}\n"
                f"ARCH       : {arch_info()}\n"
                f"CREATED AT : {created.isoformat()}\n"
                f"EXPIRED IN : {expire_text_val}\n\n"
                f"# Informasi!\n"
                f"DEVICE UID gabungan dari System(OS), Hostname, dan Hardware.")

    print("\n"), SUCCESS("UID BERHASIL DIBUAT")
    print(f"{Fore.WHITE}{'─'*40}")
    INFO(f"UID       : {Fore.WHITE}{uid}")
    INFO(f"PASSWORD  : {Fore.WHITE}{password}")
    INFO(f"DEVICE ID : {Fore.WHITE}{device_uid()}")
    INFO(f"EXPIRE IN : {Fore.WHITE}{expire_text_val}")
    print(f"{Fore.WHITE}{'─'*40}")
    sys.exit(0)

if args == ["--show-password"]:
    if not os.path.exists(FILE_NAME):
        ERROR("FILE UID TIDAK DITEMUKAN!")
        sys.exit(0)
        
    with open(FILE_NAME, "r") as f:
        data = f.read()
    
    raw_pwd = extract(data, "PASSWORD")
    
    if raw_pwd:
        try:
            clean_hash = raw_pwd.split()[0]
            pwd = xor_decrypt(clean_hash, XOR_KEY)
            INFO(f"PASSWORDMU : {Fore.YELLOW}{BOLD}{pwd}")
        except Exception:
            ERROR("GAGAL MENDEKRIPSI PASSWORD. FILE MUNGKIN RUSAK!")
    else:
        ERROR("DATA PASSWORD TIDAK DITEMUKAN DALAM FILE!")
        
    sys.exit(0)


if args == ["--check"]:
    if not os.path.exists(FILE_NAME):
        ERROR("PERANGKAT BELUM TERDAFTAR!")
        sys.exit(0)

    data = open(FILE_NAME).read()
    if extract(data, "DEVICE UID") != device_uid():
        ERROR("AKSES DITOLAK: PERANGKAT TIDAK COCOK!")
        sys.exit(0)

    created_at_raw = extract(data, "CREATED AT")
    expired_in_raw = extract(data, "EXPIRED IN")

    created = datetime.fromisoformat(created_at_raw)
    duration = expire_delta_from_file(expired_in_raw)

    expire_date = created + duration
    remain = int((expire_date - datetime.now()).total_seconds())

    if remain <= 0:
        ERROR("UIDMU SUDAH EXPIRED")
        INFO(f"TANGGAL EXPIRED: {Fore.RED}{expire_date.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        SUCCESS("LISENSI AKTIF / VALID")
        INFO(f"SISA WAKTU : {Fore.GREEN}{BOLD}{human_time(remain)}")
    sys.exit(0)

if len(args) == 2 and args[0] == "--renew":
    if not os.path.exists(FILE_NAME):
        ERROR("FILE TIDAK ADA ATAU BLM DIBUAT!")
        sys.exit(0)
        
    data = open(FILE_NAME).read()
    raw_pwd = extract(data, "PASSWORD")

    if not raw_pwd:
        ERROR("DATA PASSWORD TIDAK DITEMUKAN!")
        sys.exit(0)

    try:
        clean_hash = raw_pwd.split()[0]
        decrypted_pwd = xor_decrypt(clean_hash, XOR_KEY)
        
        if args[1] != decrypted_pwd:
            ERROR("PASSWORD SALAH!")
            sys.exit(0)
    except Exception:
        ERROR("FILE UID RUSAK ATAU TIDAK VALID!")
        sys.exit(0)

    lines = [f"CREATED AT : {datetime.now().isoformat()}" if l.startswith("CREATED AT") else l for l in data.splitlines()]
    with open(FILE_NAME, "w") as f: 
        f.write("\n".join(lines))
    
    print("")
    progress_bar("MEMPERPANJANG MASA AKTIF")
    print("\n"), SUCCESS("UID BERHASIL DIPERPANJANG!")
    sys.exit(0)

if args == ["--delete"]:
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
        SUCCESS("UID BERHASIL DIHAPUS DARI PERANGKAT ANDA")
    else:
        WARN("FILE TIDAK ADA ATAU BLM DIBUAT!")
    sys.exit(0)
    
if not args or "--help" in args or "-h" in args:
    help_msg()
    sys.exit(0)
