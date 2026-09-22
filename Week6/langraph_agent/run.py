from .graph import build_graph_with_memory
from langchain_core.runnables import RunnableConfig
import uuid
from langgraph.types import Command

def print_steps(app, graph_state, config: RunnableConfig):
    for chunk in app.stream(graph_state, config, stream_mode="updates"):
        print("=================================")
        print(chunk)

        if "__interrupt__" in chunk:
            return "interrupted"

        print()

    return "closed"

if __name__ == "__main__":
    app = build_graph_with_memory()

    sample_ticket = (
        "Checkout page times out when using saved cards on the Payment service."
    )

    thread_id = str(uuid.uuid4())
    config: RunnableConfig = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = {
        "ticket": sample_ticket,
        "messages": [],
        "evidence": [],
        "trace": [],
        "retrieval_attempts": 0,
        "tool_attempts": 0
    }

    status: str = "new"
    while status != "closed":
        status = print_steps(app, initial_state, config)

        # handle interruptions
        if status == "interrupted":
            answer = input("approve / reject > ") or "reject"
            state = Command(resume=answer)

    final_state = app.get_state(config).values
    for node in final_state.get("trace", []):
        print(f"{node} ->")
