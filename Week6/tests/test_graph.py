import pytest
from langraph_agent.retriever import load_runbook_chunks
from langraph_agent.graph import build_graph
from langraph_agent.graph import build_graph_with_memory
from langraph_agent.schemas import Diagnosis
from langchain_core.runnables import RunnableConfig
import uuid

# documents load and split as expecte
def test_document_split():
    chunks = load_runbook_chunks()
    assert len(chunks) > 0
    assert isinstance(chunks, list)

# graph has the nodes I think it has
def test_nodes():
    app = build_graph()
    node_names = list(app.nodes.keys())
    assert("triage" in node_names)
    assert("retrieve" in node_names) 
    assert("diagnose" in node_names)
    assert("reframe" in node_names)
    assert("response" in node_names)
    assert("close" in node_names)  

# Confirming routing decisions behaves as expected
def test_routing():
    app = build_graph_with_memory()
    config: RunnableConfig = {
        "configurable": {
            "thread_id": "1234"
        }
    }

    initial_state = {
        "ticket": "Timeout on checkout",
        "retrieval_attempts": 1,
        "diagnosis": Diagnosis(
            grounded=True,
            recommended_action="Flush cache",
            sources=["cache.md"]
        )
    }

    app.update_state(config, initial_state, as_node="diagnose")
    next_node = app.get_state(config).next
    assert "response" in next_node

def test_retry_bound():
    app = build_graph_with_memory()
    config: RunnableConfig = {
        "configurable": {
            "thread_id": "1234"
        }
    }

    initial_state = {
        "ticket": "Timeout on checkout",
        "retrieval_attempts": 2,
        "diagnosis": Diagnosis(
            grounded=False, 
            recommended_action="Flush cache",
            sources=["cache.md"]
        )
    }

    app.update_state(config, initial_state, as_node="diagnose")
    next_node = app.get_state(config).next
    assert "response" in next_node