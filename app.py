from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Backend API URL
API_URL = "https://conceptifier.onrender.com/test"

@app.route("/", methods=["GET", "POST"])
def index():
    explanation = None
    if request.method == "POST":
        concept = request.form["concept"]
        complexity = request.form["complexity"]
        
        response = requests.get(f"{API_URL}?concept={concept}&complexity={complexity}")
        
        if response.status_code == 200:
            explanation = response.text
        else:
            explanation = "Error fetching explanation. Please try again."

    return render_template("index.html", explanation=explanation)

if __name__ == "__main__":
    app.run(debug=True)
