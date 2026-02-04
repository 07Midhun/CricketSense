from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

matches_df = pd.read_csv("data/match_summary.csv")
overs_df = pd.read_csv("data/over_summary.csv")

# 🔹 MAKE DASHBOARD THE ANALYSIS PAGE
@app.route("/")
@app.route("/analysis")
def analysis():
    match_list = matches_df[["match_id", "team1", "team2"]].to_dict(orient="records")
    return render_template("dashboard.html", matches=match_list)

@app.route("/match/<int:match_id>")
def match_analysis(match_id):
    match = matches_df[matches_df["match_id"] == match_id].iloc[0]
    over_data = overs_df[overs_df["match_id"] == match_id]

    runs = over_data.groupby("over")["runs"].sum().cumsum().tolist()
    overs = over_data["over"].tolist()

    return jsonify({
        "teams": f"{match['team1']} vs {match['team2']}",
        "venue": match["venue"],
        "winner": match["winner"],
        "overs": overs,
        "runs": runs
    })
