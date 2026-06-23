"""
Brute-Force Detector
=====================================
Goal: parse a Linux auth log with Python, find IP addresses with an
unusually high number of failed SSH logins, and flag possible breaches.

This is your STARTER file. Follow the TODOs - the course videos walk
through each step. A worked solution lives in scripts/solutions/.
"""

import re
import pandas as pd

LOG_PATH = "data/auth.log"

# A regex that pulls the fields we care about out of each auth.log line.
# Example line:
# Jan 15 11:00:03 webserver01 sshd[8843]: Failed password for invalid user test from 198.51.100.77 port 54433 ssh2
LINE = re.compile(
    r"(?P<month>\w{3})\s+(?P<day>\d+)\s+(?P<time>[\d:]+)\s+"
    r"\S+\s+sshd\[\d+\]:\s+(?P<result>Accepted|Failed)\s+password\s+"
    r"for\s+(?:invalid user\s+)?(?P<user>\S+)\s+from\s+(?P<ip>\d+\.\d+\.\d+\.\d+)"
)


def parse_log(path):
    """Read the log file and return a tidy DataFrame, one row per event."""
    rows = []
    with open(path) as f:
        for line in f:
            m = LINE.search(line)
            if m:
                rows.append(m.groupdict())
    return pd.DataFrame(rows)


def main():
    df = parse_log(LOG_PATH)
    print(f"Parsed {len(df)} login events\n")

    # TODO 1: How many Failed vs Accepted events are there?
    #   hint: df["result"].value_counts()

    # TODO 2: Count FAILED logins per source IP, highest first.
    #   hint: filter to result == "Failed", then group by "ip"
    failed = df[df["result"] == "Failed"]
    by_ip = failed.groupby("ip").size().sort_values(ascending=False)
    print("Failed logins per IP:")
    print(by_ip.to_string(), "\n")

    # TODO 3: Flag any IP with more than THRESHOLD failed attempts.
    THRESHOLD = 10
    suspects = by_ip[by_ip > THRESHOLD]
    print(f"Suspicious IPs (> {THRESHOLD} failed attempts):")
    print(suspects.to_string() if not suspects.empty else "  none", "\n")

    # TODO 4 (the important one): did any suspicious IP EVER succeed?
    #   That means a brute-force attack that broke in. Cross-reference
    #   the suspect IPs against the Accepted events.
    breached = df[(df["result"] == "Accepted") & (df["ip"].isin(suspects.index))]
    if not breached.empty:
        print("!! POSSIBLE BREACH - suspicious IP with a successful login:")
        print(breached[["month", "day", "time", "user", "ip"]].to_string(index=False))
    else:
        print("No successful logins from suspicious IPs.")


if __name__ == "__main__":
    main()
