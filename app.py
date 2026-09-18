import streamlit as st

st.title("NBA point prediction")
height=st.number_input("Predict a height: ")
w=-0.03650734467294015
b=15.534315785648516
prediction=w*height+b
st.write(f"The prediction is {prediction}")
