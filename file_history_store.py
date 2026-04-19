try:
    from langchain_community.chat_message_histories import FileChatMessageHistory
except ImportError:  # pragma: no cover
    from langchain.memory import FileChatMessageHistory
