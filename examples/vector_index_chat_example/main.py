from itypewriter import itype
from llama_index import SimpleDirectoryReader

from chat.chats.vector_index_chat import VectorIndexChat, LlamaIndexReader

if __name__ == '__main__':
    vector_index_chat = VectorIndexChat.from_readers(
        readers=[
            LlamaIndexReader(SimpleDirectoryReader(input_dir="archive", recursive=True)),
        ],
        index_path="index.json",
    )
    response = vector_index_chat.query("What is my name and what do I do for a living and who was hitler?")
    itype(str(response), delay=0.01)
