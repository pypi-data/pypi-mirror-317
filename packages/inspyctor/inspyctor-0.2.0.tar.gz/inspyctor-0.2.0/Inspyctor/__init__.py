from .inspycts.ai_inspyct import analyze_code_with_ai
from .inspycts.static_inspyct import run_flake8, run_bandit
from .utils.file_handler import read_code


def review_code(file_path):
    """
    Reviews a Python file and provides static analysis and AI-based suggestions.
    """
    try:
        code = read_code(file_path)
    except FileNotFoundError as e:
        return {"Error": str(e)}

    # Static Analysis
    flake8_feedback = run_flake8(file_path)
    bandit_feedback = run_bandit(file_path)

    # AI Suggestions
    ai_feedback = analyze_code_with_ai(code)

    return {
        "Style Issues": flake8_feedback,
        "Security Issues": bandit_feedback,
        "AI Suggestions": ai_feedback,
    }
