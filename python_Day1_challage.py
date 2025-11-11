import streamlit as st
import pandas as pd
import os
import time

# === CONFIG ===
excel_file = "customers.xlsx"
columns = ["Name", "Father Name", "Education"]

# Page config
st.set_page_config(page_title="Customer Entry", layout="centered", page_icon="🕶️")

# === IMPROVED GRADIENT BACKGROUND AND STYLES ===
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1e5799 0%, #207cca 30%, #4facfe 70%, #00f2fe 100%);
    background-attachment: fixed;
}

/* Headings and labels in white */
.stMarkdown, .stTextInput>label {
    color: white !important;
}

/* Make input text visible and styled */
.stTextInput input {
    color: black !important;
    background-color: #f3f5f9 !important;
    border-radius: 10px;
    padding: 8px;
    font-weight: 500;
    border: 1px solid #ccc !important;
}

/* Buttons styling */
.stButton>button {
    background: #00ff88 !important;
    color: black !important;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px;
}

/* Success message box */
.stSuccess {
    background-color: rgba(0, 255, 136, 0.9);
    color: black;
    padding: 15px;
    border-radius: 15px;
    font-size: 18px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# === PAGE HEADER ===
st.markdown(
    "<h1 style='text-align: center; color: white; text-shadow: 2px 2px 10px #000;'>Customer Information Form</h1>", 
    unsafe_allow_html=True
)
st.markdown("---")

# === SESSION STATE ===
if 'show_thanks' not in st.session_state:
    st.session_state.show_thanks = False
if 'just_submitted' not in st.session_state:
    st.session_state.just_submitted = False

# === LOAD & SAVE FUNCTIONS ===
@st.cache_data
def load_data():
    if os.path.exists(excel_file):
        return pd.read_excel(excel_file)
    return pd.DataFrame(columns=columns)

def save_data(df):
    df.to_excel(excel_file, index=False)
    st.cache_data.clear()

df = load_data()

# === FORM SECTION ===
with st.form("customer_form", clear_on_submit=True):
    st.markdown("<h3 style='color: #ffff00;'>Enter Your Details</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", placeholder="e.g. Priya Singh")
    with col2:
        father_name = st.text_input("Father's Name", placeholder="e.g. Rajesh Singh")

    education = st.text_input("Education", placeholder="e.g. MBA Marketing")

    submitted = st.form_submit_button("New Customer", use_container_width=True)

    if submitted:
        if not all([name.strip(), father_name.strip(), education.strip()]):
            st.error("Please fill all fields!")
        elif name.strip() in df["Name"].values:
            st.error(f"{name} is already registered!")
        else:
            new_row = {"Name": name.strip(), "Father Name": father_name.strip(), "Education": education.strip()}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            
            st.session_state.show_thanks = True
            st.session_state.just_submitted = True
            st.success(f"Customer {name.strip()} added successfully!")
            st.balloons()

# === THANK YOU MESSAGE ===
if st.session_state.show_thanks:
    st.markdown("""
    <div style='background: linear-gradient(45deg, #00ff88, #00f2fe); 
                padding: 30px; 
                border-radius: 20px; 
                text-align: center; 
                margin: 30px 0;
                box-shadow: 0 10px 30px rgba(0,0,0,0.4);'>
        <h2 style='color: black; margin:0;'>Thank You!</h2>
        <p style='font-size: 22px; color: black; font-weight: bold; margin:10px 0;'>
            Thanks for sharing the information.<br>
            We will process your request very soon.
        </p>
        <p style='color: #000; font-size: 16px;'>You will be redirected shortly...</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.just_submitted:
        st.session_state.just_submitted = False
        time.sleep(5)
        st.session_state.show_thanks = False
        st.rerun()

# === DISPLAY EXISTING DATA ===
if not df.empty:
    st.markdown("---")
    st.markdown(f"<h2 style='color: white; text-shadow: 1px 1px 5px #000;'>Total Customers: {len(df)}</h2>", unsafe_allow_html=True)
    st.dataframe(
        df.style.set_properties(**{
            'background-color': 'rgba(255,255,255,0.15)',
            'color': 'white',
            'border': '1px solid #00ff88',
            'text-align': 'center'
        }),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No customers yet. Add the first one!")

# === DOWNLOAD BUTTON ===
if not df.empty:
    csv = df.to_csv(index=False).encode()
    st.download_button(
        "Download All Data (CSV)",
        csv,
        "customers_backup.csv",
        "text/csv",
        use_container_width=True
    )
