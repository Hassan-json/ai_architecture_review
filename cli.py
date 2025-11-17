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


def main():
    parser = argparse.ArgumentParser(
        description='Review software architecture diagrams using AI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '-i', '--image',
        required=True,
        help='Path to the architecture diagram image file',
        metavar='PATH'
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

    # Validate image path
    if not validate_image_path(args.image):
        sys.exit(1)

    if args.verbose:
        print(f"Processing image: {args.image}")
        print("Sending to AI for review...")

    # Initialize reviewer and get review
    reviewer = ArchitectureReviewer()
    result = reviewer.review_architecture(args.image)

    # Print results
    print_review(result)

    # Save to file if output specified
    if args.output and result['success']:
        try:
            import json
            with open(args.output, 'w') as f:
                # Save as JSON for easy parsing
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
