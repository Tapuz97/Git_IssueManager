#!/usr/bin/env python3
# file: github_issue_manager.py

import argparse
import os
import sys
import subprocess
import requests
from pathlib import Path
from urllib.parse import urlparse

GITHUB_API = "https://api.github.com"
TOKEN_PATH = Path.home() / ".github_token"


def get_repo_path() -> Path:
    repo_path = input("Enter the path to your local Git repository: ").strip()
    path = Path(repo_path)
    if not (path.exists() and (path / ".git").is_dir()):
        print("❌ Invalid Git repository path.")
        sys.exit(1)
    os.chdir(path)
    return path


def extract_repo_from_git() -> str:
    try:
        url = subprocess.check_output([
            "git", "config", "--get", "remote.origin.url"
        ], text=True).strip()
        if url.endswith(".git"):
            url = url[:-4]
        parsed = urlparse(url)
        if parsed.scheme:
            parts = parsed.path.strip("/").split("/")
        elif ":" in url:
            parts = url.split(":", 1)[-1].split("/")
        else:
            raise ValueError("Unsupported Git URL format")
        if len(parts) >= 2:
            return f"{parts[-2]}/{parts[-1]}"
    except Exception as e:
        print(f"Failed to extract repo name: {e}")
        sys.exit(1)


def device_flow_login() -> str:
    print("🔐 Starting GitHub login via Device Flow...")
    client_id = "Iv1.06d6ba124b3d601d"  # GitHub public CLI client ID
    resp = requests.post("https://github.com/login/device/code", data={
        "client_id": client_id,
        "scope": "repo"
    }, headers={"Accept": "application/json"})
    data = resp.json()
    print(f"👉 Go to {data['verification_uri']} and enter code: {data['user_code']}")

    interval = data.get("interval", 5)
    token = None
    while not token:
        import time
        time.sleep(interval)
        poll_resp = requests.post("https://github.com/login/oauth/access_token", data={
            "client_id": client_id,
            "device_code": data["device_code"],
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
        }, headers={"Accept": "application/json"})
        poll_data = poll_resp.json()
        if "access_token" in poll_data:
            token = poll_data["access_token"]
            break
        elif poll_data.get("error") not in ("authorization_pending",):
            print("❌ Login failed:", poll_data)
            sys.exit(1)
    TOKEN_PATH.write_text(token)
    print("✅ Login successful!")
    return token


def get_token() -> str:
    if TOKEN_PATH.exists():
        return TOKEN_PATH.read_text().strip()
    return device_flow_login()


def get_headers(token: str) -> dict:
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }


def show_help():
    print("""
Commands:
  -h / --help           Show this help menu
  -o / --open           Open a new issue
  -c / --close          Close an existing issue by number
  -s / --show           Show issue list
  -f [state]            Filter with --show by issue state:
                        /o = open, /c = closed, /a = all
    """)


def command_handler(args, repo: str, token: str):
    if args.help:
        show_help()
    elif args.open:
        print("[OPEN] Handler placeholder: Prompt for title/body and open issue.")
    elif args.close:
        print("[CLOSE] Handler placeholder: Prompt for issue number and close.")
    elif args.show:
        state_map = {"/o": "open", "/c": "closed", "/a": "all"}
        state = state_map.get(args.f, "open") if args.f else "open"
        print(f"[SHOW] Handler placeholder: Listing issues with state = {state}")
    else:
        print("🔧 No valid command provided. Use --help to see available options.")


def main():
    get_repo_path()
    repo = extract_repo_from_git()
    token = get_token()
    print(f"\n✔ Repo detected: {repo}\n✔ Login verified 🎉\n")

    parser = argparse.ArgumentParser(description="GitHub Issue Manager CLI", add_help=False)
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-o", "--open", action="store_true")
    parser.add_argument("-c", "--close", action="store_true")
    parser.add_argument("-s", "--show", action="store_true")
    parser.add_argument("-f", type=str, help="/o=open /c=closed /a=all")
    args = parser.parse_args()

    command_handler(args, repo, token)


if __name__ == "__main__":
    main()
