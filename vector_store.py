from langchain_chroma import Chroma
import config_data as config
from langchain_community.embeddings import DashScopeEmbeddings

class VectorStoreService:
    def __init__(self,embedding):
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": 2})

if __name__ == "__main__":
    embedding = DashScopeEmbeddings(model="text-embedding-v4")
    service = VectorStoreService(embedding)
    retriever = service.get_retriever()
    query = "160cm的穿什么衣服"
    res = retriever.invoke(query)
    print(res)