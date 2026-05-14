skills_list = [

    "python",
    "java",
    "html",
    "css",
    "javascript",
    "sql",
    "flask",
    "django",
    "machine learning",
    "data science",
    "c",
    "c++",
    "react",
    "nodejs"

]


def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in skills_list:

        if skill in text:
            found_skills.append(skill)

    return found_skills