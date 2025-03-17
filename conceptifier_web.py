from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse
import requests
import os

# Load API Key from .env
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Model Name (Hugging Face)
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"

# Initialize FastAPI
app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates directory
templates = Jinja2Templates(directory="templates")

class ConceptRequest(BaseModel):
    concept: str
    complexity: str

# Function to generate explanation
def generate_explanation(concept, complexity):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"inputs": f"Please explain {concept} to me. Explain it at a {complexity} level in a straightforward and direct way."}

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
        headers=headers,
        json=data
    )

    result = response.json()

    if isinstance(result, list) and "generated_text" in result[0]:
        explanation = result[0]["generated_text"].strip()

        # Remove unwanted first lines
        explanation_lines = explanation.split("\n")
        if any(phrase in explanation_lines[0].lower() for phrase in ["provide a simple", "explain", "complexity"]):
            explanation_lines.pop(0)  # Remove the first line

        return "\n".join(explanation_lines).strip()
    else:
        return f"Error: Unable to generate response. API Response: {result}"

# ✅ Serve the frontend
@app.get("/", response_class=PlainTextResponse)
async def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "explanation": None})

# ✅ Handle form submission from the frontend
@app.post("/")
async def handle_explanation(request: Request, concept: str = Form(...), complexity: str = Form(...)):
    explanation = generate_explanation(concept, complexity)
    return templates.TemplateResponse("index.html", {"request": request, "explanation": explanation})

# ✅ API Endpoint for backend usage
@app.get("/test", response_class=PlainTextResponse)
def test_explanation(concept: str = "gravity", complexity: str = "simple"):
    return generate_explanation(concept, complexity)
