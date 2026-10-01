import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your compliance matrix
df = pd.read_excel("Privacy Compliance Assessment/Compliance_Assessment_Project.xlsx")

st.title("Privacy Compliance Assessment Tool")

score = 0
answers = []

# Loop through all questions
for i, row in df.iterrows():
    question = row["Assessment Question"]
    options = row["Response Options"].split(" / ")

    # Prevent pre-selection
    answer = st.radio(question, options, key=i, index=None)
    answers.append(answer)

    # Scoring logic
    if answer == "Yes":
        points = 0
    elif answer == "Partial":
        points = 1
    elif answer == "No":
        points = 2
    else:
        points = 0  # For NA or skipped
    score += points

# Calculate compliance percentage
max_points = len(df) * 2  # worst case: all "No"
compliance_percentage = 100 - (score / max_points * 100)

# Show results
st.subheader("Your Compliance Score")
st.progress(int(compliance_percentage))
st.write(f"✅ Compliance: {compliance_percentage:.1f}%")

# Color-coded risk posture
if compliance_percentage >= 80:
    st.success("Strong compliance posture")
elif compliance_percentage >= 50:
    st.warning("Moderate compliance posture")
else:
    st.error("High risk – remediation needed")

# Expandable remediation guidance
with st.expander("See remediation guidance"):
    for i, row in df.iterrows():
        if answers[i] in ["No", "Partial"]:
            st.write(f"- {row['Control ID']}: {row['Remediation Guidance']}")

# Pie chart summary
labels = ["Compliant", "Partial", "Non-Compliant"]
values = [
    sum(1 for a in answers if a == "Yes"),
    sum(1 for a in answers if a == "Partial"),
    sum(1 for a in answers if a == "No"),
]

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
st.pyplot(fig)
