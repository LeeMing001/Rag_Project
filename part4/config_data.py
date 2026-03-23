from ollama import embeddings
from zipp.glob import separate

md5_path="./md5.text"

collection_name="rag"
persist_directory="./chroma_db"


#spliter
chunk_size=1000
chunk_overlap=100
separators=["\n\n","\n",".","!","?","。"]
max_split_char_number=1000

similarity_k=3

embeddings_model_name="Qwen/Qwen3-Embedding-0.6B"
chat_model_name="Qwen/Qwen3-8B"
