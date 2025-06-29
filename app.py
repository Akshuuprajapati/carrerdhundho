from flask import Flask, render_template, request
import json

app = Flask(__name__)

# ✅ Correct: Load interests from correct key
with open("career_data.json", "r") as f:
    data = json.load(f)

interests_data = data.get("interests", [])
all_keywords = sorted([interest["name"] for interest in interests_data])  # Extract names only

@app.route("/")
def index():
    return render_template("index.html", interests=all_keywords)




@app.route("/")
def index():
    return render_template("index.html", interests=all_keywords)


@app.route("/result", methods=["POST"])
def result():
    selected_interests = request.form.getlist("interests")
    recommendations = []

    for interest in interests_data:
        if interest["name"] in selected_interests:
            recommendations.append({
                "title": interest["name"],
                "motivation": interest.get("motivation", ""),
                "resources": interest.get("resources", {}),
                "career_paths": interest.get("career_paths", []),
                "keywords": [interest["name"]]  # for display
            })

    return render_template("result.html", careers=recommendations, selected_interests=selected_interests)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
