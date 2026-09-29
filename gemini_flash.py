import json
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_outline(user_prompt: str) -> list:
    """Generates a 5-panel comic layout based on the user's story idea using Gemini Flash."""
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    
    prompt = f"""
You are a professional AI comic planner.
Your task is to generate a *strictly formatted* JSON array containing 5 panel descriptions for a comic based on the story idea below:

STORY: "{user_prompt}"

Each JSON object must include:
- "panel" (integer)
- "title" (string)
- "scene_description" (string)
- "image_prompt" (string)

Respond ONLY in this valid JSON format, without any explanations or markdown syntax:
[
  {{
    "panel": 1,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Image prompt for Stable Diffusion"
  }}
]
"""
    try:
        response = model.generate_content(prompt)
        output_text = response.text.strip()
        
        # Strip potential Markdown backticks
        if output_text.startswith("```json"):
            output_text = output_text.replace("```json", "").replace("```", "").strip()
        elif output_text.startswith("```"):
            output_text = output_text.replace("```", "").strip()
            
        panel_data = json.loads(output_text)
        
        if not isinstance(panel_data, list):
            raise ValueError("Gemini response is not a valid list.")
            
        for panel in panel_data:
            if not isinstance(panel, dict) or not all(k in panel for k in ("panel", "title", "scene_description", "image_prompt")):
                raise ValueError(f"Invalid panel format: {panel}")
                
        return panel_data

    except Exception as e:
        print(f"Error generating panel outline: {e}")
        return [{
            "panel": 1,
            "title": "Error Processing Outline",
            "scene_description": f"Failed to parse model output: {str(e)}",
            "image_prompt": user_prompt
        }]