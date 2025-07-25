import streamlit as st

rules = [
    {
        "bacteria": "B.C. (Bacillus cereus)",
        "symptoms": {"nausea_vomit", "diarrhea"},
        "stool": {"watery_stool"},
        "food": {"rice_flour_food", "protein_food"},
        "incubation": "30m-6h",
        "details": "มักเกิดจากอาหารแป้งหรือโปรตีนที่ปรุงทิ้งไว้ อาการเด่นคืออาเจียนและถ่ายเหลว"
    },
    {
        "bacteria": "Shigella spp.",
        "symptoms": {"diarrhea", "fever", "stomachache", "bloody_mucus_stool", "high_fever"},
        "stool": {"bloody_mucus_stool"},
        "food": {"protein_food"},
        "incubation": "1-2d",
        "details": "ติดจากอาหารปนเปื้อน มีไข้สูง ถ่ายเป็นมูกเลือด"
    },
    {
        "bacteria": "V.P. (Vibrio parahaemolyticus)",
        "symptoms": {"nausea_vomit", "diarrhea", "stomachache"},
        "stool": {"watery_stool"},
        "food": {"seafood"},
        "incubation": "8-24h",
        "details": "มักพบในอาหารทะเลไม่สุก เช่นหอยนางรมสด อาการหลักคือปวดท้อง ถ่ายเหลว"
    },
    {
        "bacteria": "C.J. (Campylobacter jejuni)",
        "symptoms": {"fever", "chill_fever", "stomachache", "body_ache"},
        "stool": {"watery_stool"},
        "food": {"protein_food"},
        "incubation": "3-5d",
        "details": "พบในสัตว์ปีกไม่สุก มีอาการไข้ หนาวสั่น ปวดเมื่อย"
    }
]

st.set_page_config(page_title="Bacterial Foodborne Illness Diagnostic Tool", layout="wide")
st.title("🔬 Bacterial Foodborne Illness Diagnostic Tool (Clinical Version)")
st.markdown("Please select observed symptoms, stool characteristics, associated foods, and incubation period.")


col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🧬 General Symptoms")
    symptoms_input = set()
    if st.checkbox("Nausea / Vomiting"): symptoms_input.add("nausea_vomit")
    if st.checkbox("Diarrhea"): symptoms_input.add("diarrhea")
    if st.checkbox("Fever"): symptoms_input.add("fever")
    if st.checkbox("Abdominal pain"): symptoms_input.add("stomachache")
    if st.checkbox("Body ache"): symptoms_input.add("body_ache")
    if st.checkbox("Cramping / Tenesmus"): symptoms_input.add("cramp")
    if st.checkbox("Chill + Fever"): symptoms_input.add("chill_fever")
    if st.checkbox("High Fever"): symptoms_input.add("high_fever")

with col2:
    st.subheader("💩 Stool Characteristics")
    stool_input = set()
    if st.checkbox("Watery stool"): stool_input.add("watery_stool")
    if st.checkbox("Milky / cloudy rice water"): stool_input.add("milky_diarrhea")
    if st.checkbox("Bloody mucus"): stool_input.add("bloody_mucus_stool")

with col3:
    st.subheader("🍽️ Suspected Foods")
    food_input = set()
    if st.checkbox("Protein-based (meat, egg, milk)"): food_input.add("protein_food")
    if st.checkbox("Rice / Starch-based foods"): food_input.add("rice_flour_food")
    if st.checkbox("Seafood"): food_input.add("seafood")

st.subheader("⏱️ Incubation Period")
incubation_input = st.selectbox(
    "Estimated time from ingestion to onset of symptoms:",
    ["30m-6h", "6h-24h", "8-24h" , "8-48h" , "1-2d", "3-5d" , "Other"]
)

st.divider()
if st.button("🔍 Run Diagnosis"):
    results = []
    for rule in rules:
        match_score = 0
        match_score += len(rule["symptoms"].intersection(symptoms_input))
        match_score += len(rule["stool"].intersection(stool_input))
        match_score += len(rule["food"].intersection(food_input))
        match_score += 1 if rule["incubation"] == incubation_input else 0
        total_possible = len(rule["symptoms"]) + len(rule["stool"]) + len(rule["food"]) + 1
        percent = round((match_score / total_possible) * 100, 1)
        results.append((percent, rule))

    results.sort(reverse=True, key=lambda x: x[0])
    top_results = [r for r in results if r[0] >= 40]

    if top_results:
        for score, rule in top_results[:3]:
            st.subheader(f"🦠 Likely Pathogen: {rule['bacteria']} ({score}%)")
            st.markdown(f"**Details:** {rule['details']}")
            st.markdown(f"- **Core Symptoms:** {', '.join(rule['symptoms'])}")
            st.markdown(f"- **Stool Pattern:** {', '.join(rule['stool'])}")
            st.markdown(f"- **Associated Foods:** {', '.join(rule['food'])}")
            st.markdown(f"- **Incubation Period:** {rule['incubation']}")
            st.markdown("---")
    else:
        st.warning("No likely pathogens matched the criteria. Please review inputs or consult a specialist.")

st.info(
    "ℹ️ **Clinical Advisory**:\n"
    "- Patients with persistent vomiting, high fever, bloody diarrhea, or signs of dehydration should be referred to a healthcare provider promptly.\n"
    "- Consider stool culture or molecular diagnostics if clinical suspicion remains high despite inconclusive results."
)

st.markdown(
    """
    <div style='text-align: right; font-size: 12px; color: gray; margin-top: 50px;'>
        Developed by <strong>Mr.Kittisak Srimek</strong><br>
        Data compiled by <strong>Dr.Jaravee Sukprasert</strong>
    </div>
    """,
    unsafe_allow_html=True
)