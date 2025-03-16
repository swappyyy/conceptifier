# hugging face access key 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

from fastapi import FastAPI
from pydantic import BaseModel
import requests

# Set your Hugging Face API Key
HUGGINGFACE_API_KEY = "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"  # Replace with your real API key

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
    data = {"inputs": f"Explain {concept} in a {complexity} way."}

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
        headers=headers,
        json=data
    )

    result = response.json()
    
    # Extract text
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    else:
        return f"Error: Unable to generate response. API Response: {result}"

@app.post("/explain")
def explain_concept(request: ConceptRequest):
    explanation = generate_explanation(request.concept, request.complexity)
    return {"concept": request.concept, "explanation": explanation}

@app.get("/")
def home():
    return {"message": "Welcome to the AI Concept Explainer. Use /explain with a POST request."}

@app.get("/test")
def test_explanation():
    example_concept = "Gravity"
    example_complexity = "simple"
    explanation = generate_explanation(example_concept, example_complexity)
    return {"concept": example_concept, "explanation": explanation}

