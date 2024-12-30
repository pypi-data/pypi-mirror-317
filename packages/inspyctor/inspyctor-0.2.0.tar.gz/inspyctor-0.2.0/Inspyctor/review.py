import subprocess


def run_flake8(file_path):
    """Run Flake8 for style checks."""
    try:
        result = subprocess.run(
            ['flake8', file_path],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() or "No style issues found."
    except FileNotFoundError:
        return "Flake8 is not installed. Please install it using `pip install flake8`."


def run_bandit(file_path):
    """Run Bandit for security checks."""
    try:
        result = subprocess.run(
            ['bandit', '-r', file_path],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() or "No security issues found."
    except FileNotFoundError:
        return "Bandit is not installed. Please install it using `pip install bandit`."


def review_code(file_path):
    """Run all code review tools on the given file."""
    style_issues = run_flake8(file_path)
    security_issues = run_bandit(file_path)

    return {
        "Style Issues": style_issues,
        "Security Issues": security_issues,
    }
