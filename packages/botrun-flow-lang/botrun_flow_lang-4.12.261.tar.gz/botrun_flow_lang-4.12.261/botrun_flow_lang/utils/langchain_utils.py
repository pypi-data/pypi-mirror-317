from typing import Dict, List
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage


def litellm_msgs_to_langchain_msgs(msgs: List[Dict]) -> List[BaseMessage]:
    """
    Convert LiteLLM style messages to Langchain messages.

    Args:
        msgs: List of dictionaries with 'role' and 'content' keys

    Returns:
        List of Langchain message objects
    """
    converted_msgs = []
    for msg in msgs:
        role = msg["role"]
        content = msg["content"]

        if role == "system":
            converted_msgs.append(SystemMessage(content=content))
        elif role == "user":
            converted_msgs.append(HumanMessage(content=content))
        elif role == "assistant":
            converted_msgs.append(AIMessage(content=content))
        else:
            raise ValueError(f"Unsupported role: {role}")

    return converted_msgs
