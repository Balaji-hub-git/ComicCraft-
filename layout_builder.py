def build_comic_layout(image_paths: list, full_story: str, outline: list) -> list:
    """Organizes panel information, generated images, and text into a structured layout."""
    story_panels = full_story.split("**Panel")
    story_panels = [f"**Panel{panel}" for panel in story_panels if panel.strip()]

    layout = []
    for idx, (image, text, panel_info) in enumerate(zip(image_paths, story_panels, outline), start=1):
        # Extract narration by removing the main panel heading title line
        lines = text.strip().splitlines()
        cleaned_text = "\n".join(lines[1:]).strip() if len(lines) > 1 else text.strip()
        
        layout.append({
            "panel": idx,
            "title": panel_info.get("title", f"Panel {idx}"),
            "image_path": image,
            "text": cleaned_text,
            "scene_description": panel_info.get("scene_description", ""),
            "image_prompt": panel_info.get("image_prompt", "")
        })

    return layout