from langchain_aws import ChatBedrockConverse
from config import AWS_REGION, BEDROCK_AGENT_MODEL, BEDROCK_MAX_TOKENS
def load_model() -> ChatBedrockConverse:
    """Get Bedrock model client using IAM credentials."""
    return ChatBedrockConverse(
        model=BEDROCK_AGENT_MODEL,
        region_name = AWS_REGION,
        max_tokens = BEDROCK_MAX_TOKENS,
        guardrail_config={
            "guardrailIdentifier": "hq18w3ku7qu9", 
            "guardrailVersion": "1",                                                      
        }
        )

_MODEL : ChatBedrockConverse | None = None

def get_model() -> ChatBedrockConverse:
    global _MODEL
    if _MODEL is None:
        _MODEL = load_model()
    return _MODEL