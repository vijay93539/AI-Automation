from tools.prediction_tool import predict_failure

result = predict_failure(
    Type=0,
    air_temp=300,
    process_temp=310,
    rpm=1500,
    torque=50,
    tool_wear=120
)

print(result)