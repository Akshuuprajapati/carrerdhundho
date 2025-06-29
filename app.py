from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load career data from JSON
with open("career_data.json", "r") as f:
    data = json.load(f)

career_paths = data.get("career_paths", [])

# Collect all unique keywords for the form
all_keywords = sorted({kw for career in career_paths for kw in career.get("keywords", [])})


@app.route("/")
def index():
    return render_template("index.html", interests=all_keywords)


@app.route("/result", methods=["POST"])
def result():
    selected_interests = request.form.getlist("interests")
    recommendations = []

    for career in career_paths:
        matched_keywords = list(set(career.get("keywords", [])) & set(selected_interests))
        if matched_keywords:
            # Matching job roles with thoughts
            matched_jobs = []
            for job in career.get("jobs", []):
                if set(job.get("keywords", [])) & set(selected_interests):
                    matched_jobs.append({
                        "title": job.get("title", "Job Title"),
                        "thought": job.get("thought", "Stay focused and keep learning!")
                    })

            recommendations.append({
                "title": career.get("title", "Career"),
                "keywords": matched_keywords,
                "motivation": career.get("motivation", "Your passion can lead to great things."),
                "matching_jobs": matched_jobs
            })

    # Sort by number of matched interests and show top 5
    top_careers = sorted(recommendations, key=lambda x: len(x["keywords"]), reverse=True)[:5]

    return render_template("result.html", careers=top_careers, selected_interests=selected_interests)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
