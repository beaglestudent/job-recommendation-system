import re

# Technical skills our system can recognize
SKILL_DICTIONARY = {
    "Python": ["python"],
    "SQL":["sql"],
    "Java": ["java"],
    "JavaScript": ["javascript", "java script"],
    "R": ["r programming", "r language"],
    "C++":["c++"],
    "C#":["c#"],
    "Kotlin":["kotlin"],
    "Typescript":["typescript"],

    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "NLP": ["natural language processing", "nlp"],
    "Computer Vision": ["computer vision", "cv"],

    "PyTorch": ["pytorch"],
    "TensorFlow": ["tensorflow"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "XGBoost": ["xgboost"],

    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud platform"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes"],

    "Git": ["git", "github", "gitlab"],
    "Linux": ["linux", "unix"],
    "Spark": ["pyspark", "apache spark"],
    "Hadoop": ["hadoop"],

    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel"],

    "FASTAPI": ["fastapi"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Streamlit": ["streamlit"],
}   

def extract_skills(text:str) -> list[str]:
    """
    Extracts technical skills from a given text based on the SKILL_DICTIONARY.
    
    Args:
        text (str): The input text from which to extract skills.
    
    Returns:
        list[str]: A sorted list of unique skills found in the text.
    """

    if not isinstance(text, str):
        return []

    extracted_skills = set()

    for skill, keywords in SKILL_DICTIONARY.items():
        for keyword in keywords:

            # checks that the match does not start inside another word
            # treats characters such as + in C++ lterally
            # checks that the match does not continue in another word
            pattern = (r"(?<!\w)" + re.escape(keyword) + r"(?!\w)")

            if re.search(pattern, text, re.IGNORECASE):
                extracted_skills.add(skill)
                break  # No need to check other keywords for this skill 

    return sorted(extracted_skills, key=str.lower)

if __name__ == "__main__":
    sample_description = """
    We are hirign a Data Science Intern.

    Requirements:
    - Strong Python and SQL programming skills
    - Experience with machine learning and deep learning frameworks such as TensorFlow and PyTorch
    - Familiarity with PyTorch and Pandas
    - Knowledge of Docker and AWS is a plus
    """

    skills = extract_skills(sample_description)
    print("Extracted Skills:", skills)
