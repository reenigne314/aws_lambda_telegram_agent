from langgraph.checkpoint.mongodb import MongoDBSaver

from telegram_agent_aws.infrastructure.mongodb_utils import get_mongodb_client
from telegram_agent_aws.application.conversation_service.workflow.graph import create_workflow_graph


def get_agent_response(payload: dict, user_id: int):
    config = {
        "configurable": {"thread_id": str(user_id)}
    }
    checkpointer = MongoDBSaver(get_mongodb_client())

    graph = create_workflow_graph().compile(checkpointer=checkpointer)

    return graph.invoke(payload, config)
