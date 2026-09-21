from .chains import build_triage_chain
from .state import IncidentState 
from rag import format_query
from typing import cast
from retriever import get_retriever
from langchain_core.messages import HumanMessage, SystemMessage
from schemas import Diagnosis
from llm import get_chat_model
from rag import format_docs, enforce_grounding
from prompts import DIAGNOSIS_PROMPT


def triage_node(state: IncidentState) -> dict:
    triage = build_triage_chain().invoke({"ticket": state["ticket"]})

    return {
        "triage": triage,
        "search_query": format_query(triage),
        "evidence": [f"triage: {triage.service}"],
        "trace": ["triage"]
    }

MAX_RETRIEVAL_ATTEMPTS = 2

def retrieve_node(state: IncidentState) -> dict:
    """Fetch documents excerpts for the current search query."""

    query = state.get("search_query") or state["ticket"]
    docs = get_retriever(k=4).invoke(query)
    attempts = state.get("retrieval_attempts", 0) + 1
    return {
        "retrieval_attempts": attempts,
        "evidence": [f"retrieved {len(docs)} excerpt(s) for {query!r}"],
        "messages": [
            HumanMessage(f"Runbook excerpts for {query!r}:\n\n{format_docs(docs)}")
        ],
        "trace": [f"retrieve#{attempts}"],
    }


def diagnose_node(state: IncidentState) -> dict:
    """Produce a Diagnosis, then verify its citations before storing it."""

    convo = list(state["messages"]) + [
        HumanMessage(
            "Using ONLY the runbook excerpts above, diagnose this alert."
        )
    ]
    raw: Diagnosis = cast(
        "Diagnosis",
        get_chat_model()
        .with_structured_output(Diagnosis)
        .invoke([SystemMessage(DIAGNOSIS_PROMPT)] + convo)
    )

    diagnosis = enforce_grounding(raw)
    return {
        "diagnosis": diagnosis,
        "evidence": [
            f"diagnosis grounded={diagnosis.grounded} sources={diagnosis.sources}"
        ],
        "trace": ["diagnose"],
    }


def route_after_diagnose(state: IncidentState) -> str:
    """Grounded? plan it. Not grounded? try a different search, then give up."""

    diagnosis = state.get("diagnosis")
    if diagnosis and diagnosis.grounded:
        return "plan_remediation"
    if state.get("retrieval_attempts", 0) < MAX_RETRIEVAL_ATTEMPTS:
        return "reframe"
    return "escalate"


def reframe_node(state: IncidentState) -> dict:
    """Rewrite the search query and send the graph back to `retrieve`."""

    triage = state.get("triage")
    failed = state.get("search_query", "")
    ask = (
        f"Ticket: {state['ticket'][:300]}\n"
        f"Service: {triage.service if triage else 'unknown'}\n"
        f"Query that found nothing: {failed!r}\n\n"
        "Better query:"
    )
    new_query = (
        get_chat_model(temperature=0.2)
        .invoke([SystemMessage(REFRAME_PROMPT), HumanMessage(ask)])
        .text.strip()
        .strip('"')
    )
    # Fall back to the raw service name rather than looping on an empty string.
    if not new_query:
        new_query = triage.service if triage else state["alert"][:80]
    return {
        "search_query": new_query,
        "evidence": [f"reframed query -> {new_query!r}"],
        "trace": ["reframe"],
    }