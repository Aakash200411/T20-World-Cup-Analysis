import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load datasets
@st.cache_data
def load_data():
    summary = pd.read_csv("Match Summary.csv")
    batting_summary = pd.read_csv("Batting summaries for every match.csv")
    bowling_summary = pd.read_csv("Bowling summaries for every match.csv")
    player_info = pd.read_csv("Player_Info with Images T20 WC 2024.csv")
    complete_batting_summary = pd.read_csv("complete_batting_summary.csv")
    complete_bowling_summary = pd.read_csv("complete_bowling_summary.csv")

    return {
        "Match Summary": summary,
        "Batting Summary": batting_summary,
        "Bowling Summary": bowling_summary,
        "Player Info": player_info,
        "Complete Batting Summary": complete_batting_summary,
        "Complete Bowling Summary": complete_bowling_summary,
    }

# Load Data
data_dict = load_data()

# Sidebar: Select Dataset
st.sidebar.header("📂 Select Dataset")
selected_dataset = st.sidebar.selectbox("Choose a dataset", list(data_dict.keys()))

# Load the selected dataset
df = data_dict[selected_dataset]

# Display dataset properly
st.title(f"📊 {selected_dataset} - T20 World Cup 2024 Dashboard")
st.dataframe(df)

# 🎯 Match Summary Analysis
if selected_dataset == "Match Summary":

    # 1️⃣ **Filter by Stage**
    if "Stage" in df.columns:
        selected_stage = st.sidebar.selectbox("📌 Select Match Stage", df["Stage"].unique())
        df = df[df["Stage"] == selected_stage]
        st.write(f"Showing data for **{selected_stage}** stage")
        st.dataframe(df)

    # 2️⃣ **Teams with Most Wins**
    if "Winners" in df.columns:
        st.subheader("🏆 Most Wins by Teams")
        team_wins = df["Winners"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(team_wins.index, team_wins.values, color='green')
        ax.set_xlabel("Teams")
        ax.set_ylabel("Number of Wins")
        ax.set_title("🏆 Most Wins by Teams")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # 3️⃣ **Toss Decision Analysis**
    if "Toss Winning" in df.columns and "Toss Decision" in df.columns:
        st.subheader("🪙 Toss Decisions - Bat vs Bowl")

        toss_decisions = df.groupby("Toss Decision")["Toss Winning"].count()

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(toss_decisions, labels=toss_decisions.index, autopct='%1.1f%%', colors=['blue', 'orange'], startangle=90)
        ax.set_title("🪙 Toss Decisions - Bat vs Bowl")
        st.pyplot(fig)

    # 4️⃣ **Winning Margin Analysis**
    if "Won by" in df.columns and "Winning Margin" in df.columns:
        st.subheader("📊 How Teams Won Matches")

        win_by_runs = df[df["Won by"] == "Runs"]["Winning Margin"].astype(int)
        win_by_wickets = df[df["Won by"] == "Wickets"]["Winning Margin"].astype(int)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(win_by_runs, bins=10, alpha=0.7, color='red', label="Wins by Runs")
        ax.hist(win_by_wickets, bins=10, alpha=0.7, color='blue', label="Wins by Wickets")
        ax.set_xlabel("Winning Margin")
        ax.set_ylabel("Number of Matches")
        ax.set_title("📊 Distribution of Winning Margins")
        ax.legend()
        st.pyplot(fig)

    # 5️⃣ **Top Player of the Match Winners**
    if "Player Of The Match" in df.columns:
        st.subheader("🌟 Most Player of the Match Awards")

        best_players = df["Player Of The Match"].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(best_players.index[::-1], best_players.values[::-1], color='purple')
        ax.set_xlabel("Number of Awards")
        ax.set_ylabel("Players")
        ax.set_title("🌟 Most Player of the Match Awards")
        st.pyplot(fig)
# 🎯 Batting Performance Analysis
if selected_dataset == "Complete Batting Summary":

    # 1️⃣ **Top Run Scorers**
    st.subheader("🏏 Top Run Scorers")
    top_scorers = df.groupby("batsmanName")["total_runs"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_scorers.index[::-1], top_scorers.values[::-1], color='blue')
    ax.set_xlabel("Total Runs")
    ax.set_ylabel("Batsmen")
    ax.set_title("🏏 Top 10 Run Scorers")
    st.pyplot(fig)

    # 2️⃣ **Best Strike Rates (Minimum 100 runs)**
    st.subheader("⚡ Best Strike Rates (Min 100 Runs)")
    best_strike_rates = df[df["total_runs"] > 100].sort_values(by="batting_sr", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(best_strike_rates["batsmanName"][::-1], best_strike_rates["batting_sr"][::-1], color='green')
    ax.set_xlabel("Strike Rate")
    ax.set_ylabel("Batsmen")
    ax.set_title("⚡ Best Strike Rates (Min 100 Runs)")
    st.pyplot(fig)

    # 3️⃣ **Most Boundaries (4s & 6s)**
    st.subheader("🔥 Most Boundaries Hit")
    df["total_boundaries"] = df["4s"] + df["6s"]
    top_boundaries = df.groupby("batsmanName")["total_boundaries"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_boundaries.index[::-1], top_boundaries.values[::-1], color='red')
    ax.set_xlabel("Total Boundaries (4s + 6s)")
    ax.set_ylabel("Batsmen")
    ax.set_title("🔥 Most Boundaries Hit")
    st.pyplot(fig)

    # 4️⃣ **Most Consistent Batsmen (Best Batting Averages)**
    st.subheader("📈 Best Batting Averages (Min 5 Innings)")
    consistent_batsmen = df[df["total_bat_innings"] >= 5].sort_values(by="batting_avg", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(consistent_batsmen["batsmanName"][::-1], consistent_batsmen["batting_avg"][::-1], color='purple')
    ax.set_xlabel("Batting Average")
    ax.set_ylabel("Batsmen")
    ax.set_title("📈 Best Batting Averages (Min 5 Innings)")
    st.pyplot(fig)

    # 5️⃣ **Percentage of Runs Scored via Boundaries**
    st.subheader("🎯 % of Runs Scored via Boundaries")
    boundary_percentage = df.groupby("batsmanName")["runs % by boundary"].mean().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(boundary_percentage.index[::-1], boundary_percentage.values[::-1], color='orange')
    ax.set_xlabel("Boundary %")
    ax.set_ylabel("Batsmen")
    ax.set_title("🎯 % of Runs Scored via Boundaries")
    st.pyplot(fig)
# 🎯 Bowling Performance Analysis
if selected_dataset == "Complete Bowling Summary":

    # 1️⃣ **Top Wicket-Takers**
    st.subheader("🔥 Top Wicket-Takers")
    top_wickets = df.groupby("bowlerName")["total_wickets"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_wickets.index[::-1], top_wickets.values[::-1], color='blue')
    ax.set_xlabel("Total Wickets")
    ax.set_ylabel("Bowlers")
    ax.set_title("🔥 Top 10 Wicket-Takers")
    st.pyplot(fig)

    # 2️⃣ **Best Economy Rate (Min 5 innings)**
    st.subheader("📉 Best Economy Rate (Min 5 Innings)")
    best_economy = df[df["total_bowl_innings"] >= 5].sort_values(by="bowling_ecn", ascending=True).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(best_economy["bowlerName"][::-1], best_economy["bowling_ecn"][::-1], color='green')
    ax.set_xlabel("Economy Rate")
    ax.set_ylabel("Bowlers")
    ax.set_title("📉 Best Economy Rates (Min 5 Innings)")
    st.pyplot(fig)

    # 3️⃣ **Best Bowling Strike Rate (Min 5 innings)**
    st.subheader("⚡ Best Bowling Strike Rates (Min 5 Innings)")
    best_sr = df[df["total_bowl_innings"] >= 5].sort_values(by="bowling_sr", ascending=True).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(best_sr["bowlerName"][::-1], best_sr["bowling_sr"][::-1], color='purple')
    ax.set_xlabel("Bowling Strike Rate")
    ax.set_ylabel("Bowlers")
    ax.set_title("⚡ Best Bowling Strike Rates (Min 5 Innings)")
    st.pyplot(fig)

    # 4️⃣ **Most Dot Balls Bowled**
    st.subheader("🎯 Most Dot Balls Bowled")
    most_dot_balls = df.groupby("bowlerName")["dotBalls"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(most_dot_balls.index[::-1], most_dot_balls.values[::-1], color='orange')
    ax.set_xlabel("Total Dot Balls")
    ax.set_ylabel("Bowlers")
    ax.set_title("🎯 Most Dot Balls Bowled")
    st.pyplot(fig)

    # 5️⃣ **Most Runs Conceded**
    st.subheader("🚨 Most Runs Conceded")
    most_runs_conceded = df.groupby("bowlerName")["runsConceded"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(most_runs_conceded.index[::-1], most_runs_conceded.values[::-1], color='red')
    ax.set_xlabel("Total Runs Conceded")
    ax.set_ylabel("Bowlers")
    ax.set_title("🚨 Most Runs Conceded")
    st.pyplot(fig)

    # 6️⃣ **Most Extras Conceded (Wides + No Balls)**
    st.subheader("⚠️ Most Extras Conceded")
    df["total_extras"] = df["wides"] + df["noBalls"]
    most_extras = df.groupby("bowlerName")["total_extras"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(most_extras.index[::-1], most_extras.values[::-1], color='brown')
    ax.set_xlabel("Total Extras (Wides + No Balls)")
    ax.set_ylabel("Bowlers")
    ax.set_title("⚠️ Most Extras Conceded")
    st.pyplot(fig)
# 🏏 Batting Performance Analysis
if selected_dataset == "Batting Summary":

    # 1️⃣ **Top Run Scorers**
    st.subheader("🔥 Top Run Scorers")
    top_scorers = df.groupby("batsmanName")["runs"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_scorers.index[::-1], top_scorers.values[::-1], color='blue')
    ax.set_xlabel("Total Runs")
    ax.set_ylabel("Batsmen")
    ax.set_title("🔥 Top 10 Run Scorers")
    st.pyplot(fig)

    # 2️⃣ **Highest Strike Rate (Min 50 Balls Faced)**
    st.subheader("⚡ Highest Strike Rates (Min 50 Balls Faced)")
    high_sr = df[df["balls"] >= 50].groupby("batsmanName")["SR"].mean().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(high_sr.index[::-1], high_sr.values[::-1], color='green')
    ax.set_xlabel("Strike Rate")
    ax.set_ylabel("Batsmen")
    ax.set_title("⚡ Highest Strike Rates (Min 50 Balls Faced)")
    st.pyplot(fig)

    # 3️⃣ **Most Sixes & Fours Hit**
    st.subheader("💥 Most Sixes & Fours")
    most_sixes = df.groupby("batsmanName")["6s"].sum().sort_values(ascending=False).head(10)
    most_fours = df.groupby("batsmanName")["4s"].sum().sort_values(ascending=False).head(10)

    col1, col2 = st.columns(2)
    with col1:
        st.write("🔴 **Most Sixes**")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.barh(most_sixes.index[::-1], most_sixes.values[::-1], color='red')
        ax.set_xlabel("Total Sixes")
        ax.set_title("🔴 Most Sixes Hit")
        st.pyplot(fig)

    with col2:
        st.write("🔵 **Most Fours**")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.barh(most_fours.index[::-1], most_fours.values[::-1], color='blue')
        ax.set_xlabel("Total Fours")
        ax.set_title("🔵 Most Fours Hit")
        st.pyplot(fig)

    # 4️⃣ **Most Balls Faced**
    st.subheader("🛡️ Most Balls Faced")
    most_balls = df.groupby("batsmanName")["balls"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(most_balls.index[::-1], most_balls.values[::-1], color='purple')
    ax.set_xlabel("Total Balls Faced")
    ax.set_ylabel("Batsmen")
    ax.set_title("🛡️ Most Balls Faced")
    st.pyplot(fig)

    # 5️⃣ **Dismissal Type Analysis**
    st.subheader("🚪 Dismissal Type Analysis")
    dismissal_counts = df["out/not_out"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(dismissal_counts, labels=dismissal_counts.index, autopct='%1.1f%%', colors=['gray', 'orange'])
    ax.set_title("🚪 Out vs. Not Out Ratio")
    st.pyplot(fig)
# 🏏 Bowling Performance Analysis
if selected_dataset == "Bowling Summary":

    # 1️⃣ **Top Wicket-Takers**
    st.subheader("🎯 Top Wicket-Takers")
    top_wickets = df.groupby("bowlerName")["wickets"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_wickets.index[::-1], top_wickets.values[::-1], color='orange')
    ax.set_xlabel("Total Wickets")
    ax.set_ylabel("Bowlers")
    ax.set_title("🎯 Top 10 Wicket-Takers")
    st.pyplot(fig)

    # 3️⃣ **Most Dot Balls Bowled**
    st.subheader("⏳ Most Dot Balls Bowled")
    most_dot_balls = df.groupby("bowlerName")["dotBalls"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(most_dot_balls.index[::-1], most_dot_balls.values[::-1], color='blue')
    ax.set_xlabel("Total Dot Balls")
    ax.set_ylabel("Bowlers")
    ax.set_title("⏳ Most Dot Balls Bowled")
    st.pyplot(fig)

    # 4️⃣ **Most Runs Conceded**
    st.subheader("🔥 Most Runs Conceded")
    most_runs = df.groupby("bowlerName")["runsConceded"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(most_runs.index[::-1], most_runs.values[::-1], color='red')
    ax.set_xlabel("Total Runs Conceded")
    ax.set_ylabel("Bowlers")
    ax.set_title("🔥 Most Runs Conceded")
    st.pyplot(fig)

    # 5️⃣ **Most Maidens Bowled**
    st.subheader("🎯 Most Maidens Bowled")
    most_maidens = df.groupby("bowlerName")["maiden"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(most_maidens.index[::-1], most_maidens.values[::-1], color='purple')
    ax.set_xlabel("Total Maidens")
    ax.set_ylabel("Bowlers")
    ax.set_title("🎯 Most Maidens Bowled")
    st.pyplot(fig)

    # 6️⃣ **Most Extras Given (Wide & No-Balls)**
    st.subheader("⚠️ Most Extras Given")
    df["Extras"] = df["wides"] + df["noBalls"]
    most_extras = df.groupby("bowlerName")["Extras"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(most_extras.index[::-1], most_extras.values[::-1], color='brown')
    ax.set_xlabel("Total Extras (Wides + No-Balls)")
    ax.set_ylabel("Bowlers")
    ax.set_title("⚠️ Most Extras Given")
    st.pyplot(fig)
