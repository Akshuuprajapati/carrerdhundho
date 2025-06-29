from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

with open("career_data.json", "r") as f:
    data = json.load(f)
    career_paths = data["career_paths"]

all_keywords = sorted({kw for career in career_paths for kw in career["keywords"]})

motivational_quotes = [
    "Chase your passion, not your pension.",
    "Start where you are. Use what you have. Do what you can.",
    "Believe you can and you're halfway there.",
    "Every expert was once a beginner.",
    "Opportunities don't happen, you create them."
]

job_thoughts = [
    "This role needs a mix of creativity and logic!",
    "Perfect for those who love solving real-world problems.",
    "If you enjoy learning and adapting, this is for you!",
    "You’ll be building the future with this role.",
    "Think big, start small, and grow fast in this role!"
]

@app.route("/")
def index():
    return render_template("index.html", interests=all_keywords)

@app.route("/result", methods=["POST"])
def result():
    selected_interests = request.form.getlist("interests")

    matching_careers = []

    for career in career_paths:
        career_score = len(set(career["keywords"]).intersection(set(selected_interests)))
        matching_jobs = []

        for job in career.get("jobs", []):
            job_keywords = job.get("keywords", [])
            job_score = len(set(job_keywords).intersection(set(selected_interests)))
            if job_score > 0:
                matching_jobs.append({
                    "title": job["title"],
                    "score": job_score,
                    "thought": random.choice(job_thoughts)
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

    return render_template("result.html", careers=top_careers, selected_interests=selected_interests)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
