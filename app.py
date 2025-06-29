from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open("career_data.json", "r") as f:
    data = json.load(f)

career_paths = data.get("career_paths", [])

# Automatically extract all unique interests from keywords
all_keywords = sorted({kw for career in career_paths for kw in career.get("keywords", [])})


@app.route("/")
def index():
    return render_template("index.html", interests=all_interest_names)

@app.route("/result", methods=["POST"])
def result():
    selected_interests = request.form.getlist("interests")
    recommendations = []

    for interest in interests_data:
        if interest["name"] in selected_interests:
            recommendations.append({
                "name": interest["name"],
                "motivation": interest.get("motivation", "Keep pushing forward!"),
                "resources": interest.get("resources", {}),
                "career_paths": interest.get("career_paths", [])
            })

    return render_template("result.html", careers=recommendations, selected_interests=selected_interests)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
