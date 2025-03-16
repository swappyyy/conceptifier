from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse
import requests
import os


# Set your Hugging Face API Key
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Replace with your real API key

# Use a lightweight model
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"

# Initialize FastAPI
app = FastAPI()

class ConceptRequest(BaseModel):
    concept: str
    complexity: str

def generate_explanation(concept, complexity):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    # ✅ Update prompt to avoid repeats
    data = {"inputs": f"Explain {concept} at a {complexity} level in a straightforward and direct way."}

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
        headers=headers,
        json=data
    )

    result = response.json()

    if isinstance(result, list) and "generated_text" in result[0]:
        explanation = result[0]["generated_text"].strip()

        # 🔥 **Remove the first line if it contains unwanted intro**
        explanation_lines = explanation.split("\n")
        if any(phrase in explanation_lines[0].lower() for phrase in ["provide a simple", "explain", "complexity"]):
            explanation_lines.pop(0)  # Remove the first line

        cleaned_explanation = "\n".join(explanation_lines).strip()

        return cleaned_explanation
    else:
        return f"Error: Unable to generate response. API Response: {result}"

@app.get("/test", response_class=PlainTextResponse)
def test_explanation(concept: str = "gravity", complexity: str = "simple"):
    explanation = generate_explanation(concept, complexity)

    # Debugging: Print explanation and return an error message if empty
    print(f"Generated Explanation: {explanation}")

    if not explanation.strip():  # If the response is empty, return an error
        return "Error: No explanation generated. Try a different query."

    return explanation  # Return plain text
