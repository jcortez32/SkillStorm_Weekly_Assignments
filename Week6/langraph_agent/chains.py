from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from .llm import get_chat_model
from .schemas import Ticket
from .prompts import GROUNDED_PROMPT

def build_triage_chain() -> Runnable:

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", GROUNDED_PROMPT), 
            ("human", "ticket:\n{ticket}")
        ]
    )

    # making sure the model (ai) responds in a format defined by our model (pydantic)
    structured_model = get_chat_model().with_structured_output(Ticket)

    return prompt | structured_model