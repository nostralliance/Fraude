import streamlit as st
import tensorflow as tf

st.title("Test de Streamlit et TensorFlow")

# Affichage de la version de TensorFlow
st.write(f"Version de TensorFlow: {tf.__version__}")

if st.button("Calculer 2 + 2"):
    st.write("2 + 2 = ", 2 + 2)
