import pytest
from pathlib import Path
from github_repo_analyzer import analyze_github_repo, AnalysisConfig

def test_config_defaults():
    """Test that default configuration is created correctly."""
    config = AnalysisConfig.from_file()
    assert isinstance(config.extensions, set)
    assert isinstance(config.exclude_dirs, set)
    assert config.max_file_size == 1024 * 1024  # 1MB
    assert config.token_encoding == "cl100k_base"
    assert config.max_workers == 4
    assert config.output_format == "markdown"

def test_config_from_dict():
    """Test configuration can be created from dictionary."""
    custom_config = {
        "extensions": [".py", ".js"],
        "exclude_dirs": [".git"],
        "max_file_size": 500000,
        "token_encoding": "cl100k_base",
        "max_workers": 2,
        "output_format": "markdown"
    }
    
    config = AnalysisConfig(
        extensions=set(custom_config["extensions"]),
        exclude_dirs=set(custom_config["exclude_dirs"]),
        max_file_size=custom_config["max_file_size"],
        token_encoding=custom_config["token_encoding"],
        max_workers=custom_config["max_workers"],
        output_format=custom_config["output_format"]
    )
    
    assert len(config.extensions) == 2
    assert ".py" in config.extensions
    assert ".js" in config.extensions
    assert len(config.exclude_dirs) == 1
    assert ".git" in config.exclude_dirs
    assert config.max_file_size == 500000

def test_analyze_repo_basic():
    """Test basic repository analysis."""
    # Use a small test repository
    test_repo = "https://github.com/octocat/Hello-World"
    result = analyze_github_repo(test_repo)
    assert isinstance(result, str)
    assert "Repository Analysis:" in result
    assert "Summary" in result
    assert "File Types" in result