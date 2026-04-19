md5_path = "./md5.txt"
collection_name = "rag"
persist_directory = "./chroma_db"
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?","。","！","？"," ",""]
len_func = len
max_split_char_number = 1000
chat_modal_name = "deepseek-chat"
embedding_modal_name = "text-embedding-v4"
chat_history_dir = "./chat_history"
session_config = {
    "configurable":{
        "session_id":"koko"
    }
}
