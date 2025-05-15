import kagglehub
import pandas as pd
from kagglehub import KaggleDatasetAdapter
from statsmodels.stats.proportion import proportions_ztest
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from scipy.stats import ttest_ind

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

The two tables below are the descriptive statistics
Comparing the mean and std of the Control Group and Test Group, we can find:
1. Impressions are higher in Test Group (Higher mean)
2. The mean of clicks of Control Group is higher (better CTR in control group)
3. Purchase in test group looks a little higher for now, but need to check with further analysis
4. Earnings are higher in Test Group (mean: 2514.89 > mean: 1908.56)
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
Please note that the values are the sum values of the datasets.
From the adding-up values, the overall CTR and CVR is lower in test group.
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
                               title_x=0.40,
                               title_font_size=20
                               )
st.plotly_chart(funnel_chart_sum, use_container_width=True)

####################################
#         Z Test for CTR           #
####################################
st.subheader(":bulb: Z Test for CTR of the two groups")
st.text("""
As we could see from the funnel chart, the CTRs are 5.01% and 3.29% respectively.
Now we use a Z-test to determine whether the difference between the two proportions is statistically significant.
""")

st.text("""
Null Hypothesis (H₀): The click-through rates (CTR) of the control group and the test group are equal.
Alternative Hypothesis (H₁): The CTRs of the two groups are not equal.
""")

clicks_control = con_df.Click.sum()
impressions_control = con_df.Impression.sum()
clicks_test = test_df.Click.sum()
impressions_test = test_df.Impression.sum()

con_ctr = clicks_control / impressions_control
test_ctr = clicks_test / impressions_test

counts = [clicks_control, clicks_test]
nobs = [impressions_control, impressions_test]

z_stat, p_val = proportions_ztest(counts, nobs)

z_test_df_ctr = pd.DataFrame({
    'Z-stat': [z_stat],
    'p-value': [p_val]
})
st.table(z_test_df_ctr)

st.text("""
p-value <0.05, we reject the H₀
This indicates that the difference in CTR between the control and test groups is statistically significant.
""")
####################################
#         Z Test for CVR           #
####################################
st.subheader(":bulb: Z Test for CVR of the two groups")
st.text("""
After analyzing the CTR, we will now assess whether the CVRs show a statistically significant difference.
""")

st.text("""
Null Hypothesis (H₀): The Conversion Rate (CVR) of the control group and the test group are equal.
Alternative Hypothesis (H₁): The CVRs of the two groups are not equal.
""")

purchases_control = con_df.Purchase.sum()
purchases_test = test_df.Purchase.sum()

con_cvr = purchases_control / clicks_control
test_cvr = purchases_test / clicks_test

test_df_cvr = pd.DataFrame({
    'CVR (Control Group)': [con_cvr],
    'CVR (Test Group)': [test_cvr]
})
st.table(test_df_cvr[['CVR (Control Group)', 'CVR (Test Group)']])

counts = [purchases_control, purchases_test]
nobs = [clicks_control, clicks_test]

z_stat, p_val = proportions_ztest(counts, nobs)

z_test_df_cvr = pd.DataFrame({
    'Z-stat': [z_stat],
    'p-value': [p_val]
})
st.table(z_test_df_cvr)

st.text("""
p-value <0.05, we reject the H₀
This indicates that the difference in CVR between the control and test groups is statistically significant.
""")

st.text(" :bulb: The CTR is higher in Control Group.")
st.text(" :bulb: While the CVR is higher in Test Group.")

####################################
#     Violin Chart for Earnings    #
####################################

st.subheader(":bulb: Violin Chart for Earnings")
st.text("""
The violin chart provides a clear view of the distribution for both groups.
And apparently that the earnings are higher in the Test Group.
The highest earning in Control Group is 2497; the median of Test Group is 2544.
""")
# Add a 'Group' column to distinguish control vs test
con_df['Group'] = 'Control'
test_df['Group'] = 'Test'

# Combine both DataFrames
combined_df = pd.concat([con_df, test_df], ignore_index=True)

# Create side-by-side violin plots
fig_violin = px.violin(combined_df, y="Earning", x="Group", box=True, points="all", color="Group")
fig_violin.update_layout(title="Earning Distribution: Control vs Test", violingap=0.3)
st.plotly_chart(fig_violin, use_container_width=True)

####################################
#       T test for Earnings        #
####################################
st.subheader(":bulb: T test for Earnings")
st.text("""
Conduct a T test to compare earnings difference between the control and test groups.
Null Hypothesis (H₀):The mean earnings of the control and test groups are equal.
Alternative Hypothesis (H₁): The mean earnings of the control and test groups are different.
""")

# Run Welch's t-test (does not assume equal variances)
t_stat, p_val = ttest_ind(con_df['Earning'], test_df['Earning'], equal_var=False)
t_test_df_ear = pd.DataFrame({
    't-stat': [t_stat],
    'p-value': [p_val]
})
st.table(t_test_df_ear)

st.text("""
p-value <0.05, we reject the H₀
With the data, it's sufficient to say that the two groups' mean earnings are different.
""")
