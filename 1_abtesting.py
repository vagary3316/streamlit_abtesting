import kagglehub
from kagglehub import KaggleDatasetAdapter
import openpyxl
import streamlit as st

#Streamlit Header and Subheader
st.header('Welcome to my project - AB Testing Data Analysis')
st.text("""
Kaggle - AB Testing Dataset
(https://www.kaggle.com/datasets/cagataytuylu/ab-testing)

This page shows the data processing and every analysis steps.
""")

file_path = "ab_testing.xlsx"

# Load the Control Group from Kaggle
con_df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "cagataytuylu/ab-testing",
  file_path,
  pandas_kwargs={'sheet_name':'Control Group'})

# Load the Test Group from Kaggle
test_df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "cagataytuylu/ab-testing",
  file_path,
  pandas_kwargs={'sheet_name':'Test Group'})


## Present the Control Group in the page using streamlit.df
st.dataframe(con_df)