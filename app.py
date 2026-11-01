import streamlit as st

st.title("NBA point prediction")
if st.button("start"):
  height=st.number_input("Predict a height: ")
  weight=st.number_input("Predict a weight: ")
  w1=-0.07072934956142778
  w2=0.030519406728451052
  b=19.337737482061705
  prediction=w1*height+w2*weight+b
  st.write(f"The prediction is {prediction}")


