import streamlit as st
from head_master import *
import pandas as pd
import plotly.express as px


# Définir la couleur de fond avec HTML
st.markdown(
    """
    <style>
        body {
            background-color: #f0f0f0; /* Remplacez ceci par la couleur de fond souhaitée en format hexadécimal ou autre */
        }
    </style>
    """,
    unsafe_allow_html=True
)