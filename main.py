import asyncio
import uuid
import sys
from langchain_core.messages import HumanMessage
from agent import create_agent

async def main():
    print("Initializing Content Writing Agent (Progressive Disclosure)...")
    try:
        agent_graph = create_agent()
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return

    # Create a unique thread ID for this session
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print(f"Session ID: {thread_id}")
    print("Ready! Type your request (or 'exit' to quit).")

    while True:
        try:
            user_input = input("\nUser: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting...")
                break
            
            if not user_input:
                continue

            # Stream the agent's execution
            # We use 'stream' to see the tool calls happening in real-time
            async for event in agent_graph.astream_events(
                {"messages": [HumanMessage(content=user_input)]},
                config,
                version="v1"
            ):
                kind = event["event"]
                
                if kind == "on_tool_start":
                    # Parse arguments to show WHICH skill is being loaded
                    args = event.get('data', {}).get('input', {})
                    arg_str = ""
                    if 'skill_name' in args:
                        arg_str = f"({args['skill_name']})"
                    elif args:
                         arg_str = f"({args})"
                         
                    print(f" --> [Tool Call] {event['name']} {arg_str}")
                
                # Print Final Answer chunks (if streaming supported) or just wait for final output
                # For simplicity in this CLI, we will just look for the final output at the end of the turn
                
            # Fetch the final state to get the last message
            final_state = agent_graph.get_state(config)
            last_message = final_state.values["messages"][-1]
            print(f"\nAgent: {last_message.content}")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
