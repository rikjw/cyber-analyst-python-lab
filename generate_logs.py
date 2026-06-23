"""
generate_logs.py - build the lab's sample log files with RECENT dates
=====================================================================
Creates data/auth.log and data/access.log with timestamps anchored to
*now*, so the data always looks current no matter when the course is taken.

The contents are otherwise fixed (same attacker IP, same brute-force burst,
same breach) so the course videos and starter scripts always line up.

Run it yourself any time:   python generate_logs.py
In Codespaces it runs automatically when the environment is created.
"""

import os
import random
import datetime

SEED = 42                 # fixed seed -> same events every run (only dates shift)
HOST = "webserver01"
ATTACKER = "198.51.100.77"
NORMAL_IPS = ["192.168.1.10", "192.168.1.22", "10.0.0.5", "203.0.113.40"]
USERS = ["ubuntu", "admin", "www-data", "backup", "deploy"]
AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0)",
    "Mozilla/5.0 (Macintosh)",
    "curl/8.0",
    "python-requests/2.31",
]


def ts(dt):
    """Linux auth.log style timestamp (no year, just like the real thing)."""
    return dt.strftime("%b %d %H:%M:%S")


def build_auth_log(base):
    """base = the datetime the log should 'start' at (we use ~yesterday)."""
    rng = random.Random(SEED)
    lines = []
    t = base

    # --- normal background SSH traffic ---
    for _ in range(120):
        t += datetime.timedelta(seconds=rng.randint(20, 400))
        ip = rng.choice(NORMAL_IPS)
        u = rng.choice(USERS[:2])
        pid = rng.randint(1000, 9999)
        port = rng.randint(40000, 60000)
        result = "Accepted" if rng.random() < 0.92 else "Failed"
        lines.append(f"{ts(t)} {HOST} sshd[{pid}]: {result} password for {u} "
                     f"from {ip} port {port} ssh2")

    # --- brute-force burst from the attacker ~3 hours in ---
    burst = base + datetime.timedelta(hours=3)
    for _ in range(60):
        burst += datetime.timedelta(seconds=rng.randint(1, 4))
        u = rng.choice(["root", "admin", "oracle", "test"])
        pid = rng.randint(1000, 9999)
        port = rng.randint(40000, 60000)
        lines.append(f"{ts(burst)} {HOST} sshd[{pid}]: Failed password for "
                     f"invalid user {u} from {ATTACKER} port {port} ssh2")

    # --- the breach: attacker finally succeeds ---
    burst += datetime.timedelta(seconds=5)
    pid = rng.randint(1000, 9999)
    port = rng.randint(40000, 60000)
    lines.append(f"{ts(burst)} {HOST} sshd[{pid}]: Accepted password for admin "
                 f"from {ATTACKER} port {port} ssh2")

    # --- normal traffic resumes ---
    for i in range(40):
        t = burst + datetime.timedelta(seconds=rng.randint(20, 400) * (i + 1))
        ip = rng.choice(NORMAL_IPS)
        u = rng.choice(USERS[:2])
        pid = rng.randint(1000, 9999)
        port = rng.randint(40000, 60000)
        lines.append(f"{ts(t)} {HOST} sshd[{pid}]: Accepted password for {u} "
                     f"from {ip} port {port} ssh2")

    lines.sort(key=lambda L: datetime.datetime.strptime(
        L.split(" " + HOST)[0], "%b %d %H:%M:%S"))
    return "\n".join(lines) + "\n"


def build_access_log(base):
    rng = random.Random(SEED + 1)
    paths = ["/", "/index.html", "/about", "/products", "/login",
             "/api/users", "/static/app.css", "/images/logo.png"]
    lines = []
    wt = base + datetime.timedelta(hours=1)

    # --- normal web traffic ---
    for _ in range(200):
        wt += datetime.timedelta(seconds=rng.randint(1, 30))
        ip = rng.choice(NORMAL_IPS + [ATTACKER])
        p = rng.choice(paths)
        code = rng.choices([200, 200, 200, 304, 404, 500],
                           [60, 20, 5, 5, 7, 3])[0]
        sz = rng.randint(200, 5000)
        ag = rng.choice(AGENTS)
        stamp = wt.strftime("%d/%b/%Y:%H:%M:%S +0000")
        lines.append(f'{ip} - - [{stamp}] "GET {p} HTTP/1.1" {code} {sz} "-" "{ag}"')

    # --- directory scan + SQL injection attempts from the attacker ---
    scan = base + datetime.timedelta(hours=3, minutes=30)
    scan_paths = ["/admin", "/wp-login.php", "/.env", "/phpmyadmin",
                  "/config.php", "/backup.zip",
                  "/api/users?id=1' OR '1'='1",
                  "/api/users?id=1;DROP TABLE users"]
    for p in scan_paths:
        scan += datetime.timedelta(seconds=rng.randint(1, 3))
        code = 200 if p in ("/admin", "/api/users?id=1' OR '1'='1") else 404
        stamp = scan.strftime("%d/%b/%Y:%H:%M:%S +0000")
        lines.append(f'{ATTACKER} - - [{stamp}] "GET {p} HTTP/1.1" {code} '
                     f'{rng.randint(200, 800)} "-" "python-requests/2.31"')

    return "\n".join(lines) + "\n"


def main():
    # Anchor the data to ~yesterday so timestamps always read as recent.
    base = (datetime.datetime.now() - datetime.timedelta(days=1)).replace(
        hour=8, minute=0, second=0, microsecond=0)

    os.makedirs("data", exist_ok=True)
    with open("data/auth.log", "w") as f:
        f.write(build_auth_log(base))
    with open("data/access.log", "w") as f:
        f.write(build_access_log(base))

    print(f"Generated data/auth.log and data/access.log")
    print(f"Events dated around {base.strftime('%b %d %Y')} (yesterday).")


if __name__ == "__main__":
    main()
