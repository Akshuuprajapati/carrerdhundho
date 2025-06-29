
from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

# Load career data
with open("career_data.json", "r") as f:
    data = json.load(f)
    career_paths = data["career_paths"]
    experience_levels = data["experience_levels"]

# Extract all unique interest keywords
all_keywords = sorted({kw for career in career_paths for kw in career["keywords"]})

# Sample motivational quotes
motivational_quotes = [
    "Success doesn't come to you – you go to it.",
    "The future depends on what you do today.",
    "Your passion is your power – use it wisely.",
    "Dream big, start small, act now.",
    "Don’t watch the clock; do what it does – keep going."
]

@app.route("/")
def index():
    return render_template("index.html", interests=all_keywords, experience_levels=experience_levels)

@app.route("/result", methods=["POST"])
def result():
    selected_interests = request.form.getlist("interests")
    selected_experience = request.form.get("experience")

    matching_careers = []

    for career in career_paths:
        career_score = len(set(career["keywords"]).intersection(set(selected_interests)))
        matching_jobs = []

        for job in career.get("jobs", []):
            job_keywords = job.get("keywords", [])
            job_score = len(set(job_keywords).intersection(set(selected_interests)))
            if job_score > 0 and job.get("experience_level") == selected_experience:
                matching_jobs.append({
                    "title": job["title"],
                    "experience_level": job["experience_level"],
                    "score": job_score
                })

        if career_score > 0 or matching_jobs:
            matching_careers.append({
                "title": career["title"],
                "score": career_score,
                "matching_jobs": sorted(matching_jobs, key=lambda x: x["score"], reverse=True),
                "motivation": random.choice(motivational_quotes)
            })

    sorted_careers = sorted(matching_careers, key=lambda x: x["score"], reverse=True)
    top_careers = sorted_careers[:5]

    return render_template("result.html", careers=top_careers)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
