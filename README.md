# Become a Cybersecurity Analyst with Python — Lab Environment

Welcome! This repository is your hands-on lab for the course. It runs in
**GitHub Codespaces**, so you don't need to install anything on your own
computer — everything is pre-configured.

## Getting started (one click)

1. Click the green **`< > Code`** button at the top of this repo.
2. Open the **Codespaces** tab.
3. Click **Create codespace on main**.
4. Wait about a minute while it builds. Python, pandas, and all the lab
   data install automatically. When the terminal says the lab is ready,
   you're set.

Run your first detector:

```bash
python scripts/01_brute_force_detector.py
```

You should see it flag an attacker IP and a possible breach.

## What's inside

| Folder | What it holds |
|---|---|
| `data/` | Sample log files (`auth.log`, `access.log`) — synthetic, safe to use |
| `scripts/` | Starter Python scripts for each lab |
| `notebooks/` | Interactive Jupyter versions of the labs |

## Important — staying free (please read)

GitHub gives every personal account **120 free core-hours per month** —
about **60 hours of actual working time** on the standard machine. That is
far more than this course needs. To stay comfortably within the free tier:

- **Stop your codespace when you take a break.** It also auto-stops after
  30 minutes of inactivity.
- **Delete your codespace when you finish the course.** A codespace uses a
  small amount of storage quota for as long as it *exists*, even when
  stopped. Deleting it stops that completely.
  - To delete: go to <https://github.com/codespaces>, click the **`...`**
    next to your codespace, and choose **Delete**.
- **Don't add a payment method** unless you specifically want to. Without
  one, GitHub simply pauses Codespaces if you ever hit the limit — it can
  **never charge you by surprise**.
- Stay on the **2-core machine** (the default for this repo). Bigger
  machines use your free hours faster.

You'll get an email if you ever reach 90% of your monthly quota.

## Working locally instead (optional)

Prefer your own machine? Clone the repo and install the requirements:

```bash
git clone <this-repo-url>
cd <repo>
pip install -r requirements.txt
python scripts/01_brute_force_detector.py
```

For the networking section you'll install **Wireshark** on your own
computer to open the provided capture files — that part isn't done in
Codespaces.
