from typing import List, Optional, TypedDict
import os
import frontmatter

class Skill(TypedDict):
    """A skill defined by a Markdown file."""
    name: str
    description: str
    content: str
    
def load_skills_from_dir(directory: str) -> List[Skill]:
    """Loads skills from Markdown files in the specified directory."""
    skills: List[Skill] = []
    
    if not os.path.exists(directory):
        print(f"[Warning] Skills directory not found: {directory}")
        return skills

    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            try:
                path = os.path.join(directory, filename)
                post = frontmatter.load(path)
                
                # Use metadata name if available, else filename without extension
                name = post.metadata.get("name", filename.replace(".md", ""))
                description = post.metadata.get("description", "No description provided.")
                content = post.content
                
                skills.append({
                    "name": name,
                    "description": description,
                    "content": content
                })
            except Exception as e:
                print(f"[Warning] Error reading skill file {filename}: {e}")
                
    return skills
