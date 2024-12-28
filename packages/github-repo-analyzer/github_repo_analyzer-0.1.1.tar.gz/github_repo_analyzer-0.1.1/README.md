# GitHub Repository Analyzer

A Python package for analyzing GitHub repositories and generating detailed markdown reports. This tool helps you understand repository structure, calculate token counts, and generate comprehensive documentation.

## Features

- Generate comprehensive source tree visualization
- Calculate total token count using OpenAI's tiktoken library
- Provide file type statistics and repository summaries
- Support parallel processing for faster analysis
- Handle multiple programming languages
- Exclude common non-code directories
- Generate beautiful markdown reports

## Installation

```bash
pip install github-repo-analyzer
```

## Quick Start

### As a Python Package

```python
from github_repo_analyzer import analyze_github_repo

# Analyze a single repository
report = analyze_github_repo("https://github.com/username/repo")
print(report)

# Batch analyze multiple repositories
from github_repo_analyzer import batch_analyze_repos
repos = ["https://github.com/user1/repo1", "https://github.com/user2/repo2"]
results = batch_analyze_repos(repos)
```

### Command Line Interface

```bash
# Analyze a single repository
repo-analyzer --url https://github.com/username/repo

# Analyze multiple repositories from a file
repo-analyzer --batch repos.txt

# Use custom configuration
repo-analyzer --url https://github.com/username/repo --config config.json

# Save output to file
repo-analyzer --url https://github.com/username/repo --output report.md
```

## Configuration

Create a `config.json` file to customize the analysis:

```json
{
    "extensions": [".py", ".js", ".ts"],
    "exclude_dirs": [".git", "node_modules"],
    "max_file_size": 1048576,
    "token_encoding": "cl100k_base",
    "max_workers": 4,
    "output_format": "markdown"
}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI's tiktoken library for token counting
- GitPython for repository handling