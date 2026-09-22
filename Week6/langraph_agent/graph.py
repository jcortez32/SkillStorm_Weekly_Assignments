from langgraph.graph import START, END, StateGraph
from .state import IncidentState
from .nodes import triage_node, diagnose_node, retrieve_node, reframe_node, response_node, close_node, route_after_diagnose
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from .schemas import Diagnosis, Ticket
from langgraph.checkpoint.memory import InMemorySaver
SERDE = JsonPlusSerializer(allowed_msgpack_modules=[Ticket, Diagnosis])

def build_graph(checkpointer=None):
    graph = StateGraph(IncidentState)
     # --- NODES ---
    graph.add_node("triage", triage_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("diagnose", diagnose_node)
    graph.add_node("reframe", reframe_node)
    graph.add_node("response", response_node)
    graph.add_node("close", close_node)

    # --- EDGES ---
    graph.add_edge(START, "triage")
    graph.add_edge("triage", "retrieve")
    graph.add_edge("retrieve", "diagnose")
    graph.add_conditional_edges("diagnose",
        route_after_diagnose,
        {
            "reframe": "reframe",
            "response": "response"
        }
    )
    graph.add_edge("reframe", "retrieve")
    graph.add_edge("response", "close")
    graph.add_edge("close", END)

    return graph.compile(checkpointer=checkpointer)

def build_graph_with_memory():
    """ builds the graph with a checkpointer so the state can survive an interruption """
    return build_graph(checkpointer=InMemorySaver(serde=SERDE))

if __name__ == "__main__":
    app = build_graph()
    print(app.get_graph().draw_mermaid())