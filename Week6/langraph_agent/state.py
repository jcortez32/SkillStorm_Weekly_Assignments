from typing import TypedDict
from typing import TypedDict, Annotated, NotRequired
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from .schemas import Ticket, Diagnosis

import operator

class IncidentState(TypedDict):

    # input
    ticket: str
    messages: Annotated[list[AnyMessage], add_messages]

    # what the model has learned
    triage: NotRequired[Ticket | None]
    evidence: Annotated[list[str], operator.add]
    tool_attempts: int

    # retrieval 
    search_query: NotRequired[str]
    retrieval_attempts: int
    diagnosis: NotRequired[Diagnosis | None]

    # # plan
    # plan: NotRequired[RemediationPlan | None] 
    # approval: NotRequired[str | None]
    # approval_note: NotRequired[str | None]

    # # output
    # status_update: NotRequired[StatusUpdate | None]
    # outcome: NotRequired[str | None]
