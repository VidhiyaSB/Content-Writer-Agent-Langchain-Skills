# Content Writing Agent (LangChain Skills)

A "Progressive Disclosure" Content Writing Agent built with LangChain and LangGraph. This agent dynamically loads specialized writing "skills" (defined as Markdown files) only when needed, allowing for a lightweight and flexible architecture.

## Features

- **Progressive Disclosure**: The agent knows *about* all available skills but loads the heavy instruction context only on demand.
- **Dynamic Skills**: Skills are defined in simple `.md` files in the `skills/` directory. Adding a new skill is as easy as adding a file.
- **LangGraph Architecture**: Uses a graph-based flow for agent execution.
- **Streaming Output**: See real-time tool calls and responses.

## Why this Architecture?

Traditional agents often dump all instructions into the system prompt at once. This approach solves two problems:

1.  **Token Efficiency**: You don't pay for the tokens of 20+ skills when you only use one. The agent starts with a lightweight "menu" of options.
2.  **Context clarity**: The agent isn't confused by conflicting instructions from different skills. It loads *exactly* what it needs, when it needs it.

## Prerequisites

- Python 3.9+
- API Key for **Mistral AI** (`MISTRAL_API_KEY`) or **OpenAI** (`OPENAI_API_KEY`).

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/VidhiyaSB/Content-Writer-Agent-Langchain-Skills.git
    cd Content-Writer-Agent-Langchain-Skills
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Set up environment variables:
    Create a `.env` file in the root directory and add your API key:
    ```ini
    MISTRAL_API_KEY=your_mistral_key_here
    # OR
    OPENAI_API_KEY=your_openai_key_here
    ```

## Usage

Run the agent with:

```bash
python main.py
```

### Example Interaction

```text
User: Write a blog post about learning Python.
 --> [Tool Call] load_skill (blog_writer)

Agent: Here is a blog post about learning Python...
[Content generated using the specific blog_writer instructions]
```

## Adding New Skills

1.  Create a new `.md` file in the `skills/` directory (e.g., `tweet_writer.md`).
2.  Add YAML frontmatter with the skill name and description:
    ```markdown
    ---
    name: tweet_writer
    description: Writes viral tweets and threads.
    ---
    
    You are an expert Social Media Manager...
    ```
3.  Restart the agent. It will now be aware of the new skill!

## License

MIT
