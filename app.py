
from flask import Flask, render_template, request

app = Flask(__name__)

def predict_runs(overs):
    return int(overs * 7.5)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    result = None
    if request.method == "POST":
        overs = float(request.form["overs"])
        result = predict_runs(overs)
    return render_template("predict.html", result=result)

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
