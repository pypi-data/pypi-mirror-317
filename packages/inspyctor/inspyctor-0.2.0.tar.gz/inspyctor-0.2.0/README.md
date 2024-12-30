# Inspyctor

**Inspyctor** is a command-line tool to review Python code for style and security issues. It uses industry-standard tools like **Flake8** and **Bandit** to provide detailed feedback on your Python files.

---

## Features

- **Style Checks**: Analyze code for PEP 8 compliance using Flake8.
- **Security Checks**: Identify potential security vulnerabilities using Bandit.
- **Easy-to-Use CLI**: Review your code with a single command: `inspyctor review <file_path>`.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/abhishekchaudharygh/inspyctor.git
   cd inspyctor
   ```

2. Install the package:
   ```bash
   pip install .
   ```

3. Ensure the required tools are installed:
   ```bash
   pip install flake8 bandit
   ```

---

## Usage

### Command:
```bash
inspyctor review <file_path>
```

### Example:
```bash
inspyctor review example.py
```

### Output:
```
=== Inspyctor Review ===

Style Issues:
example.py:10:1: W293 blank line contains whitespace

Security Issues:
No security issues found.
```

---

## Requirements

- Python 3.6 or higher
- Flake8 (for style checks)
- Bandit (for security checks)

Install the dependencies with:
```bash
pip install flake8 bandit
```

---

## Development

1. Clone the repository and navigate to its directory:
   ```bash
   git clone https://github.com/yourusername/inspyctor.git
   cd inspyctor
   ```

2. Install the package locally for development:
   ```bash
   pip install -e .
   ```

3. Run tests or experiment with the codebase:
   ```bash
   python -m inspyctor.cli review <file_path>
   ```

---

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Make your changes and commit: `git commit -m "Add feature-name"`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Future Enhancements

- Add support for more linters like `pylint` and `mypy`.
- Include configuration options for custom rules.
- Provide a web-based interface for the review process.
- Explore AI integration for advanced code analysis.

---

### Contact

For questions or support, feel free to reach out:

- GitHub: [@abhishekchaudharygh](https://github.com/abhishekchaudharygh)
- Email: abhishekchaudhary1403@gmail.com

