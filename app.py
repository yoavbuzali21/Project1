import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="NBA Predictor", page_icon="🏀")

# Model parameters
w1 = -0.07072934956142778
w2 = 0.030519406728451052
b = 19.337737482061705

# Game settings
TOTAL_ROUNDS = 5

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("all_seasons.csv")
    df = df[["player_name", "player_height",
             "player_weight", "pts"]].dropna()
    return df

df = load_data()

# Initialize game
if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "round" not in st.session_state:
    st.session_state.round = 0

if "user_score" not in st.session_state:
    st.session_state.user_score = 0

if "model_score" not in st.session_state:
    st.session_state.model_score = 0

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answered" not in st.session_state:
    st.session_state.answered = False


st.title("🏀 NBA Predictor")
st.subheader("Can you beat the machine?")


# Start screen
if not st.session_state.game_started:

    st.write("### Welcome to NBA Predictor!")

    st.write("""
    **Game rules:**

    1. You will play 5 rounds.
    2. In each round, you will see a real NBA player.
    3. You will get the player's height and weight.
    4. Try to predict how many points the player scored.
    5. The AI model will make its own prediction.
    6. After each round, you will see the real result.

    **Scoring:**
    - The closer your prediction is to the real result,
      the more points you receive.
    - The model gets points according to the same rule.
    - At the end, we compare your score with the model's score.
    """)

    if st.button("Start Game"):
        st.session_state.questions = df.sample(
            TOTAL_ROUNDS, random_state=random.randint(1, 100000)
        ).to_dict("records")

        st.session_state.round = 0
        st.session_state.user_score = 0
        st.session_state.model_score = 0
        st.session_state.answered = False
        st.session_state.game_started = True
        st.rerun()


# Game screen
elif st.session_state.round < TOTAL_ROUNDS:

    current = st.session_state.questions[
        st.session_state.round
    ]

    st.progress(
        (st.session_state.round + 1) / TOTAL_ROUNDS
    )

    st.write(
        f"### Round {st.session_state.round + 1} "
        f"out of {TOTAL_ROUNDS}"
    )

    st.write(f"**Player:** {current['player_name']}")
    st.write(f"**Height:** {current['player_height']} cm")
    st.write(f"**Weight:** {current['player_weight']} kg")

    prediction = (
        w1 * current["player_height"]
        + w2 * current["player_weight"]
        + b
    )

    if not st.session_state.answered:

        user_guess = st.number_input(
            "How many points do you think the player scored?",
            min_value=0,
            max_value=100,
            step=1,
            key=f"guess_{st.session_state.round}"
        )

        if st.button("Submit Answer"):

            actual = current["pts"]

            user_distance = abs(user_guess - actual)
            model_distance = abs(prediction - actual)

            user_points = max(0, 100 - int(user_distance * 2))
            model_points = max(0, 100 - int(model_distance * 2))

            st.session_state.user_score += user_points
            st.session_state.model_score += model_points

            st.session_state.user_points = user_points
            st.session_state.model_points = model_points
            st.session_state.user_guess = user_guess
            st.session_state.prediction = prediction
            st.session_state.actual = actual

            st.session_state.answered = True
            st.rerun()

    else:

        st.write("### Round Results")

        st.write(
            f"Your prediction: {st.session_state.user_guess}"
        )

        st.write(
            f"AI prediction: {st.session_state.prediction:.2f}"
        )

        st.write(
            f"Actual points: {st.session_state.actual:.2f}"
        )

        st.write(
            f"Your score this round: "
            f"{st.session_state.user_points}"
        )

        st.write(
            f"AI score this round: "
            f"{st.session_state.model_points}"
        )

        st.write("---")
        st.write(f"Your total score: {st.session_state.user_score}")
        st.write(f"AI total score: {st.session_state.model_score}")

        if st.button("Next Round"):
            st.session_state.round += 1
            st.session_state.answered = False
            st.rerun()


# End screen
else:

    st.title("🏆 Game Over!")

    st.write(f"Your final score: {st.session_state.user_score}")
    st.write(f"AI final score: {st.session_state.model_score}")

    if st.session_state.user_score > st.session_state.model_score:
        st.success("Congratulations! You beat the AI!")
    elif st.session_state.user_score < st.session_state.model_score:
        st.info("The AI won this time!")
    else:
        st.warning("It's a tie!")

    if st.button("Play Again"):
        st.session_state.game_started = False
        st.session_state.round = 0
        st.session_state.user_score = 0
        st.session_state.model_score = 0
        st.session_state.answered = False
        st.rerun()
