from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load lightweight CSV data (already updated by you)
MATCH_CSV = "data/match_summary.csv"
OVER_CSV = "data/over_summary.csv"

matches_df = pd.read_csv(MATCH_CSV)
overs_df = pd.read_csv(OVER_CSV)

@app.route("/")
def dashboard():
    # send match list to dropdown
    match_list = matches_df[["match_id", "team1", "team2"]].to_dict(orient="records")
    return render_template("dashboard.html", matches=match_list)

@app.route("/match/<int:match_id>")
def match_analysis(match_id):
    # Match summary
    match = matches_df[matches_df["match_id"] == match_id].iloc[0]

    # Over-wise data
    over_data = overs_df[overs_df["match_id"] == match_id]

    runs_by_over = over_data.groupby("over")["runs"].sum().cumsum().tolist()
    overs = over_data["over"].unique().tolist()

    # Phase-wise stats
    powerplay = over_data[over_data["over"] <= 6]["runs"].sum()
    middle = over_data[(over_data["over"] > 6) & (over_data["over"] <= 15)]["runs"].sum()
    death = over_data[over_data["over"] > 15]["runs"].sum()

    return jsonify({
        "teams": f"{match['team1']} vs {match['team2']}",
        "venue": match["venue"],
        "winner": match["winner"],
        "overs": overs,
        "runs": runs_by_over,
        "phases": {
            "powerplay": int(powerplay),
            "middle": int(middle),
            "death": int(death)
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
