
import streamlit as st
import pandas as pd

# Load your compliance matrix
df = pd.read_excel("Compliance_Assessment_Project.xlsx")

st.title("Privacy Compliance Assessment Tool")

# Loop through all questions
score = 0
for i, row in df.iterrows():
    question = row["Assessment Question"]
    options = row["Response Options"].split(" / ")
    answer = st.radio(question, options, key=i)

    # Simple scoring logic
    if answer == "Yes":
        points = 0
    elif answer == "Partial":
        points = 1
    elif answer == "No":
        points = 2
    else:
        points = 0  # For NA or other cases

    score += points

# Show results
st.subheader("Your Compliance Score")
st.write(f"Total risk points: {score}")

if score > 0:
    st.write("⚠️ Areas needing remediation:")
    for i, row in df.iterrows():
        answer = st.session_state[i]
        if answer in ["No", "Partial"]:
            st.write(f"- {row['Control ID']}: {row['Remediation Guidance']}")
