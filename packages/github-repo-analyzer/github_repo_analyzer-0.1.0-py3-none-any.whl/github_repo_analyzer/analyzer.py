import os
import git
import logging
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
import tiktoken
from git.exc import GitCommandError

from .utils import AnalysisConfig

class GitHubAnalyzer:
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.token_counter = tiktoken.get_encoding(config.token_encoding)

    def parse_github_url(self, github_url: str) -> tuple:
        """Parse GitHub URL to extract repository URL and subdirectory path."""
        url_parts = github_url.replace('/tree/', '/').replace('/blob/', '/').split('/')
        repo_parts = []
        branch_found = False
        subdirectory_parts = []

        for i, part in enumerate(url_parts):
            if i < 5:  # Always include the first 5 parts (https://github.com/user/repo)
                repo_parts.append(part)
            elif not branch_found and '.' not in part and part not in ['main', 'master']:
                repo_parts.append(part)
            else:
                branch_found = True
                if i < len(url_parts) - 1:
                    subdirectory_parts.append(part)

        repo_url = '/'.join(repo_parts)
        subdirectory = '/'.join(subdirectory_parts[1:] if subdirectory_parts else [])
        return repo_url, subdirectory

    def clone_repository(self, github_url: str, target_dir: str) -> Optional[git.Repo]:
        """Clone a GitHub repository."""
        try:
            print(f"Cloning {github_url}...")
            return git.Repo.clone_from(github_url, target_dir)
        except GitCommandError as e:
            print(f"Failed to clone repository: {e}")
            return None

    def process_file(self, file_path: Path, repo_root: Path) -> Dict:
        """Process a single file and return its analysis results."""
        try:
            if file_path.stat().st_size > self.config.max_file_size:
                print(f"Skipping large file: {file_path}")
                return {"skip": True}

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                return {
                    "content": content,
                    "tokens": len(self.token_counter.encode(content)),
                    "relative_path": str(file_path.relative_to(repo_root)),
                    "extension": file_path.suffix,
                    "skip": False
                }
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return {"skip": True}

    def format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f}TB"

    def analyze_repository(self, repo_path: Path) -> Dict:
        """Analyze repository contents and generate markdown report."""
        results = {"files": [], "total_tokens": 0, "file_types": {}}
        
        for root, dirs, files in os.walk(repo_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.config.exclude_dirs]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in self.config.extensions:
                    result = self.process_file(file_path, repo_path)
                    if not result.get("skip", True):
                        results["files"].append(result)
                        results["total_tokens"] += result["tokens"]
                        ext = result["extension"]
                        results["file_types"][ext] = results["file_types"].get(ext, 0) + 1

        return results

    def generate_markdown(self, results: Dict, repo_url: str) -> str:
        """Generate markdown report from analysis results."""
        markdown = [
            f"# Repository Analysis: {repo_url}\n",
            f"## Summary",
            f"- Total files analyzed: {len(results['files'])}",
            f"- Total tokens: {results['total_tokens']:,}",
            "\n## File Types",
        ]

        for ext, count in sorted(results["file_types"].items()):
            markdown.append(f"- {ext}: {count} files")

        markdown.append("\n## File Details")
        for file in sorted(results["files"], key=lambda x: x["relative_path"]):
            markdown.append(
                f"- {file['relative_path']}\n"
                f"  - Tokens: {file['tokens']:,}"
            )

        return "\n".join(markdown)

def analyze_github_repo(github_url: str, config_path: Optional[str] = None) -> str:
    """Analyze a GitHub repository and generate markdown report."""
    config = AnalysisConfig.from_file(config_path)
    analyzer = GitHubAnalyzer(config)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo = analyzer.clone_repository(github_url, temp_dir)
        if not repo:
            return "Failed to clone repository"
            
        results = analyzer.analyze_repository(Path(temp_dir))
        return analyzer.generate_markdown(results, github_url)

def batch_analyze_repos(repo_list: List[str], config_path: Optional[str] = None) -> Dict[str, str]:
    """Analyze multiple repositories in batch."""
    results = {}
    for repo_url in repo_list:
        try:
            results[repo_url] = analyze_github_repo(repo_url, config_path)
        except Exception as e:
            results[repo_url] = f"Error analyzing repository: {str(e)}"
    return results