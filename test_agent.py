from agent.agent import run_agent

query = "Type=0, air_temp=300, process_temp=310, rpm=1500, torque=50, tool_wear=120"

result = run_agent(query)
print(result)