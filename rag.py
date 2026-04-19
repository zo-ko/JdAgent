import os
from operator import itemgetter

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.embeddings import DashScopeEmbeddings

import config_data as config
from file_history_store import FileChatMessageHistory
from vector_store import VectorStoreService


load_dotenv()


def _format_docs(docs) -> str:
    if not docs:
        return "未检索到相关资料。"

    return "\n\n".join(doc.page_content for doc in docs)


class RagService:
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_modal_name)
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是一个服装知识库问答助手。请优先依据参考资料回答，回答要简洁、准确。"
                    "如果参考资料不足以回答，就明确说明不知道，不要编造。\n\n"
                    "参考资料：\n{context}",
                ),
                (
                    "system",
                    "以下是你与用户的历史对话，请结合历史上下文继续回答。",
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "用户问题：{input}"),
            ]
        )
        self.chat_model = init_chat_model(
            model=config.chat_modal_name,
            model_provider="deepseek",
            temperature=0,
        )
        self.parser = StrOutputParser()
        self.chain = self.__get_chain()

    def _get_history(self, session_id: str) -> FileChatMessageHistory:
        os.makedirs(config.chat_history_dir, exist_ok=True)
        file_path = os.path.join(config.chat_history_dir, f"{session_id}.txt")
        return FileChatMessageHistory(file_path=file_path)

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        chain = (
            {
                "context": itemgetter("input") | retriever | RunnableLambda(_format_docs),
                "history": itemgetter("history"),
                "input": itemgetter("input"),
            }
            | self.prompt_template
            | self.chat_model
            | self.parser
        )

        return RunnableWithMessageHistory(
            chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def invoke(self, query: str, session_id: str = "default") -> str:
        return self.chain.stream(
            {"input": query},
            config={"configurable": {"session_id": session_id}},
        )


if __name__ == "__main__":
    service = RagService()
    print(service.invoke("160cm 的女生怎么选衣服？", session_id="demo"))
