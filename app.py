from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load career data from JSON
with open("career_data.json", "r", encoding="utf-8") as f:
    careers = json.load(f)

def match_careers(user_interests):
    scores = []
    for career in careers:
        match_score = len(set(user_interests) & set(career["keywords"]))
        if match_score > 0:
            scores.append((match_score, career))
    scores.sort(reverse=True, key=lambda x: x[0])
    return [career for score, career in scores[:5]]  # top 5

@app.route("/")
def index():
    # Collect all unique interests from data
    all_keywords = sorted({kw for career in careers for kw in career["keywords"]})
    return render_template("index.html", interests=all_keywords)

@app.route("/result", methods=["POST"])
def result():
    selected_interests = request.form.getlist("interests")
    matched_careers = match_careers(selected_interests)
    return render_template("result.html", careers=matched_careers, selected_interests=selected_interests)

if __name__ == "__main__":
    app.run(debug=True)