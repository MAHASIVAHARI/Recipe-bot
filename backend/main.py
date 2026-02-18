import os
import json
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/")
def read_root():
    return {"message": "AI Recipe Backend is running 🚀"}


# =========================
# 🔥 RECIPE ENDPOINT
# =========================
@app.post("/generate-recipe")
def generate_recipe(data: dict):
    ingredients = data.get("ingredients")
    diet = data.get("diet")

    prompt = f"""
Generate a recipe strictly in JSON format:

{{
  "name": "Recipe Name",
  "ingredients": [
      {{"item": "ingredient1", "calories": "calories value"}},
      {{"item": "ingredient2", "calories": "calories value"}}
  ],
  "steps": ["Step 1", "Step 2"],
  "total_calories": "Approx total calories",
  "protein": "Approx protein grams"
}}

Ingredients provided: {ingredients}
Diet preference: {diet}

Return ONLY valid JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict JSON generator. "
                    "Return ONLY valid JSON. "
                    "No explanation. No markdown. No extra text."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown formatting
    content = re.sub(r"^```json", "", content)
    content = re.sub(r"^```", "", content)
    content = re.sub(r"```$", "", content)
    content = content.strip()

    try:
        # Extract JSON safely
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            clean_json = json_match.group()
            return json.loads(clean_json)
        else:
            raise ValueError("No JSON object found")
    except Exception as e:
        print("Recipe JSON parse error:", e)
        return {
            "name": "AI Generated Recipe",
            "ingredients": [],
            "steps": [content],
            "total_calories": "Not available",
            "protein": "Not available"
        }


# =========================
# 🛒 GROCERY ENDPOINT
# =========================
@app.post("/generate-grocery")
def generate_grocery(data: dict):
    ingredients = data.get("ingredients")

    prompt = f"""
Generate a grocery shopping list strictly in JSON format:

{{
  "items": [
      {{"name": "ingredient1", "quantity": "estimated quantity"}},
      {{"name": "ingredient2", "quantity": "estimated quantity"}}
  ]
}}

Based on these ingredients: {ingredients}

Return ONLY valid JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict JSON generator. "
                    "Return ONLY valid JSON. "
                    "No explanation. No markdown."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    content = re.sub(r"^```json", "", content)
    content = re.sub(r"^```", "", content)
    content = re.sub(r"```$", "", content)
    content = content.strip()

    try:
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            clean_json = json_match.group()
            return json.loads(clean_json)
        else:
            raise ValueError("No JSON object found")
    except Exception as e:
        print("Grocery JSON parse error:", e)
        return {"items": []}
