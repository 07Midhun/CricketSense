from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

matches_df = pd.read_csv("data/match_summary.csv")
overs_df = pd.read_csv("data/over_summary.csv")

TEAM_COLS = [c for c in matches_df.columns if "team" in c.lower()]

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    prediction = None
    if request.method == "POST":
        overs = float(request.form["overs"])
        avg_run_rate = 8.5  # realistic T20-style assumption
        prediction = int(overs * avg_run_rate)
    return render_template("predict.html", prediction=prediction)


# ---------------- ANALYSIS ----------------
@app.route("/analysis")
def analysis():
    match_list = []
    for _, row in matches_df.iterrows():
        teams = " vs ".join(str(row[c]) for c in TEAM_COLS[:2])
        match_list.append({
            "match_id": row["match_id"],
            "teams": teams
        })
    return render_template("analysis.html", matches=match_list)

@app.route("/analysis/<int:match_id>")
def match_analysis(match_id):
    match = matches_df[matches_df["match_id"] == match_id].iloc[0]
    over_data = overs_df[overs_df["match_id"] == match_id]

    runs = over_data.groupby("over")["runs"].sum().cumsum().tolist()
    overs = over_data["over"].tolist()

    return jsonify({
        "teams": " vs ".join(str(match[c]) for c in TEAM_COLS[:2]),
        "overs": overs,
        "runs": runs
    })

# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
