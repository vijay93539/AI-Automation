import os
import json
from google import genai
from tools.prediction_tool import predict_failure

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

REQUIRED_FIELDS = [
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]


def run_gemini_agent(user_query: str):
    prompt = f"""
You are a predictive maintenance AI assistant.

Extract machine sensor values from the user's message.

Required fields:
- Type
- Air temperature [K]
- Process temperature [K]
- Rotational speed [rpm]
- Torque [Nm]
- Tool wear [min]

Return ONLY valid JSON in this exact structure:

{{
  "Type": 0,
  "Air temperature [K]": 300,
  "Process temperature [K]": 310,
  "Rotational speed [rpm]": 1500,
  "Torque [Nm]": 50,
  "Tool wear [min]": 120
}}

If any value is missing, return ONLY valid JSON in this structure:

{{
  "missing_fields": ["field name 1", "field name 2"]
}}

User message:
{user_query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    extracted_text = response.text.strip()
    extracted_text = extracted_text.replace("```json", "").replace("```", "").strip()

    values = json.loads(extracted_text)

    if "missing_fields" in values:
        return {
            "status": "missing_values",
            "missing_fields": values["missing_fields"],
            "analysis": f"Please provide these missing values: {', '.join(values['missing_fields'])}"
        }

    missing = [field for field in REQUIRED_FIELDS if field not in values]
    if missing:
        return {
            "status": "missing_values",
            "missing_fields": missing,
            "analysis": f"Please provide these missing values: {', '.join(missing)}"
        }

    result = predict_failure(
        Type=int(values["Type"]),
        air_temp=float(values["Air temperature [K]"]),
        process_temp=float(values["Process temperature [K]"]),
        rpm=float(values["Rotational speed [rpm]"]),
        torque=float(values["Torque [Nm]"]),
        tool_wear=float(values["Tool wear [min]"])
    )

    probability_pct = round(result["failure_probability"] * 100, 2)

    explanation_prompt = f"""
You are a predictive maintenance AI assistant.

User query:
{user_query}

Extracted sensor values:
{values}

Model result:
- failure_prediction: {result["failure_prediction"]}
- failure_probability_percent: {probability_pct}

Write a clear, short analysis for a beginner.
Explain whether the machine is at risk and why.
Do not invent sensor values.
"""

    explanation_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=explanation_prompt
    )

    return {
        "status": "success",
        "extracted_values": values,
        "prediction": result["failure_prediction"],
        "failure_probability_percent": probability_pct,
        "analysis": explanation_response.text
    }