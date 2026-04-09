from general_dataset_agent import run_general_dataset_agent

questions = [
    "Which machine has the highest torque?",
    "Which machine has the lowest torque?",
    "Which machine has the lowest rotational speed?",
    "How many machines have failed?",
    "What is the average torque?",
    "Show the top 5 machines by tool wear."
]

for q in questions:
    print("\n" + "=" * 80)
    print("QUESTION:", q)

    result = run_general_dataset_agent(q)

    print("STATUS:", result["status"])
    print("GENERATED CODE:")
    print(result["generated_code"])
    print("TOOL RESULT:")
    print(result["tool_result"])
    print("ANALYSIS:")
    print(result["analysis"])