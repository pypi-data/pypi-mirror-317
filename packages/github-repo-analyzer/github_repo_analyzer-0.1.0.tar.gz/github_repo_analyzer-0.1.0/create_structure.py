import os

# Create main directories
os.makedirs("src/github_repo_analyzer", exist_ok=True)
os.makedirs("tests", exist_ok=True)

# Create empty files
files = [
    "src/github_repo_analyzer/__init__.py",
    "src/github_repo_analyzer/analyzer.py",
    "src/github_repo_analyzer/utils.py",
    "src/github_repo_analyzer/cli.py",
    "tests/__init__.py",
    "tests/test_analyzer.py",
    "pyproject.toml",
    "README.md",
    "LICENSE",
    ".gitignore"
]

for file in files:
    with open(file, 'a') as f:
        pass  # Just create empty files
