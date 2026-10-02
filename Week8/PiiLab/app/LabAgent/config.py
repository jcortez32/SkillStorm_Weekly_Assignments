import os 
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.environ["AWS_REGION"]
BEDROCK_AGENT_MODEL = os.environ["BEDROCK_AGENT_MODEL"]
BEDROCK_MAX_TOKENS = int(os.environ["BEDROCK_MAX_TOKENS"])