# open ai api key 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
# hugging face access key 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

import requests

# Set your Hugging Face API Key
HUGGINGFACE_API_KEY = "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"  # Replace with your real API key

# Choose a model (e.g., "deepseek-ai/DeepSeek-R1")
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
