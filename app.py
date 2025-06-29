from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load career data from career_data.json
with open("career_data.json", "r") as f:
    interest_data = json.load(f)

interests_list = interest_data.get("interests", [])

# Extract list of interest names
all_interest_names = sorted([item["name"] for item in interests_list])

@app.route("/")
def index():
    return render_template("index.html", interests=all_interest_names)

@app.route("/result", methods=["POST"])
def result():
    selected_interests = request.form.getlist("interests")
    recommendations = []

    for interest in interests_list:
        if interest["name"] in selected_interests:
            recommendations.append({
                "title": interest["name"],
                "motivation": interest.get("motivation", ""),
                "resources": interest.get("resources", {}),
                "career_paths": interest.get("career_paths", [])
            })

    return render_template("result.html", careers=recommendations, selected_interests=selected_interests)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
