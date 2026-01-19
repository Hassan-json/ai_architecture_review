#!/usr/bin/env python3
"""
CLI tool for reviewing software architecture diagrams using AI
"""

import argparse
import os
import sys
from services.ai_reviewer import ArchitectureReviewer
from config import Config


def print_review(result):
    """Pretty print the review result"""
    print("\n" + "=" * 80)
    print("ARCHITECTURE REVIEW RESULTS")
    print("=" * 80 + "\n")

    if result['success']:
        print(f"Model: {result['model']}\n")
        review = result['review']

        # Print Issues
        if 'issues' in review and review['issues']:
            print("\n" + "─" * 80)
            print("POTENTIAL ISSUES & ANTI-PATTERNS")
            print("─" * 80)
            for i, issue in enumerate(review['issues'], 1):
                print(f"\n{i}. Issue: {issue['title']}")
                print(f"   Problem: {issue['problem']}")
                print(f"   Impact: {issue['impact']}")
                print(f"   Mitigation:")
                for m in issue['mitigation']:
                    print(f"      • {m}")

        # Print Security
        if 'security' in review and review['security']:
            print("\n" + "─" * 80)
            print("SECURITY CONCERNS")
            print("─" * 80)
            for i, sec in enumerate(review['security'], 1):
                print(f"\n{i}. Concern: {sec['concern']}")
                print(f"   Risk: {sec['risk']}")
                print(f"   Mitigation:")
                for m in sec['mitigation']:
                    print(f"      • {m}")

        # Print Scalability
        if 'scalability' in review and review['scalability']:
            print("\n" + "─" * 80)
            print("SCALABILITY ISSUES")
            print("─" * 80)
            for i, scale in enumerate(review['scalability'], 1):
                print(f"\n{i}. Issue: {scale['issue']}")
                print(f"   Impact: {scale['impact']}")
                print(f"   Mitigation:")
                for m in scale['mitigation']:
                    print(f"      • {m}")

        # Print Best Practices
        if 'bestPractices' in review and review['bestPractices']:
            print("\n" + "─" * 80)
            print("BEST PRACTICES VIOLATIONS")
            print("─" * 80)
            for i, bp in enumerate(review['bestPractices'], 1):
                print(f"\n{i}. Practice: {bp['practice']}")
                print(f"   Why Important: {bp['whyImportant']}")
                print(f"   Implementation:")
                for impl in bp['implementation']:
                    print(f"      • {impl}")

        # Print Recommendations
        if 'recommendations' in review and review['recommendations']:
            print("\n" + "─" * 80)
            print("PRIORITY RECOMMENDATIONS")
            print("─" * 80)
            for rec in review['recommendations']:
                print(f"\n[Priority {rec['priority']}] {rec['title']}")
                print(f"   {rec['description']}")
                print(f"   Implementation Steps:")
                for j, step in enumerate(rec['steps'], 1):
                    print(f"      {j}. {step}")

        print("\n" + "=" * 80)
    else:
        print(f"ERROR: {result['error']}")
        print("=" * 80)


def print_code_review(result):
    """Pretty print the code review result"""
    print("\n" + "=" * 80)
    print("CODE FLOW REVIEW RESULTS")
    print("=" * 80 + "\n")

    if result['success']:
        print(f"Model: {result['model']}\n")
        review = result['review']

        # Print Flow Issues
        if 'flowIssues' in review and review['flowIssues']:
            print("\n" + "-" * 80)
            print("FLOW ISSUES")
            print("-" * 80)
            for i, issue in enumerate(review['flowIssues'], 1):
                print(f"\n{i}. Location: {issue.get('location', 'N/A')}")
                print(f"   Issue: {issue.get('issue', 'N/A')}")
                print(f"   Impact: {issue.get('impact', 'N/A')}")
                print(f"   Fix: {issue.get('fix', 'N/A')}")

        # Print Code Smells
        if 'codeSmells' in review and review['codeSmells']:
            print("\n" + "-" * 80)
            print("CODE SMELLS")
            print("-" * 80)
            for i, smell in enumerate(review['codeSmells'], 1):
                print(f"\n{i}. Smell: {smell.get('smell', 'N/A')}")
                print(f"   Location: {smell.get('location', 'N/A')}")
                print(f"   Suggestion: {smell.get('suggestion', 'N/A')}")

        # Print Suggestions
        if 'suggestions' in review and review['suggestions']:
            print("\n" + "-" * 80)
            print("SUGGESTIONS")
            print("-" * 80)
            for i, sug in enumerate(review['suggestions'], 1):
                print(f"\n{i}. {sug.get('title', 'N/A')}")
                print(f"   {sug.get('description', 'N/A')}")
                if sug.get('codeExample'):
                    print(f"   Example:\n   {sug['codeExample']}")

        # Print Refactoring Opportunities
        if 'refactoring' in review and review['refactoring']:
            print("\n" + "-" * 80)
            print("REFACTORING OPPORTUNITIES")
            print("-" * 80)
            for i, ref in enumerate(review['refactoring'], 1):
                print(f"\n{i}. What: {ref.get('what', 'N/A')}")
                print(f"   Why: {ref.get('why', 'N/A')}")
                print(f"   How: {ref.get('how', 'N/A')}")

        # Print Priority Changes
        if 'priorityChanges' in review and review['priorityChanges']:
            print("\n" + "-" * 80)
            print("PRIORITY CHANGES")
            print("-" * 80)
            for change in review['priorityChanges']:
                print(f"\n[Priority {change.get('priority', 'N/A')}] {change.get('change', 'N/A')}")
                print(f"   Reason: {change.get('reason', 'N/A')}")

        print("\n" + "=" * 80)
    else:
        print(f"ERROR: {result['error']}")
        print("=" * 80)


def validate_image_path(path):
    """Validate if the image path exists and is a valid file"""
    if not os.path.exists(path):
        print(f"Error: File not found: {path}")
        return False

    if not os.path.isfile(path):
        print(f"Error: Path is not a file: {path}")
        return False

    # Check file extension
    ext = os.path.splitext(path)[1].lower()
    if ext.lstrip('.') not in Config.ALLOWED_EXTENSIONS:
        print(f"Error: Invalid file type. Allowed extensions: {', '.join(Config.ALLOWED_EXTENSIONS)}")
        return False

    return True


def validate_code_path(path):
    """Validate if the code path exists and is a valid file"""
    if not os.path.exists(path):
        print(f"Error: File not found: {path}")
        return False

    if not os.path.isfile(path):
        print(f"Error: Path is not a file: {path}")
        return False

    # Check file extension
    ext = os.path.splitext(path)[1].lower()
    if ext.lstrip('.') not in Config.ALLOWED_CODE_EXTENSIONS:
        print(f"Error: Invalid file type. Allowed extensions: {', '.join(Config.ALLOWED_CODE_EXTENSIONS)}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Review software architecture diagrams or code using AI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Architecture Review:
    %(prog)s -i architecture.png
    %(prog)s --image diagrams/system-design.jpg
    %(prog)s -i arch.png -o review.txt

  Code Flow Review:
    %(prog)s -c mycode.py
    %(prog)s --code services/api.js
    cat mycode.py | %(prog)s --stdin
    %(prog)s -c mycode.py -o review.json

For more information, visit: https://github.com/yourusername/ai-arch-review
        """
    )

    parser.add_argument(
        '-i', '--image',
        help='Path to the architecture diagram image file',
        metavar='PATH'
    )

    parser.add_argument(
        '-c', '--code',
        help='Path to the code file to review',
        metavar='PATH'
    )

    parser.add_argument(
        '--stdin',
        action='store_true',
        help='Read code from stdin (for piping)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Optional: Save review to output file',
        metavar='FILE'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Check if OpenAI API key is set
    if not Config.OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable is not set")
        print("Please create a .env file (copy from .env.example) and add your OpenAI API key")
        sys.exit(1)

    # Determine which mode to run in
    if args.stdin:
        # Code review from stdin
        if args.verbose:
            print("Reading code from stdin...")

        code = sys.stdin.read()
        if not code.strip():
            print("Error: No code provided via stdin")
            sys.exit(1)

        if args.verbose:
            print("Sending code to AI for review...")

        reviewer = ArchitectureReviewer()
        result = reviewer.review_code_flow(code)
        print_code_review(result)

    elif args.code:
        # Code review from file
        if not validate_code_path(args.code):
            sys.exit(1)

        if args.verbose:
            print(f"Processing code file: {args.code}")
            print("Sending to AI for review...")

        # Read code file
        with open(args.code, 'r') as f:
            code = f.read()

        # Detect language from extension
        ext = os.path.splitext(args.code)[1].lower().lstrip('.')
        language_map = {
            'py': 'Python', 'js': 'JavaScript', 'ts': 'TypeScript',
            'java': 'Java', 'go': 'Go', 'rb': 'Ruby', 'php': 'PHP',
            'c': 'C', 'cpp': 'C++', 'rs': 'Rust'
        }
        language = language_map.get(ext)

        reviewer = ArchitectureReviewer()
        result = reviewer.review_code_flow(code, language)
        print_code_review(result)

    elif args.image:
        # Architecture review from image
        if not validate_image_path(args.image):
            sys.exit(1)

        if args.verbose:
            print(f"Processing image: {args.image}")
            print("Sending to AI for review...")

        reviewer = ArchitectureReviewer()
        result = reviewer.review_architecture(args.image)
        print_review(result)

    else:
        print("Error: You must specify either -i/--image, -c/--code, or --stdin")
        parser.print_help()
        sys.exit(1)

    # Save to file if output specified
    if args.output and result['success']:
        try:
            import json
            with open(args.output, 'w') as f:
                json.dump({
                    'model': result['model'],
                    'review': result['review']
                }, f, indent=2)
            print(f"\nReview saved to: {args.output} (JSON format)")
        except Exception as e:
            print(f"Error saving to file: {e}")

    # Exit with appropriate code
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()