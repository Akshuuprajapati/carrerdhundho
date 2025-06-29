from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load data from career_data.json
with open("career_data.json", "r") as f:
    data = json.load(f)

career_paths = data.get("career_paths", [])

# Extract all unique keywords for interests
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
            matched_jobs = []
            for job in career.get("jobs", []):
                if set(job.get("keywords", [])) & set(selected_interests):
                    matched_jobs.append({
                        "title": job.get("title", "Job Title"),
                        "experience_level": job.get("experience_level", "N/A")
                    })

            recommendations.append({
                "title": career.get("title", "Career"),
                "keywords": matched_keywords,
                "fields": career.get("fields", []),
                "matching_jobs": matched_jobs
            })

    # Sort top 5 best match careers
    top_careers = sorted(recommendations, key=lambda x: len(x["keywords"]), reverse=True)[:5]

    return render_template("result.html", careers=top_careers, selected_interests=selected_interests)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
