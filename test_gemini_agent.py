from gemini_agent import run_gemini_agent

query = "Machine type is 0, air temperature is 300 K, process temperature is 310 K, rotational speed is 1500 rpm, torque is 50 Nm, and tool wear is 120 min."

result = run_gemini_agent(query)
print(result)