from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load interest-based data
with open("career_data.json", "r") as f:
    data = json.load(f)

interest_data = data.get("interests", [])

# Extract all interest names
all_interest_names = sorted([item["name"] for item in interest_data])

@app.route("/")
def index():
    return render_template("index.html", interests=all_interest_names)

@app.route("/result", methods=["POST"])
def result():
    selected_interests = request.form.getlist("interests")
    recommendations = []

    for item in interest_data:
        if item["name"] in selected_interests:
            recommendations.append({
                "title": item["name"],
                "motivation": item.get("motivation", ""),
                "resources": item.get("resources", {}),
                "career_paths": item.get("career_paths", [])
            })

    return render_template("result.html", careers=recommendations, selected_interests=selected_interests)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
