from dotenv import load_dotenv
import requests
import os

# Set your Hugging Face API Key
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Replace with your real API key

# Choose a model (e.g., "mistralai/Mistral-7B-Instruct-v0.3")
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"

def generate_explanation(concept, complexity):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    data = {"inputs": f"Explain {concept} in a {complexity} way."}

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
        headers=headers,
        json=data
    )

    result = response.json()
    
    # Print full response for debugging
    print("API Response:", result)

    # Extract text if response is valid
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    else:
        return f"Error: Unable to generate response. API Response: {result}"

# Example usage
concept = input("Please enter a concept you would like to understand: ")
complexity = "simple"
explanation = generate_explanation(concept, complexity)
print("Generated Explanation:", explanation)
