from flask import Flask, render_template, request
import os
import PyPDF2

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# =========================
# LOAD AI MODEL
# =========================

model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================
# UPLOAD FOLDER
# =========================

UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =========================
# EXTRACT TEXT FROM PDF
# =========================

def extract_text(pdf_path):

    text = ""

    with open(pdf_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + " "

    return text

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    return render_template("index.html")

# =========================
# UPLOAD & ANALYZE
# =========================

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]
    job_description = request.form["job_description"]

    if file:

        # =========================
        # SAVE RESUME
        # =========================

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        # =========================
        # EXTRACT RESUME TEXT
        # =========================

        resume_text = extract_text(filepath)

        resume_lower = resume_text.lower()
        job_lower = job_description.lower()

        # =========================
        # AI SEMANTIC MATCH SCORE
        # =========================

        embeddings = model.encode(
            [resume_text, job_description]
        )

        similarity = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )

        score = round(
            similarity[0][0] * 100,
            2
        )

        # =========================
        # SKILLS MATCHING
        # =========================

        skills = [
            "python",
            "java",
            "javascript",
            "html",
            "css",
            "flask",
            "django",
            "react",
            "sql",
            "mongodb",
            "machine learning",
            "ai",
            "data structures",
            "algorithms",
            "competitive programming",
            "problem solving",
            "git",
            "github",
            "api",
            "team collaboration",
            "communication",
            "documentation"
        ]

        matched_skills = []
        missing_skills = []

        for skill in skills:

            if skill in resume_lower:
                matched_skills.append(skill)

            elif skill in job_lower:
                missing_skills.append(skill)

        # =========================
        # AI ANALYSIS
        # =========================

        strengths = (
            ", ".join(matched_skills[:8])
            if matched_skills
            else "Programming and development skills"
        )

        missing = (
            ", ".join(missing_skills)
            if missing_skills
            else "No major missing skills found"
        )

        analysis = f"""
Resume Strengths:
• Strong background in {strengths}
• Good academic profile with technical projects
• GitHub and development experience add value
• Shows interest in software engineering and AI technologies

Missing Skills:
• {missing}

Suggestions to Improve:
• Add more DSA and competitive programming achievements
• Mention communication and collaboration experience
• Add internship availability
• Include deployment and API integration projects
• Add coding profile links like LeetCode/HackerRank
"""

        # =========================
        # MATCHING CHART
        # =========================

        requirements = {
            "Python": "python" in resume_lower,

            "DSA / Competitive Programming":
            (
                "data structures" in resume_lower or
                "algorithms" in resume_lower or
                "competitive programming" in resume_lower
            ),

            "Problem Solving":
            "problem solving" in resume_lower,

            "Web Development":
            (
                "html" in resume_lower or
                "css" in resume_lower or
                "javascript" in resume_lower or
                "flask" in resume_lower
            ),

            "GitHub":
            "github" in resume_lower,

            "Team Collaboration":
            "team" in resume_lower,

            "Technical Documentation":
            "documentation" in resume_lower,

            "Communication Skills":
            "communication" in resume_lower,

            "Immediate Joining":
            (
                "immediately" in resume_lower or
                "available to join" in resume_lower
            )
        }

        matching_chart = []

        for skill, status in requirements.items():

            matching_chart.append({
                "skill": skill,
                "status": "✅ Matched" if status else "❌ Missing"
            })

        # =========================
        # SEND TO HTML
        # =========================

        return render_template(
            "index.html",
            score=score,
            analysis=analysis,
            matching_chart=matching_chart
        )

    return "Upload Failed"

# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)