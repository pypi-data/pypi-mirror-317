import argparse
from .analyzer import analyze_github_repo, batch_analyze_repos

def main():
    """Command-line interface for GitHub Repository Analyzer."""
    parser = argparse.ArgumentParser(
        description='Analyze GitHub repositories and generate markdown reports'
    )
    parser.add_argument(
        '--url',
        type=str,
        help='GitHub repository URL to analyze'
    )
    parser.add_argument(
        '--batch',
        type=str,
        help='Path to file containing repository URLs (one per line)'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration JSON file'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path for the markdown report'
    )
    
    args = parser.parse_args()

    if args.batch:
        try:
            with open(args.batch) as f:
                repos = [line.strip() for line in f if line.strip()]
            results = batch_analyze_repos(repos, args.config)
            
            if args.output:
                with open(args.output, 'w') as f:
                    for url, report in results.items():
                        f.write(f"\n\n{'='*80}\n\n")
                        f.write(report)
            else:
                for url, report in results.items():
                    print(f"\n{'='*80}\n")
                    print(report)
                    
        except Exception as e:
            print(f"Error processing batch file: {e}")
            
    elif args.url:
        try:
            report = analyze_github_repo(args.url, args.config)
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(report)
            else:
                print(report)
        except Exception as e:
            print(f"Error analyzing repository: {e}")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()