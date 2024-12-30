from enum import Enum


class IntegrationModels(Enum):
    Azure_OpenAI = "Azure_OpenAI"
    OpenAI = "OpenAI"
    Bedrock = "Bedrock"
    # Add more integrations - when ready
