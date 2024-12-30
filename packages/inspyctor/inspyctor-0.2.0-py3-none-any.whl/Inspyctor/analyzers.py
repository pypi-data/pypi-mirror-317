class Flake8Analyzer:
    @staticmethod
    def run(file_path):
        """Run Flake8 analysis on the given file."""
        import subprocess

        try:
            result = subprocess.run(
                ["flake8", file_path], capture_output=True, text=True
            )
            output = result.stdout.strip()
            return output.splitlines() if output else []
        except FileNotFoundError:
            return ["Flake8 is not installed. Please install it using `pip install flake8`."]


class BanditAnalyzer:
    @staticmethod
    def run(file_path):
        """Run Bandit analysis on the given file."""
        import subprocess

        try:
            result = subprocess.run(
                ["bandit", "-r", file_path], capture_output=True, text=True
            )
            output = result.stdout.strip()
            # Extract issues from Bandit's output
            issues = []
            for line in output.splitlines():
                if line.startswith(" >>") or line.startswith("[B"):
                    issues.append(line)
            return issues if issues else ["No issues found."]
        except FileNotFoundError:
            return ["Bandit is not installed. Please install it using `pip install bandit`."]
