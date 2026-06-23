{
  "name": "Cybersecurity Analyst with Python - Lab",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-toolsai.jupyter",
        "ms-python.vscode-pylance"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "terminal.integrated.defaultProfile.linux": "bash"
      }
    }
  },
  "postCreateCommand": "pip install --upgrade pip && pip install -r requirements.txt && python generate_logs.py",
  "postAttachCommand": "echo 'Lab ready. Run: python scripts/01_brute_force_detector.py'",
  "hostRequirements": {
    "cpus": 2
  },
  "remoteUser": "vscode"
}
