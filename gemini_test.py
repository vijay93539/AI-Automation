import os
from google import genai

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Send a simple test prompt
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain why high torque and high tool wear can cause machine failure in predictive maintenance."
)

print(response.text)