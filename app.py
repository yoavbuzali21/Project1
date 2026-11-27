import streamlit as st
import pandas as pd
import random
import numpy as np

st.set_page_config(page_title="NBA Predictor", page_icon="🏀")

# Model parameters
W=np.array([-1.05789158e-03, -2.81028014e-02, -7.25399727e-02,  1.27346749e+00, 1.72689998e+00])
b =5.5216345564516836


# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("all_seasons.csv")
    df = df[["player_height",
             "player_weight", "age", "reb", "ast", "pts"]].dropna()
    return df

df = load_data()
st.title("🏀 NBA Predictor")
player_height=st.number_input("Height: ")
player_weight=st.number_input("Weight: ")
age=st.number_input("Age: ")
reb=st.number_input("Rebounds: ")
ast=st.number_input("Assists: ")

predict = player_height*W[0]+player_weight*W[1]+age*W[2]+reb*W[3]+ast*W[4]+b
st.Write(predict)
