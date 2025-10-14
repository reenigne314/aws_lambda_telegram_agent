from langgraph.checkpoint.memory import MemorySaver

from telegram_agent_aws.application.conversation_service.workflow.graph import create_workflow_graph
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
    reraise=True
)
def get_agent_response(payload: dict, user_id: int):
    config = {
        "configurable": {"thread_id": str(user_id)}
    }
    memory = MemorySaver()
    graph = create_workflow_graph().compile(checkpointer=memory)

    return graph.invoke(payload, config)
