from inspect_ai.tool import ToolCall
from inspect_ai.model import ChatMessageAssistant, ChatMessage
from inspect_ai.tool._tool_call import ToolCall
from inspect_ai.model import get_model, Model
from inspect_ai.solver import TaskState
from inspect_ai.approval import Approval
from pydantic_core import to_jsonable_python
from typing import Any
from copy import deepcopy
from inspect_ai.model import get_model, Model
from typing import List, Any, Tuple, Literal
from inspect_ai.tool import ToolCall
import logging
from asteroid_sdk.supervision.config import SupervisionDecision

def tool_jsonable(tool_call: ToolCall | None = None) -> dict[str, Any] | None:
    if tool_call is None:
        return None

    return {
        "id": tool_call.id,
        "function": tool_call.function,
        "arguments": tool_call.arguments,
        "type": tool_call.type,
    }

def chat_message_jsonable(message: ChatMessage) -> dict[str, Any]:
    def as_jsonable(value: Any) -> Any:
        return to_jsonable_python(value, exclude_none=True, fallback=lambda _x: None)

    message_data = {
        "role": message.role,
        "content": message.content,
        "source": message.source,
    }

    if isinstance(message, ChatMessageAssistant):
        message_data["tool_calls"] = [tool_jsonable(call) for call in message.tool_calls if call is not None] if message.tool_calls else None

    jsonable = as_jsonable(message_data)
    return deepcopy(jsonable)


def generate_tool_call_change_explanation(original_call: ToolCall, modified_data: dict) -> str:
    """
    Generate a detailed explanation of changes made to a tool call.

    Args:
        original_call (ToolCall): The original tool call.
        modified_data (dict): The modified tool call data.

    Returns:
        str: A formatted explanation of the changes.
    """
    explanation = "Human changed the tool call:\n"
    explanation += f"From: {original_call.function}({', '.join(f'{k}={v}' for k, v in original_call.arguments.items())})\n"
    explanation += f"To: {modified_data['function']}("
    if 'arguments' in modified_data:
        explanation += ', '.join(f"{k}='{v}'" for k, v in modified_data['arguments'].items())
    explanation += ")\n"
    explanation += f"ID: {modified_data.get('id', 'N/A')}\n"
    explanation += f"Type: {modified_data.get('type', 'N/A')}"
    return explanation



async def generate_tool_call_suggestions(task_state: TaskState, n: int, call: ToolCall) -> Tuple[List[Any], List[Any]]:
    """
    Generate N tool call suggestions for the specified tool call.

    Args:
        task_state (TaskState): The current state of the task.
        n (int): The number of tool call suggestions to generate.
        call (ToolCall): The tool call for which to generate suggestions.

    Returns:
        Tuple[List[Any], List[Any]]: A tuple containing lists of last messages and tool options.
    """
    # Deep copy of task_state messages to avoid side-effects
    message_copy = deepcopy(task_state.messages)
    
    # Ensure the last message contains tool calls
    if len(message_copy) > 0 and (not hasattr(message_copy[-1], 'tool_calls') or not message_copy[-1].tool_calls):
        raise ValueError("No tool calls found in the last message.")
    last_message = message_copy[-1]

    last_messages = [last_message]
    tool_options = [tool_jsonable(last_message.tool_calls[0])]

    # Generate alternative tool call suggestions
    model: Model = get_model()
    # Prepare the conversation without the last message
    messages_without_last = message_copy[:-1]
    
        # Find the specified tool call in the last message
    try:
        call_index = next(i for i, tc in enumerate(last_message.tool_calls) if tc.id == call.id)
    except StopIteration:
        raise ValueError("Specified tool call not found in the last message.")

    # Keep only the specified tool call in the last message
    last_message.tool_calls = [last_message.tool_calls[call_index]]

    for _ in range(n):
        output = await model.generate(messages_without_last, tools=task_state.tools)
        generated_message = output.message
        
        if hasattr(generated_message, 'tool_calls') and generated_message.tool_calls:
            if len(generated_message.tool_calls) > 1:
                logging.warning("More than one tool call generated. Using only the first one. More than one tool call for n>1 is not supported yet.")
        
            last_messages.append(generated_message)
            tool_options.append(tool_jsonable(generated_message.tool_calls[0]))

    return last_messages, tool_options


def transform_asteroid_approval_to_inspect_ai_approval(approval_decision: SupervisionDecision) -> Approval:
    """
    Transform an EntropyLabs SupervisionDecision to an InspectAI Approval
    """
    # Map the decision types
    decision_mapping: dict[str, Literal['approve', 'modify', 'reject', 'terminate', 'escalate']] = {
        "approve": "approve",
        "reject": "reject",
        "escalate": "escalate",
        "terminate": "terminate",
        "modify": "modify"
    }

    inspect_ai_decision = decision_mapping[approval_decision.decision]

    # Handle the 'modified' field
    modified = None
    if inspect_ai_decision == "modify" and approval_decision.modified is not None:
        # Create ToolCall instance directly from the modified data
        original_call = approval_decision.modified.original_inspect_ai_call
        # TODO: Figure this one out for N > 1
        tool_kwargs = approval_decision.modified.tool_kwargs or {}
        if original_call is not None:
            modified = ToolCall(id=original_call.id, function=original_call.function, arguments=tool_kwargs, type=original_call.type)


    return Approval(
        decision=inspect_ai_decision,
        modified=modified,
        explanation=approval_decision.explanation
    )