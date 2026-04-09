import os
import json
from dotenv import load_dotenv
from google import genai

from tools.prediction_tool import predict_failure
from tools.dataset_tool import (
    get_dataset_overview,
    highest_torque_machine,
    lowest_rpm_machine,
    highest_failure_machine,
    lowest_failure_machine
)

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def run_general_agent(user_query: str):
    router_prompt = f"""
You are a predictive maintenance AI assistant.

Classify the user's question into exactly one of these intents:

1. dataset_overview
2. highest_torque_machine
3. lowest_rpm_machine
4. highest_failure_machine
5. lowest_failure_machine
6. prediction
7. unknown

Return ONLY valid JSON.

Examples:

{{"intent": "dataset_overview"}}
{{"intent": "highest_torque_machine"}}
{{"intent": "lowest_rpm_machine"}}
{{"intent": "highest_failure_machine"}}
{{"intent": "lowest_failure_machine"}}

For prediction questions, return:
{{
  "intent": "prediction",
  "values": {{
    "Type": 0,
    "Air temperature [K]": 300,
    "Process temperature [K]": 310,
    "Rotational speed [rpm]": 1500,
    "Torque [Nm]": 50,
    "Tool wear [min]": 120
  }}
}}

If values are missing, return:
{{
  "intent": "prediction",
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
    intent = route.get("intent", "unknown")

    if intent == "dataset_overview":
        result = get_dataset_overview()
        answer = (
            f"Dataset name: {result['dataset_name']}. "
            f"It contains {result['rows']} rows and {len(result['columns'])} columns. "
            f"Columns are: {', '.join(result['columns'])}."
        )

    elif intent == "highest_torque_machine":
        result = highest_torque_machine()
        answer = (
            f"The machine with the highest torque is Product ID {result['Product ID']}. "
            f"Its torque is {result['Torque [Nm]']} Nm."
        )

    elif intent == "lowest_rpm_machine":
        result = lowest_rpm_machine()
        answer = (
            f"The machine with the lowest rotational speed is Product ID {result['Product ID']}. "
            f"Its rotational speed is {result['Rotational speed [rpm]']} rpm."
        )

    elif intent == "highest_failure_machine":
        result = highest_failure_machine()
        answer = (
            f"A high-failure machine in the dataset is Product ID {result['Product ID']}. "
            f"It has Machine failure = {result['Machine failure']} and torque = {result['Torque [Nm]']} Nm."
        )

    elif intent == "lowest_failure_machine":
        result = lowest_failure_machine()
        answer = (
            f"A low-failure machine in the dataset is Product ID {result['Product ID']}. "
            f"It has Machine failure = {result['Machine failure']} and torque = {result['Torque [Nm]']} Nm."
        )

    elif intent == "prediction":
        if "missing_fields" in route:
            return {
                "status": "missing_values",
                "analysis": f"Please provide these missing values: {', '.join(route['missing_fields'])}"
            }

        values = route["values"]

        result = predict_failure(
            Type=int(values["Type"]),
            air_temp=float(values["Air temperature [K]"]),
            process_temp=float(values["Process temperature [K]"]),
            rpm=float(values["Rotational speed [rpm]"]),
            torque=float(values["Torque [Nm]"]),
            tool_wear=float(values["Tool wear [min]"])
        )

        prediction_text = "will fail" if result["failure_prediction"] == 1 else "will not fail"

        answer = (
            f"Based on the model prediction, this machine {prediction_text}. "
            f"Failure probability is {round(result['failure_probability'] * 100, 2)}%."
        )

    else:
        return {
            "status": "unknown",
            "analysis": "I could not understand the question properly."
        }

    return {
        "status": "success",
        "intent": intent,
        "tool_result": result,
        "analysis": answer
    }