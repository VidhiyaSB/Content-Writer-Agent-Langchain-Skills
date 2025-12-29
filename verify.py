import asyncio
import uuid
import sys
from langchain_core.messages import HumanMessage
from agent import create_agent

async def verify():
    print("Verifying Content Writing Agent...")
    try:
        agent_graph = create_agent()
    except Exception as e:
        print(f"FAILED: Error initializing agent: {e}")
        return

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    # Test Case: Write a blog post
    # This should trigger the 'load_skill' tool for 'blog_writer'
    query = "Write a short blog post about the benefits of AI in healthcare."
    print(f"\nTest Query: {query}")
    
    tool_called = False
    
    async for event in agent_graph.astream_events(
        {"messages": [HumanMessage(content=query)]},
        config,
        version="v1"
    ):
        kind = event["event"]
        if kind == "on_tool_start":
            print(f" --> Tool Call Detected: {event['name']}")
            if event['name'] == 'load_skill':
                tool_called = True
                print("     ([PASS] Correct tool called!)")

    # Final check
    if tool_called:
        print("\n[PASS] VERIFICATION PASSED: Agent correctly loaded a skill.")
    else:
        print("\n[FAIL] VERIFICATION FAILED: Agent did NOT load a skill.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify())
