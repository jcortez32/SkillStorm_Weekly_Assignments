from langgraph.graph import START, END, StateGraph
from state import IncidentState
from nodes import triage_node

def build_graph(checkpointer=None):
    graph = StateGraph(IncidentState)
    graph.add_node("triage", triage_node)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("diagnose", diagnose_node)
    graph.add_node("reframe", reframe_node)

    graph.add_node("escalate", something)
    graph.add_node("execute", something)