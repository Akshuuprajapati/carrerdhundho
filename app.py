from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load interest data from JSON
with open("interest_data.json", "r") as f:
    data = json.load(f)

interests_data = data.get("interests", [])

# Collect all interest names for the form
all_interest_names = sorted([interest["name"] for interest in interests_data])

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
