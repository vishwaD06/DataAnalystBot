import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="AI Data Analyst Bot", layout="wide")

# CSS for refined, modern, and professional look
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Open Sans', sans-serif;
            background: linear-gradient(to right, #e3f2fd, #eceff1);
            color: #263238;
        }

        .stApp {
            padding: 2rem;
        }

        .section-box {
            background-color: white;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        }

        h1 {
            color: #00796B;
            text-align: center;
            font-size: 2.3rem;
            margin-bottom: 0.5rem;
        }

        h3 {
            color: #00796B;
            font-weight: 600;
            margin-bottom: 1rem;
        }

        .stButton>button, .stDownloadButton>button {
            border-radius: 8px;
            padding: 10px 18px;
            font-weight: 600;
            background-color: #00796B;
            color: white;
            border: none;
            transition: background-color 0.3s ease;
        }

        .stButton>button:hover, .stDownloadButton>button:hover {
            background-color: #004d40;
        }

        .stTextInput>div>input {
            border-radius: 6px;
            padding: 8px;
            border: 1px solid #90a4ae;
            background-color: #f9f9f9;
        }

        .sidebar .sidebar-content {
            background-color: #eceff1;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>AI Data Analyst Bot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:16px; color: #455a64;'>Upload your CSV, clean, explore, and export insights with ease.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Upload Your File")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

st.sidebar.header("Query Your Data")
query = st.sidebar.text_input("Enter a Pandas query:")

# App Logic
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    
    st.markdown("Data Preview")
    st.dataframe(df.head())
    st.markdown('</div>', unsafe_allow_html=True)

    # Data Cleaning
    
    st.markdown("Data Cleaning")
    if df.isnull().values.any():
        st.info("Missing values detected. Filling them with forward fill method.")
        df.fillna(method='ffill', inplace=True)
    else:
        st.success("No missing values found.")
    st.markdown('</div>', unsafe_allow_html=True)

    # EDA
    
    st.markdown("Exploratory Data Analysis")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

    for col in numeric_cols:
        st.markdown(f"#### Distribution of {col}")
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax, color='#00796B')
        ax.set_xlabel(col)
        st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    # Key Insights
    
    st.markdown("Key Insights")
    if any('sales' in col.lower() for col in df.columns):
        sales_col = [col for col in df.columns if 'sales' in col.lower()][0]
        max_idx = df[sales_col].idxmax()
        min_idx = df[sales_col].idxmin()
        st.write(f"**Highest {sales_col}:** {df[sales_col][max_idx]} at index {max_idx}")
        st.write(f"**Lowest {sales_col}:** {df[sales_col][min_idx]} at index {min_idx}")
    else:
        st.info("No 'sales' column found.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Custom Query
    if query:
        
        st.markdown("Query Result")
        try:
            result = df.query(query)
            st.dataframe(result)
        except Exception as e:
            st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Download CSV
    
    st.markdown("Download Cleaned Data")

    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    cleaned_csv = convert_df_to_csv(df)

    st.download_button(
        label="Download CSV",
        data=cleaned_csv,
        file_name='cleaned_data.csv',
        mime='text/csv'
    )
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Please upload a CSV file from the sidebar to begin.")
