"""
GitHub Repository Analyzer
------------------------

A tool for analyzing GitHub repositories and generating detailed markdown reports.

Example usage:
    >>> from github_repo_analyzer import analyze_github_repo
    >>> report = analyze_github_repo("https://github.com/username/repo")
    >>> print(report)
"""

from .analyzer import analyze_github_repo, batch_analyze_repos
from .utils import AnalysisConfig

__version__ = "0.1.0"
__all__ = ["analyze_github_repo", "batch_analyze_repos", "AnalysisConfig"]