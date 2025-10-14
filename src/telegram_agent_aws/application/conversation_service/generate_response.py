from langgraph.checkpoint.memory import MemorySaver

from telegram_agent_aws.application.conversation_service.workflow.graph import create_workflow_graph


def get_agent_response(payload: dict, user_id: int):
    config = {
        "configurable": {"thread_id": str(user_id)}
    }
    memory = MemorySaver()
    graph = create_workflow_graph().compile(checkpointer=memory)

    return graph.invoke(payload, config)
