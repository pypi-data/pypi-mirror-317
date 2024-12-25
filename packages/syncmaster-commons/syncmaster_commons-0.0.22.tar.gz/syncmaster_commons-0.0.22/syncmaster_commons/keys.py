from typing import Literal

from pydantic import BaseModel


class QueueCreator(BaseModel):

    name: str
    produced_by: Literal["agent", "user", "celery"]
    consumed_by: Literal["agent", "celery"]
    relevance: str

    def __init__(self, **data):
        super().__init__(**data)
        # Dynamically generate the docstring for this instance
        self.__doc__ = self.generate_doc()

    def generate_doc(self) -> str:
        """
        Generate a detailed docstring for the queue.
        """
        return (
            f"Queue Name: {self.name}\n"
            f"Produced By: {self.produced_by}\n"
            f"Consumed By: {self.consumed_by}\n"
            f"Relevance: {self.relevance}"
        )


class Queues(BaseModel):

    GUPSHUP_RESPONSE_QUEUE: QueueCreator = QueueCreator(
        name="gupshup_response",
        produced_by="agent",
        consumed_by="celery",
        relevance="The queue for Gupshup responses which are sent to user.",
    )

    GUPSHUP_TASK_QUEUE: QueueCreator = QueueCreator(
        name="gupshup_task",
        produced_by="user",
        consumed_by="celery",
        relevance="The queue for Gupshup tasks gets created and consumed by celery.",
    )

    GUPSHUP_ERROR_QUEUE: QueueCreator = QueueCreator(
        name="gupshup_error",
        produced_by="agent",
        consumed_by="celery",
        relevance="The queue for Gupshup errors which are sent to user.",
    )

    AGENT_QUEUE: QueueCreator = QueueCreator(
        name="agent",
        produced_by="celery",
        consumed_by="agent",
        relevance="The queue for agent to execute the task.",
    )

    GOT_NEW_CREDENTIAL_QUEUE: QueueCreator = QueueCreator(
        name="got_new_credential",
        produced_by="user",
        consumed_by="celery",
        relevance="The queue for agent to execute the task.",
    )

    UPDATE_CRED_QUEUE: QueueCreator = QueueCreator(
        name="update_credential",
        produced_by="celery",
        consumed_by="agent",
        relevance="The queue for agent to execute the task of updating credentials.",
    )

    MILVUS_PUSH_NEW_CONTENT_QUEUE: QueueCreator = QueueCreator(
        name="milvus_push_new_content",
        produced_by="user",
        consumed_by="celery",
        relevance="The queue for celery to push new content to Milvus.",
    )


class Exchanges(BaseModel):

    TASK_EXCHANGE: Literal["task_exchange"] = "task_exchange"
    SETTING_EXCHANGE: Literal["setting_exchange"] = "setting_exchange"
    RESPONSE_EXCHANGE: Literal["response_exchange"] = "response_exchange"
    ERROR_EXCHANGE: Literal["error_exchange"] = "error_exchange"
    MILVUS_EXCHANGE: Literal["milvus_exchange"] = "milvus_exchange"


class Keys(BaseModel):
    queue: Queues = Queues()
    exchange: Exchanges = Exchanges()


KEYS = Keys()
