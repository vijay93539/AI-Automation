import streamlit as st
from unified_agent import run_unified_agent

st.set_page_config(page_title="Predictive Maintenance AI Agent", layout="wide")

st.title("Predictive Maintenance AI Agent")
st.write("Ask any question about the dataset or machine failure prediction.")

user_query = st.text_area("Enter your question", height=120)

if st.button("Analyze"):

    if not user_query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing with Gemini..."):

            result = run_unified_agent(user_query)

        if result["status"] == "success":

            st.subheader("Answer")
            st.write(result["analysis"])

            if result["task"] == "prediction":
                st.subheader("Prediction Details")

                st.write("Failure Probability:", result["failure_probability_percent"], "%")

                st.write("Prediction:", 
                         "Machine will FAIL" if result["prediction"] == 1 else "Machine will NOT FAIL")

                with st.expander("Input Values"):
                    st.json(result["input_values"])

            if result["task"] == "dataset_analysis":

                with st.expander("Generated Pandas Code"):
                    st.code(result["generated_code"], language="python")

                with st.expander("Tool Result"):
                    st.write(result["tool_result"])

        elif result["status"] == "missing_values":
            st.warning(result["analysis"])

        else:
            st.error(result["analysis"])