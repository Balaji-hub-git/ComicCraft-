import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_story(outline: list) -> str:
    """Generates a detailed comic story with narration and character dialogue from panel outlines using Gemini 1.5 Pro."""
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    
    formatted_outline = "\n".join([f"Panel {i+1}: {item.get('title')} - {item.get('scene_description')}" for i, item in enumerate(outline)])
    
    prompt = f"""
You are a professional comic book writer.

Given the following panel breakdown, write a comic-style story with engaging narration and character dialogues for each panel.

Panel Outline:
{formatted_outline}

Guidelines:
- Use a fun and engaging tone, like an actual comic book.
- Include narration and clearly marked character lines.
- Keep each panel self-contained, but part of a cohesive story.
- Precede each section with **Panel 1**, **Panel 2**, etc.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating story: {str(e)}"