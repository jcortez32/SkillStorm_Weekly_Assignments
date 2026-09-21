from pydantic import BaseModel, Field

# first line of the class needs to be a docstring with model instructions
class Ticket(BaseModel):
    """
    An assessment of a single ticket request. Do not assume facts it does not state
    """

    response: str = Field(
        description=" The response to our company's internal policies. "
    )

    service: str = Field(
        description="The name of the affected service. Copy verbatim from text."
    )

    summary: str = Field(
        description="One sentence summary of the problem. Written in plain english. No jargon or acronyms."
    )

class Diagnosis(BaseModel):
    """A runbook-grounded assessment of an alert.

    Answer ONLY from the runbook excerpts provided to you. The excerpts are the
    company's own operational policy; your own general knowledge about how
    software systems usually behave is NOT a source and must not be used to
    fill a gap.

    If the excerpts do not cover the situation, say so by setting
    `grounded` to false rather than producing a plausible answer.
    """

    grounded: bool = Field(
        description=(
            "True only if the runbook excerpts directly support your answer. "
            "False if you had to rely on general knowledge or guesswork."
        )
    )

    recommended_action: str = Field(
        description=(
            "The next concrete step, as the runbooks describe it. If the "
            "excerpts do not cover this situation, say exactly what is missing "
            "instead of guessing."
        )
    )

    sources: list[str] = Field(
        description=(
            "The exact kb-document filenames you used, copied from the 'source:' line of each excerpt. "
            "If you do not use or have any sources, populate with an empty list. Ex: []"
        )
    )

    requires_approval: bool = Field(
        default=False,
        description=(
            "True if the runbooks say the recommended action needs a second "
            "person's sign-off before it may be carried out."
        ),
    )