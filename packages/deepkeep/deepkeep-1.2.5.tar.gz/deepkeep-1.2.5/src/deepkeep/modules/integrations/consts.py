from enum import Enum


class IntegrationsType(Enum):
    Azure_OpenAI = "Azure_OpenAI"
    OpenAI = "OpenAI"
    Bedrock = "Bedrock"
    # Add more integrations - when ready
