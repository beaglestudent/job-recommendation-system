
from src.skill_extraction import extract_skills


def test_basic_skill_extraction():
    text = "Experience with Python, SQL and PyTorch."

    result = extract_skills(text)

    assert "Python" in result
    assert "SQL" in result
    assert "PyTorch" in result


def test_case_insensitive():
    text = "Experience with PYTHON and pytorch."

    result = extract_skills(text)

    assert "Python" in result
    assert "PyTorch" in result


def test_avoid_partial_matches():
    text = "We require JavaScript development experience."

    result = extract_skills(text)

    assert "JavaScript" in result
    assert "Java" not in result


def test_duplicate_skills():
    text = "Python, python, PYTHON"

    result = extract_skills(text)

    assert result.count("Python") == 1


def test_empty_input():
    assert extract_skills("") == []
    assert extract_skills(None) == []
