import os
import json
from dotenv import load_dotenv
from google import genai

from tools.dataframe_exec_tool import run_dataframe_code

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def run_general_dataset_agent(user_query: str):
    code_prompt = f"""
You are a pandas data analyst.

A pandas DataFrame named df is already available.

The dataset columns are:
- Product ID
- Type
- Air temperature [K]
- Process temperature [K]
- Rotational speed [rpm]
- Torque [Nm]
- Tool wear [min]
- Machine failure
- TWF
- HDF
- PWF
- OSF
- RNF

Write Python pandas code to answer the user's question.

Rules:
1. Use only the existing dataframe: df
2. Do not import anything
3. Do not define functions
4. Store the final answer in a variable named result
5. Return ONLY valid JSON in this format:

{{
  "code": "result = df.head()"
}}

User question:
{user_query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=code_prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    parsed = json.loads(text)
    code = parsed["code"]

    tool_output = run_dataframe_code(code)

    if "error" in tool_output:
        return {
            "status": "error",
            "generated_code": code,
            "analysis": f"Error while analyzing the dataset: {tool_output['error']}"
        }

    explanation_prompt = f"""
You are a predictive maintenance data analyst.

User question:
{user_query}

Python code used:
{code}

Tool result:
{tool_output['result']}

Explain the answer clearly for a beginner.
Answer only based on the tool result.
Do not invent facts.
"""

    explanation_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=explanation_prompt
    )

    return {
        "status": "success",
        "generated_code": code,
        "tool_result": tool_output["result"],
        "analysis": explanation_response.text
    }