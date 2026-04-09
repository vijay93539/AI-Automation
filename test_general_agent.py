import time
from general_gemini_agent import run_general_agent

questions = [
    "What is the dataset name?",
    "Which machine has the highest torque?",
    "Which machine has the lowest RPM?",
    "Which machine is at high failure?",
    "Which machine is at low failure?",
    "Machine type is 0, air temperature is 300 K, process temperature is 310 K, rotational speed is 1500 rpm, torque is 50 Nm, and tool wear is 120 min."
]

for q in questions:
    print("\n" + "=" * 80)
    print("QUESTION:", q)

    try:
        result = run_general_agent(q)
        print("RESULT:")
        print(result)
    except Exception as e:
        print("ERROR:")
        print(e)

    time.sleep(3)