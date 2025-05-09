#!/usr/bin/env python3
# file: github_issue_manager.py

import argparse
import os
import sys
import subprocess
import requests
import webbrowser
from pathlib import Path
from urllib.parse import urlparse

GITHUB_API = "https://api.github.com"
TOKEN_PATH = Path.home() / ".github_token"

# This function checks if the provided path is a valid Git repository
def get_repo_path() -> Path:
    repo_path = input("Enter the path to your local Git repository: ").strip()
    path = Path(repo_path)
    if not (path.exists() and (path / ".git").is_dir()):
        print("❌ Invalid Git repository path.")
        sys.exit(1)
    os.chdir(path)
    return path

# This function extracts the repository name from the Git remote URL
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

# This function prompts the user to create a GitHub token if not found
def manual_token_login() -> str:
    print("🔐 No saved GitHub token found.")
    print("🌐 Opening GitHub token creation page in your browser...")
    url = "https://github.com/settings/tokens/new?scopes=repo&description=Tapuz97_GitIssueManager"
    webbrowser.open(url)
    token = input("Please paste your newly created GitHub token here: ").strip()
    if not token:
        print("❌ Token input was empty. Aborting.")
        sys.exit(1)
    TOKEN_PATH.write_text(token)
    print("✅ Token saved for future use.")
    return token

# This function retrieves the GitHub token from the saved file or prompts for a new one
def get_token() -> str:
    if TOKEN_PATH.exists():
        return TOKEN_PATH.read_text().strip()
    return manual_token_login()

# This function returns the headers required for GitHub API requests
def get_headers(token: str) -> dict:
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

# This function displays the help menu for the CLI
def show_help():
    print("""
Commands:
  /h                  Show this help menu
  /o [title]          Open a new issue with title
  /c [title/number]   Close an existing issue by number or title
  /s [state]          Show issue list default /a:
                      /o = open, /c = closed, /a = all
  /e                  Exit the CLI loop
    """)

# This function creates a new issue in the specified repository
def create_issue(repo: str, token: str, title: str):
    url = f"{GITHUB_API}/repos/{repo}/issues"
    data = {"title": title}
    response = requests.post(url, headers=get_headers(token), json=data)
    if response.status_code == 201:
        issue = response.json()
        print(f"✅ Issue #{issue['number']} created: {issue['title']}")
    else:
        print(f"❌ Failed to create issue: {response.status_code} {response.text}")

# This function lists issues based on the state provided
def list_issues(repo: str, token: str, state: str):
    url = f"{GITHUB_API}/repos/{repo}/issues?state={state}"
    response = requests.get(url, headers=get_headers(token))
    if response.status_code == 200:
        issues = response.json()
        for issue in issues:
            print(f"#{issue['number']}: {issue['title']} [{issue['state']}]")
    else:
        print(f"❌ Failed to fetch issues: {response.status_code} {response.text}")


# This function handles the command input and maps it to the appropriate function
def command_handler(repo: str, token: str):
    command_map = {
        "/h": lambda args: show_help(),
        "/o": lambda args: create_issue(repo, token, " ".join(args)) if args else print("❌ Please provide a title after /o"),
        "/c": lambda args: close_issue(repo, token, args),
        "/s": lambda args: list_issues(repo, token, {"/o": "open", "/c": "closed", "/a": "all"}.get(args[0], "all") if args else "all"),
        "/e": lambda args: exit("👋 Exiting GitHub Issue Manager.")
    }

    while True:
        raw = input("\n> Enter command: ").strip().split()
        if not raw:
            continue
        cmd, args = raw[0], raw[1:]
        handler = command_map.get(cmd)
        if handler:
            handler(args)
        else:
            print("Unrecognized command\n")
            show_help()

# This function closes an issue by its number or title
def close_issue(repo: str, token: str, args: list):
    if not args:
        print("❌ Please provide an issue title or number after /c")
        return
    ref = args[0]
    if ref.isdigit():
        number = int(ref)
        url = f"{GITHUB_API}/repos/{repo}/issues/{number}"
        response = requests.patch(url, headers=get_headers(token), json={"state": "closed"})
        if response.status_code == 200:
            print(f"✅ Closed issue #{number}")
        else:
            print(f"❌ Failed to close issue: {response.status_code} {response.text}")
    else:
        print("❌ Closing by title is not yet supported.")


def main():
    print("\n==========================")
    print("github issue manager v1.0\nCreated by Gal Mitrani\nhttps://github.com/Tapuz97")
    print("==========================")
    get_repo_path()
    repo = extract_repo_from_git()
    token = get_token()
    print(f"\n✔ Repo detected: {repo}\n✔ Login verified 🎉\n")
    show_help()
    command_handler(repo, token)


if __name__ == "__main__":
    main()
