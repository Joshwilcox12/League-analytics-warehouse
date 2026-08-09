import streamlit as st

st.set_page_config(
    page_title="League Analytics",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 League Analytics")
st.header("Best Champion Performance")

# --------------------------------
# Connect to Snowflake
# --------------------------------

conn = st.connection("snowflake")

# --------------------------------
# Query dbt mart
# --------------------------------

df = conn.query("""
    SELECT
        game_name,
        tag_line,
        champion_name,
        games_played,
        win_rate,
        kda,
        lane_cs_per_min,
        jungle_cs_per_min,
        avg_dpm,
        avg_team_damage_percent
    FROM PLAYER_CHAMPION_PERFORMANCE
""")

# --------------------------------
# Create player selector
# --------------------------------

df["PLAYER"] = (
    df["GAME_NAME"]
    + " #"
    + df["TAG_LINE"].astype(str)
)

players = sorted(df["PLAYER"].unique())

selected_player = st.selectbox(
    "Select Player",
    players
)

# --------------------------------
# Filter to selected player
# --------------------------------

player_df = df[
    df["PLAYER"] == selected_player
].copy()

# --------------------------------
# Minimum games filter
# --------------------------------

max_games = int(player_df["GAMES_PLAYED"].max())

min_games = st.slider(
    "Minimum games played",
    min_value=1,
    max_value=max_games,
    value=1
)

filtered_df = player_df[
    player_df["GAMES_PLAYED"] >= min_games
].copy()

# Sort AFTER filtering
filtered_df = filtered_df.sort_values(
    "WIN_RATE",
    ascending=False
)

# --------------------------------
# Best champion
# --------------------------------

if not filtered_df.empty:

    best = filtered_df.iloc[0]

    st.subheader(
        f"🏆 {selected_player}'s Best Champion: "
        f"{best['CHAMPION_NAME']}"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Win Rate",
        f"{best['WIN_RATE']:.1f}%"
    )

    col2.metric(
        "KDA",
        f"{best['KDA']:.2f}"
    )

    col3.metric(
        "Damage / Min",
        f"{best['AVG_DPM']:.0f}"
    )

    col4.metric(
        "Games Played",
        int(best["GAMES_PLAYED"])
    )

    # --------------------------------
    # Win rate chart
    # --------------------------------

    st.subheader("Champion Win Rate")

    chart_data = (
        filtered_df[
            ["CHAMPION_NAME", "WIN_RATE"]
        ]
        .set_index("CHAMPION_NAME")
    )

    st.bar_chart(chart_data)

    # --------------------------------
    # Full champion stats
    # --------------------------------

    st.subheader("Champion Statistics")

    display_df = filtered_df[
        [
            "CHAMPION_NAME",
            "GAMES_PLAYED",
            "WIN_RATE",
            "KDA",
            "LANE_CS_PER_MIN",
            "JUNGLE_CS_PER_MIN",
            "AVG_DPM",
            "AVG_TEAM_DAMAGE_PERCENT"
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning(
        "No champions meet the minimum games requirement."
    )