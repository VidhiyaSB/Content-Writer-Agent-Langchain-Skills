import os
from typing import List
from dotenv import load_dotenv

from langchain_core.messages import SystemMessage
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph

from skills import load_skills_from_dir
from tools import get_skill_loader_tool

def get_model():
    """Returns the configured Chat Model based on available API keys."""
    load_dotenv()
    
    if os.getenv("MISTRAL_API_KEY"):
        return ChatMistralAI(model="mistral-large-latest")
    elif os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model="gpt-4o")
    else:
        raise ValueError("No valid API key found. Please set MISTRAL_API_KEY or OPENAI_API_KEY.")

def create_agent():
    """Creates the Content Writing Agent with Progressive Disclosure."""
    
    # 1. Load Skills
    skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    skills = load_skills_from_dir(skills_dir)
    
    if not skills:
        print("[Warning] No skills found in 'skills/' directory.")

    # 2. Create Tools
    loader_tool = get_skill_loader_tool(skills)
    tools = [loader_tool]

    # 3. Create System Prompt with Skill Descriptions
    skills_list_str = "\n".join([f"- **{s['name']}**: {s['description']}" for s in skills])
    
    system_prompt = (
        "You are an expert Content Writing Agent.\n"
        "You have access to specialized writing skills. "
        "Do NOT try to write content generically if a specialized skill matches the request.\n\n"
        "## Available Skills\n"
        f"{skills_list_str}\n\n"
        "## Instructions\n"
        "1. Analyze the user's request.\n"
        "2. If a specific skill seems relevant, use the `load_skill` tool to get detailed instructions.\n"
        "3. Once the skill is loaded (you will see the content in a ToolMessage), follow its instructions strictly to generate the content.\n"
        "4. If no specific skill applies, write as a helpful general assistant.\n"
    )

    # 4. Initialize Model
    model = get_model()

    # 5. Create Checkpointer (Memory)
    checkpointer = InMemorySaver()

    # 6. Create Graph
    agent = create_react_agent(
        model,
        tools,
        prompt=system_prompt,
        checkpointer=checkpointer
    )
    
    return agent
