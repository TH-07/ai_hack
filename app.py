import streamlit as st
import pandas as pd
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

# Set a tab title
st.set_page_config(page_title="WISE")

# Set a title for your app
st.title("WISE: Wellbeing Insights Streamlined and Explained :owl:")

st.markdown("""
Welcome to WISE, your personal analytical assistant! Please drag and drop a health dataset of your choice in a supported format (e.g., CSV, XLSX).

**Please Note:**

* To ensure optimal performance, please limit the size of your dataset.
* For best results, ensure your dataset is well-structured and contains relevant health data.
* Only upload anonymised, aggregate and open data.

We're here to help you discover insights from your data. Feel free to ask questions or explore visualizations!
""")

# Text input for context with placeholder
context = st.text_input("Can you please describe your role in a sentence? (e.g., Patient, Researcher)", key="context")


# Drag and drop box with accepted file types
uploaded_file = st.file_uploader("Upload your health dataset:", type=['csv', 'xlsx'], key="uploaded_file")

if uploaded_file is not None:
    # Placeholder message for uploaded file
    st.write("File uploaded! Analyzing data...")

    # Read the file into a DataFrame
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    # Extract column names
    column_name_list = df.columns.tolist()

    selected_options = st.multiselect(
    "What data would you like to explore?",
    column_name_list)

    # (Your data analysis code using the uploaded file content, prompt and column name list)

    # Success message after analysis (replace with specific results)
    st.success("Data analysis complete! See summary below.")
else:
    st.info("Drag and drop your dataset here to start exploring!")

# Text input for problem with placeholder
problem = st.text_input("What question would you want to answer with this data?", key="problem")

def generate():
  vertexai.init(project="nhs-ai-health24lon-6306", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-preview-0514",
  )
  responses = model.generate_content(
      [document1, text1],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
  )

  for response in responses:
    print(response.text, end="")

document1 = uploaded_file
text1 = problem 

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

generate()
