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
import json
import datetime

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

    def count_lines(self, content: str) -> int:
        """Count non-empty lines in content."""
        return len([line for line in content.splitlines() if line.strip()])

    def analyze_repository(self, github_url: str) -> bool:
        """Analyze a GitHub repository and generate documentation."""
        if not github_url:
            print("No GitHub URL provided.")
            return False

        # Parse the GitHub URL to handle subdirectories
        repo_url, subdirectory = self.parse_github_url(github_url)
        if subdirectory:
            print(f"Analyzing subdirectory: {subdirectory}")

        # Create temporary directory for cloning
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            repo = self.clone_repository(repo_url, repo_path)

            if not repo:
                return False

            # Determine the path to analyze
            analysis_path = repo_path / subdirectory if subdirectory else repo_path
            if not analysis_path.exists():
                print(f"Subdirectory {subdirectory} not found in repository")
                return False

            # Extract repository/directory name for output
            repo_name = subdirectory.split('/')[-1] if subdirectory else repo_url.rstrip("/").split("/")[-1].replace(".git", "")

            # Initialize analysis results
            analysis_results = {
                "repository": repo_name,
                "timestamp": datetime.datetime.now().isoformat(),
                "files": [],
                "total_tokens": 0
            }

            # Collect files for processing
            files_to_process = []
            for root, dirs, files in os.walk(analysis_path):
                dirs[:] = [d for d in dirs if d not in self.config.exclude_dirs]

                for file in files:
                    file_path = Path(root) / file
                    if any(file.endswith(ext) for ext in self.config.extensions):
                        files_to_process.append(file_path)

            print(f"Processing {len(files_to_process)} files...")

            # Process files in parallel
            with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
                futures = [
                    executor.submit(self.process_file, file_path, analysis_path)
                    for file_path in files_to_process
                ]

                for future in futures:
                    result = future.result()
                    if not result["skip"]:
                        analysis_results["files"].append(result)
                        analysis_results["total_tokens"] += result["tokens"]

            # Generate output
            output_path = self.generate_output(analysis_results)
            print(f"Analysis completed. Output saved to: {output_path}")
            return True

    def generate_output(self, analysis_results: Dict) -> str:
        """Generate analysis output in the specified format."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        output_path = f"{analysis_results['repository']}_analysis_{timestamp}"

        if self.config.output_format == "markdown":
            output_path += ".md"
            self.generate_markdown(analysis_results, output_path)
        elif self.config.output_format == "json":
            output_path += ".json"
            self.generate_json(analysis_results, output_path)
        else:
            print(f"Unsupported output format: {self.config.output_format}")
            return ""

        return output_path

    def generate_markdown(self, analysis_results: Dict, output_path: str):
        """Generate Markdown documentation with enhanced source tree."""
        with open(output_path, 'w', encoding='utf-8') as f:
            # Clean repository name
            repo_name = analysis_results['repository'].split(os.sep)[-1].replace('.git', '')
            
            # Repository header
            f.write(f"# {repo_name} Repository Analysis\n\n")
            
            # Table of Contents
            f.write("## Table of Contents\n\n")
            f.write("1. [Repository Summary](#repository-summary)\n")
            f.write("2. [File Type Statistics](#file-type-statistics)\n")
            f.write("3. [Source Tree](#source-tree)\n")
            f.write("4. [File Contents](#file-contents)\n\n")

            # Summary section
            f.write("## Repository Summary\n\n")
            total_files = len(analysis_results['files'])
            total_lines = sum(self.count_lines(file['content']) for file in analysis_results['files'])
            total_size = sum(len(file['content'].encode('utf-8')) for file in analysis_results['files'])

            f.write(f"- **Analysis Date:** {analysis_results['timestamp']}\n")
            f.write(f"- **Total Files:** {total_files:,}\n")
            f.write(f"- **Total Lines of Code:** {total_lines:,}\n")
            f.write(f"- **Repository Size:** {self.format_size(total_size)}\n")
            f.write(f"- **Total Tokens:** {analysis_results['total_tokens']:,}\n\n")

            # File type statistics
            extension_stats = {}
            for file in analysis_results['files']:
                ext = file['extension'] or 'no extension'
                if ext not in extension_stats:
                    extension_stats[ext] = {'count': 0, 'lines': 0, 'size': 0}
                stats = extension_stats[ext]
                stats['count'] += 1
                stats['lines'] += self.count_lines(file['content'])
                stats['size'] += len(file['content'].encode('utf-8'))

            f.write("## File Type Statistics\n\n")
            f.write("| Extension | File Count | Lines of Code | Size |\n")
            f.write("|-----------|------------|---------------|------|\n")
            for ext, stats in sorted(extension_stats.items(), key=lambda x: x[1]['lines'], reverse=True):
                f.write(f"| `{ext}` | {stats['count']:,} | {stats['lines']:,} | {self.format_size(stats['size'])} |\n")
            f.write("\n")

            # Enhanced source tree
            f.write("## Source Tree\n\n")
            f.write("```\n")

            # Organize files by directory
            file_tree = {}
            max_name_length = 0
            for file_info in analysis_results["files"]:
                path_parts = file_info["relative_path"].split(os.sep)
                max_name_length = max(max_name_length, len(path_parts[-1]))
                current_dict = file_tree
                for part in path_parts[:-1]:
                    if part not in current_dict:
                        current_dict[part] = {'__files__': []}
                    current_dict = current_dict[part]
                current_dict['__files__'] = current_dict.get('__files__', [])
                current_dict['__files__'].append(file_info)

            # Write tree structure with enhanced information and aligned columns
            def write_tree(d: Dict, prefix: str = "", is_last: bool = True):
                entries = sorted([(k, v) for k, v in d.items() if k != '__files__'])
                files = d.get('__files__', [])

                for idx, (name, content) in enumerate(entries):
                    is_last_entry = idx == len(entries) - 1 and not files
                    f.write(f"{prefix}{'└──' if is_last_entry else '├──'} {name}/\n")
                    new_prefix = prefix + ('    ' if is_last_entry else '│   ')
                    write_tree(content, new_prefix, idx == len(entries) - 1)

                for idx, file_info in enumerate(sorted(files, key=lambda x: x['relative_path'])):
                    is_last_file = idx == len(files) - 1
                    name = os.path.basename(file_info['relative_path'])
                    lines = self.count_lines(file_info['content'])
                    size = len(file_info['content'].encode('utf-8'))
                    padding = max_name_length - len(name)
                    f.write(f"{prefix}{'└──' if is_last_file else '├──'} {name}{' ' * padding} "
                           f"[{self.format_size(size):>7}, {lines:>5,} lines]\n")

            write_tree(file_tree)
            f.write("```\n\n")

            # File contents with anchors for navigation
            f.write("## File Contents\n\n")
            for file_info in sorted(analysis_results["files"],
                                  key=lambda x: x["relative_path"]):
                file_path = file_info['relative_path'].replace('\\', '/')
                anchor = file_path.replace('/', '-').replace('.', '-').lower()
                f.write(f"### {file_path} {{{anchor}}}\n\n")
                ext = file_info['extension'][1:] if file_info['extension'] else ''
                f.write(f"```{ext}\n")
                f.write(file_info["content"])
                f.write("\n```\n\n")

    def generate_json(self, analysis_results: Dict, output_path: str):
        """Generate JSON output."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2)

def analyze_github_repo(github_url: str, config_path: Optional[str] = None):
    """Analyze a GitHub repository from a notebook."""
    config = AnalysisConfig.from_file(config_path)
    analyzer = GitHubAnalyzer(config)
    return analyzer.analyze_repository(github_url)

# Batch analysis function
def batch_analyze_repos(repo_list: List[str], config_path: Optional[str] = None):
    """Analyze multiple repositories in batch."""
    total_repos = len(repo_list)
    successful = []
    failed = []
    start_time = datetime.datetime.now()

    print(f"Starting batch analysis of {total_repos} repositories...")
    print("=" * 50)

    for idx, repo_url in enumerate(repo_list, 1):
        try:
            print(f"\n[{idx}/{total_repos}] Analyzing: {repo_url}")
            result = analyze_github_repo(repo_url, config_path)
            if result:
                successful.append(repo_url)
            else:
                failed.append((repo_url, "Analysis failed"))
        except Exception as e:
            failed.append((repo_url, str(e)))
            print(f"Error processing {repo_url}: {e}")

        print("-" * 50)

    # Generate summary report
    duration = datetime.datetime.now() - start_time

    print("\nBatch Analysis Summary")
    print("=" * 50)
    print(f"Time taken: {duration}")
    print(f"Total repositories: {total_repos}")
    print(f"Successfully analyzed: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("\nFailed Repositories:")
        for repo, error in failed:
            print(f"- {repo}: {error}")

print("Github analyzer code is ready to use!")