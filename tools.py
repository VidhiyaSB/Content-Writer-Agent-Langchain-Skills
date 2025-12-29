from typing import List
from langchain_core.tools import tool, BaseTool
from skills import Skill

def get_skill_loader_tool(skills: List[Skill]) -> BaseTool:
    """Returns a tool that can load skill content based on the provided skills list."""

    @tool
    def load_skill(skill_name: str) -> str:
        """
        Load the full content of a specific writing skill into the agent's context.
        
        Use this tool when you need detailed instructions, templates, or style guides
        for a specific type of writing task (e.g., 'blog_writer', 'social_media', 'technical_writer').
        
        Args:
            skill_name: The name of the skill to load.
        """
        # Find and return the requested skill
        for skill in skills:
            if skill["name"] == skill_name:
                return f"Loaded skill: {skill_name}\n\n{skill['content']}"

        # Skill not found
        available = ", ".join(s["name"] for s in skills)
        return f"Skill '{skill_name}' not found. Available skills: {available}"

    return load_skill
