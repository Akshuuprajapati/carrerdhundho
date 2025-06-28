from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load career data from JSON
with open('career_data.json') as f:
    careers = json.load(f)

# Extract all unique interests
all_keywords = sorted(list({kw for c in careers for kw in c["keywords"]}))

@app.route('/')
def index():
    return render_template("index.html", interests=all_keywords)

@app.route('/result', methods=['POST'])
def result():
    selected_interests = request.form.getlist('interests')

    def match_score(career):
        return len(set(selected_interests) & set(career['keywords']))

    # Calculate score and sort careers
    sorted_careers = sorted(careers, key=match_score, reverse=True)
    top_5 = sorted_careers[:5]

    return render_template("result.html", careers=top_5)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)