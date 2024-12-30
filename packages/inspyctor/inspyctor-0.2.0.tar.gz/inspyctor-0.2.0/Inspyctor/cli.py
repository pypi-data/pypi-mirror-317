import sys
from inspyctor.analyzers import Flake8Analyzer, BanditAnalyzer


def main():
    if len(sys.argv) == 1:
        print("Inspyctor version 0.1.0")
        sys.exit(0)

    if len(sys.argv) != 3 or sys.argv[1] != "review":
        print("Usage: inspyctor review <file_path>")
        sys.exit(1)

    file_path = sys.argv[2]

    print("=== Inspyctor Review ===\n")

    # Run Flake8 analysis
    print("Style Issues:")
    flake8_issues = Flake8Analyzer.run(file_path)
    if not flake8_issues:
        print("No style issues found.")
    else:
        print("\n".join(flake8_issues))

    print("\nSecurity Issues:")
    # Run Bandit analysis
    bandit_issues = BanditAnalyzer.run(file_path)
    if not bandit_issues:
        print("No security issues found.")
    else:
        print("\n".join(bandit_issues))


if __name__ == "__main__":
    main()
