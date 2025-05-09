# [![Buy Me a Coffee](https://i.imgur.com/rlatSuk.png)](https://www.buymeacoffee.com/galmitrani1)

# GitHub Issue Manager

## Introduction

The **GitHub Issue Manager** is a Python-based command-line tool designed to simplify the management of GitHub issues directly from your terminal. It allows users to interact with their GitHub repositories by creating, listing, and closing issues without needing to navigate the GitHub web interface.

## Features

- **Repository Detection**: Automatically detects the repository from the local Git configuration.
- **GitHub Authentication**: Supports GitHub token-based authentication, with an option to create and save a token for future use.
- **Issue Management**:
  - Create new issues with a title.
  - List issues by state (`open`, `closed`, or `all`).
  - Close issues by their number.
- **Interactive CLI**: Provides an intuitive command-line interface with helpful commands and descriptions.

## Commands

- `/h` - Display the help menu.
- `/o [title]` - Open a new issue with the specified title.
- `/c [title/number]` - Close an existing issue by its number (closing by title is not yet supported).
- `/s [state]` - Show a list of issues filtered by state (`/o` for open, `/c` for closed, `/a` for all).
- `/e` - Exit the CLI.

## How It Works

1. **Setup**: The tool prompts the user to provide the path to a local Git repository.
2. **Authentication**: If a GitHub token is not already saved, the tool guides the user to create one and saves it securely for future use.
3. **Repository Detection**: Extracts the repository name from the Git remote URL.
4. **Command Execution**: Users can execute commands to manage issues interactively.

## Requirements

- **Python 3.x**
- **Dependencies**:
  - `requests` library for making GitHub API calls
- A valid GitHub personal access token with `repo` scope

Install dependencies using:

```bash
pip install requests
```

## Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Tapuz97/github-issue-manager.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd github-issue-manager
   ```
3. **Run the Script**:
   ```bash
   python iIssue_management.py
   ```

Follow the prompts to authenticate and manage issues in your GitHub repository.

## Local Development

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Tapuz97/github-issue-manager.git
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Modify the Code** as needed.
4. **Run the Script**:
   ```bash
   python iIssue_management.py
   ```

## Contribution

Contributions are welcome! To contribute:

1. **Fork the Repository**.
2. **Create a Branch**:
   ```bash
   git checkout -b feature/new-feature
   ```
3. **Commit Your Changes**:
   ```bash
   git commit -m 'Added a new feature'
   ```
4. **Push to the Branch**:
   ```bash
   git push origin feature/new-feature
   ```
5. **Open a Pull Request**.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Thanks to all contributors for improving this tool.
- Special appreciation to the open-source community for supporting automation tools.

---

Thank you for using the GitHub Issue Manager! 🚀