import re
from tools.prediction_tool import predict_failure


def extract_values(user_input: str):
    patterns = {
        "Type": r"Type\s*=\s*(\d+)",
        "air_temp": r"air[_\s]*temp(?:erature)?\s*=\s*([0-9.]+)",
        "process_temp": r"process[_\s]*temp(?:erature)?\s*=\s*([0-9.]+)",
        "rpm": r"rpm\s*=\s*([0-9.]+)",
        "torque": r"torque\s*=\s*([0-9.]+)",
        "tool_wear": r"tool[_\s]*wear\s*=\s*([0-9.]+)",
    }

    values = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            values[key] = float(match.group(1))

    return values


def run_agent(user_input: str):
    values = extract_values(user_input)

    required = ["Type", "air_temp", "process_temp", "rpm", "torque", "tool_wear"]
    missing = [field for field in required if field not in values]

    if missing:
        return {
            "status": "missing_values",
            "message": f"Missing fields: {', '.join(missing)}"
        }

    result = predict_failure(
        Type=int(values["Type"]),
        air_temp=values["air_temp"],
        process_temp=values["process_temp"],
        rpm=values["rpm"],
        torque=values["torque"],
        tool_wear=values["tool_wear"]
    )

    probability_pct = round(result["failure_probability"] * 100, 2)

    if result["failure_prediction"] == 1:
        explanation = (
            f"Failure predicted with probability {probability_pct}%. "
            f"Likely risk is elevated due to the provided sensor conditions."
        )
    else:
        explanation = (
            f"No failure predicted. Failure probability is {probability_pct}%. "
            f"Current sensor conditions appear relatively stable."
        )

    return {
        "status": "success",
        "input_values": values,
        "prediction": result["failure_prediction"],
        "failure_probability_percent": probability_pct,
        "response": explanation
    }