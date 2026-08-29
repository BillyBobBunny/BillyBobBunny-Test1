"""
Blair's Portfolio — Flask backend

This app only serves templates and handles the contact form. All page
content lives in the data structures below (SKILL_CATEGORIES, PROJECTS,
ACHIEVEMENTS, HOBBIES) so you can edit copy without touching HTML.
"""
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Placeholder content
# Edit the values below to replace them with your own — no HTML editing
# required for text-only changes.
# ---------------------------------------------------------------------------

SKILL_CATEGORIES = [
    {
        "name": "Programming",
        "skills": [
            {"name": "Python", "level": 85},
            {"name": "JavaScript", "level": 70},
            {"name": "HTML / CSS", "level": 80},
        ],
    },
    {
        "name": "Mathematics",
        "skills": [
            {"name": "Algebra & Calculus", "level": 78},
            {"name": "Statistics", "level": 65},
            {"name": "Competition Math", "level": 72},
        ],
    },
    {
        "name": "Science",
        "skills": [
            {"name": "Chemistry", "level": 90},
            {"name": "Physics", "level": 68},
            {"name": "Lab Technique", "level": 75},
        ],
    },
    {
        "name": "Music",
        "skills": [
            {"name": "Piano", "level": 88},
            {"name": "Music Theory", "level": 70},
        ],
    },
    {
        "name": "Languages",
        "skills": [
            {"name": "English", "level": 95},
            {"name": "French", "level": 80},
        ],
    },
    {
        "name": "Design",
        "skills": [
            {"name": "UI / Visual Design", "level": 60},
            {"name": "Presentation Design", "level": 74},
        ],
    },
]

PROJECTS = [
    {
        "title": "Sample Project One",
        "description": "A short placeholder description of what this project does and why it exists. Swap this out for a real write-up.",
        "image": "project-01.jpg",
        "tech": ["Python", "Flask", "SQLite"],
        "github": "#",
        "demo": "#",
        "learn_more": "#",
    },
    {
        "title": "Sample Project Two",
        "description": "Placeholder text describing the problem this project solves and the approach taken to solve it.",
        "image": "project-02.jpg",
        "tech": ["JavaScript", "Canvas API"],
        "github": "#",
        "demo": "#",
        "learn_more": "#",
    },
    {
        "title": "Sample Project Three",
        "description": "Another placeholder card — replace the title, description, tags, and links with a real project.",
        "image": "project-03.jpg",
        "tech": ["React", "Node.js"],
        "github": "#",
        "demo": "#",
        "learn_more": "#",
    },
    {
        "title": "Sample Project Four",
        "description": "Use this slot for a research project, a creative build, or a competition submission.",
        "image": "project-04.jpg",
        "tech": ["C++", "Data Analysis"],
        "github": "#",
        "demo": "#",
        "learn_more": "#",
    },
]

ACHIEVEMENTS = [
    {
        "date": "2026 — Placeholder",
        "title": "Sample Award or Competition Result",
        "description": "Placeholder description of the achievement, the organization behind it, and why it mattered.",
    },
    {
        "date": "2025 — Placeholder",
        "title": "Sample Certification",
        "description": "Placeholder description of a certification or milestone completed this year.",
    },
    {
        "date": "2025 — Placeholder",
        "title": "Sample Publication or Recognition",
        "description": "Placeholder description of a piece of work that was published, exhibited, or recognized.",
    },
    {
        "date": "2024 — Placeholder",
        "title": "Sample Early Milestone",
        "description": "Placeholder description of an earlier achievement that started this journey.",
    },
]

HOBBIES = [
    {"icon": "💻", "name": "Programming", "description": "Placeholder text about side projects and what you like to build."},
    {"icon": "📚", "name": "Reading", "description": "Placeholder text about favorite genres or a current reading list."},
    {"icon": "🎹", "name": "Music", "description": "Placeholder text about an instrument, genre, or performance experience."},
    {"icon": "📐", "name": "Mathematics", "description": "Placeholder text about competition math or a favorite branch of math."},
    {"icon": "📷", "name": "Photography", "description": "Placeholder text about a preferred style or subject to shoot."},
    {"icon": "🎮", "name": "Gaming", "description": "Placeholder text about favorite games or genres."},
    {"icon": "✈️", "name": "Travel", "description": "Placeholder text about a memorable trip or a place on your list."},
    {"icon": "🌐", "name": "Languages", "description": "Placeholder text about languages studied or a constructed language project."},
]

# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/skills")
def skills():
    return render_template("skills.html", skill_categories=SKILL_CATEGORIES)


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS)


@app.route("/achievements")
def achievements():
    return render_template("achievements.html", achievements=ACHIEVEMENTS)


@app.route("/hobbies")
def hobbies():
    return render_template("hobbies.html", hobbies=HOBBIES)


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------------------------------------------------------------------
# Contact form API
#
# This is a placeholder backend: it validates the submission and logs it to
# the console. It does NOT send real email. See README.md "Next Steps" for
# how to wire this up to an email service (e.g. Flask-Mail, SendGrid) before
# deploying publicly.
# ---------------------------------------------------------------------------


@app.route("/api/contact", methods=["POST"])
def api_contact():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    subject = (data.get("subject") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify(success=False, message="Please fill in your name, email, and message."), 400

    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify(success=False, message="Please enter a valid email address."), 400

    # Placeholder "storage": log to console. Replace with a database write
    # or email send once you're ready to go live.
    timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    print(f"[contact] {timestamp} | {name} <{email}> | subject={subject!r}")
    print(f"[contact] message: {message}")

    return jsonify(success=True, message=f"Thanks, {name.split()[0]} — your message has been received.")


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


@app.errorhandler(404)
def not_found(_error):
    return render_template("index.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
