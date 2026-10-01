import streamlit as st
import pandas as pd
import altair as alt

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

# Altair chart summary with custom colors
labels = ["Compliant", "Partial", "Non-Compliant"]
values = [
    sum(1 for a in answers if a == "Yes"),
    sum(1 for a in answers if a == "Partial"),
    sum(1 for a in answers if a == "No"),
]

data = pd.DataFrame({"Status": labels, "Count": values})

if data["Count"].sum() > 0:
    chart = alt.Chart(data).mark_arc(innerRadius=50).encode(
        theta="Count",
        color=alt.Color("Status", scale=alt.Scale(
            domain=["Compliant", "Partial", "Non-Compliant"],
            range=["green", "yellow", "red"]
        )),
        tooltip=["Status", "Count"]
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("📊 Answer some questions to see the compliance distribution chart.")
