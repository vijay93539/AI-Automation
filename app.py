from gemini_agent import run_gemini_agent

print("\nGemini Agentic Predictive Maintenance Bot")
print("Enter machine details in natural language.")
print("Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    try:
        result = run_gemini_agent(user_input)

        print("\nBot Analysis:")
        print(result["analysis"])
        print(f"Prediction: {result['prediction']}")
        print(f"Failure Probability: {result['failure_probability_percent']}%")
        print(f"Extracted Values: {result['extracted_values']}")
        print()

    except Exception as e:
        print(f"\nBot: Error occurred -> {e}\n")