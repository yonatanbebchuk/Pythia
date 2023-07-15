from typing import List, Optional

from langchain.chat_models import ChatOpenAI
from llama_index import LLMPredictor, PromptHelper, ServiceContext, GPTSimpleVectorIndex, Document
from llama_index.readers.base import BaseReader

from chat import IChat, ChatRecord


class LlamaIndexReader:
    def __init__(
            self,
            reader: BaseReader,
            load_data_args: Optional[list] = None,
            load_data_kwargs: Optional[dict] = None,
    ):
        self.reader = reader
        self.args = load_data_args or list()
        self.kwargs = load_data_kwargs or dict()

    def load_data(self) -> List[Document]:
        return self.reader.load_data(*self.args, **self.kwargs)


class VectorIndexChat(IChat):
    def __init__(self, index_path: str):
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        self.llm_predictor = LLMPredictor(llm=self.llm)
        self.prompt_helper = PromptHelper(
            max_input_size=4096,
            num_output=256,
            max_chunk_overlap=20,
        )
        self.service_context = ServiceContext.from_defaults(
            llm_predictor=self.llm_predictor,
            prompt_helper=self.prompt_helper,
        )
        self.vector_index = GPTSimpleVectorIndex.load_from_disk(
            save_path=index_path,
            service_context=self.service_context,
        )

    @classmethod
    def from_readers(cls, readers: List[LlamaIndexReader], index_path: str):
        documents = list()
        for reader in readers:
            documents.extend(reader.load_data())
        vector_index = GPTSimpleVectorIndex.from_documents(documents=documents)
        vector_index.save_to_disk(save_path=index_path)
        return VectorIndexChat(index_path=index_path)

    def query(self, prompt: str) -> ChatRecord:
        response = self.vector_index.query(query_str=prompt)
        return ChatRecord(
            messages=[
                dict(role="user", content=prompt),
                dict(role="system", content=response),
            ],
        )
