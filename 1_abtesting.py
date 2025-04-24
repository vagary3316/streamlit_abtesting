import kagglehub
from kagglehub import KaggleDatasetAdapter
import openpyxl
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## streamlit_setting
st.set_page_config(layout="wide",
                   page_title="AB Testing Data Analysis",
                   page_icon=":Chart:")

#Streamlit Header and Subheader
st.header(' *WIP* Welcome to my project - AB Testing Data Analysis')
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
    pandas_kwargs={'sheet_name': 'Control Group'})

# Load the Test Group from Kaggle
test_df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "cagataytuylu/ab-testing",
    file_path,
    pandas_kwargs={'sheet_name': 'Test Group'})

st.subheader(":bulb: Data Description:")
st.text("""
There are two datasets - Control Group and Test Group
Both are 40 rows with 4 attributes(impression, click, purchase, earning)
There is no missing value in the datasets.
""")
## Describe the two datasets
st.text("""
Descriptive Statistics: Control Group and Test Group
1. Impressions are higher in Test Group
2. But Clicks are higher in Control Group (better CTR in control group)
3. Purchase and Earning are higher in Test Group (better Conversion Rate in Test Group)
""")

st.text("Control Group")
st.dataframe(con_df.describe().reset_index())

st.text("Test Group")
st.dataframe(test_df.describe().reset_index())

####################################
# Funnel Chart of the two datasets #
####################################
st.subheader(":bulb: Funnel Chart of Control and Test Group")
st.text("""
Comparing the two funnel charts gives us a more comprehensive perspective on how users progress through each stage—from impression to click to purchase.
""")

funnel_chart_sum = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "funnel"}, {"type": "funnel"}]],
    subplot_titles=('Funnel Chart of Control Group', 'Funnel Chart of Test Group')
)

# Control group
funnel_chart_sum.add_trace(go.Funnel(
    x=[con_df.Impression.sum(), con_df.Click.sum(), con_df.Purchase.sum()],
    y=['Impression', 'Click', 'Purchase'],
    textinfo="value+percent initial",
    texttemplate="%{value:,.2f} (%{percentInitial:.2%})",
    marker=dict(color=["#1f77b4", "#5fa2dd", "#a6c8ea"]),
    showlegend=False
), row=1, col=1)

# Test group
funnel_chart_sum.add_trace(go.Funnel(
    x=[test_df.Impression.sum(), test_df.Click.sum(), test_df.Purchase.sum()],
    y=['Impression', 'Click', 'Purchase'],
    textinfo="value+percent initial",
    texttemplate="%{value:,.2f} (%{percentInitial:.2%})",
    marker=dict(color=["#ff7f0e", "#ffb266", "#ffd699"]),
    showlegend=False
), row=1, col=2)

# fig settings
funnel_chart_sum.update_layout(title_text="Control vs Test Group Funnel Comparison",
                  title_x=0.45,
                  title_font_size=20
                  )
st.plotly_chart(funnel_chart_sum, use_container_width=True)