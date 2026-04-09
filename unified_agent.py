import os
import json
from dotenv import load_dotenv
from google import genai

from general_dataset_agent import run_general_dataset_agent
from tools.prediction_tool import predict_failure

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def run_unified_agent(user_query: str):
    router_prompt = f"""
You are a predictive maintenance AI assistant.

Decide whether the user's question is mainly:

1. "dataset_analysis" → if the user is asking about the dataset, machines, columns, averages, counts, max/min values, filtering, comparisons, summaries, etc.

2. "prediction" → if the user is asking whether a machine will fail, its failure probability, risk, or gives sensor values for prediction.

Return ONLY valid JSON.

For dataset analysis, return:
{{
  "task": "dataset_analysis"
}}

For prediction, return:
{{
  "task": "prediction",
  "values": {{
    "Type": 0,
    "Air temperature [K]": 300,
    "Process temperature [K]": 310,
    "Rotational speed [rpm]": 1500,
    "Torque [Nm]": 50,
    "Tool wear [min]": 120
  }}
}}

If prediction values are missing, return:
{{
  "task": "prediction",
  "missing_fields": ["Type", "Torque [Nm]"]
}}

User question:
{user_query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=router_prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    route = json.loads(text)
    task = route.get("task")

    if task == "dataset_analysis":
        result = run_general_dataset_agent(user_query)
        result["task"] = "dataset_analysis"
        return result

    if task == "prediction":
        if "missing_fields" in route:
            return {
                "status": "missing_values",
                "task": "prediction",
                "analysis": f"Please provide these missing values: {', '.join(route['missing_fields'])}"
            }

        values = route["values"]

        pred_result = predict_failure(
            Type=int(values["Type"]),
            air_temp=float(values["Air temperature [K]"]),
            process_temp=float(values["Process temperature [K]"]),
            rpm=float(values["Rotational speed [rpm]"]),
            torque=float(values["Torque [Nm]"]),
            tool_wear=float(values["Tool wear [min]"])
        )

        probability_pct = round(pred_result["failure_probability"] * 100, 2)

        explanation_prompt = f"""
You are a predictive maintenance assistant.

User question:
{user_query}

Extracted sensor values:
{values}

Prediction result:
- failure_prediction: {pred_result["failure_prediction"]}
- failure_probability_percent: {probability_pct}

Explain the result clearly for a beginner.
Do not invent values.
"""

        explanation = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=explanation_prompt
        )

        return {
            "status": "success",
            "task": "prediction",
            "input_values": values,
            "prediction": pred_result["failure_prediction"],
            "failure_probability_percent": probability_pct,
            "analysis": explanation.text
        }

    return {
        "status": "error",
        "analysis": "Could not determine how to process the question."
    }