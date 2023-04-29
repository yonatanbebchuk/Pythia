from chat import (
    IChat,
    ChatRecord,
)
from openai_api import (
    OpenAIChatCompletionAPI,
    OpenAIChatCompletionAPIRequest,
)


class OpenAIChat(IChat):

    def __init__(
            self,
            name: str,
            purpose: str,
            historic: bool = False,
    ):
        """
        Initialize the OpenAI api facade.
        :param name: The name of the instance of ChatGPT.
        :param purpose: The initial message from "role": "system".
        :param historic: If true query with chat history.
        """
        self.name = name
        self.purpose = purpose
        self.historic = historic

        self.chat_completion = OpenAIChatCompletionAPI()
        if self.historic:
            self.chat_record = self.create_base_record()

    def query(self, prompt: str) -> ChatRecord:
        query_record = self.create_query_record(prompt)
        api_response = self.chat_completion.create(
            request=OpenAIChatCompletionAPIRequest(
                messages=query_record.messages,
            ),
        )
        response = ChatRecord(messages=api_response.messages)
        query_record.extend(response)
        return query_record

    def create_query_record(self, prompt: str) -> ChatRecord:
        prompt_record = self.create_prompt_record(prompt)
        if not self.historic:
            query_record = self.create_base_record()
            query_record.extend(prompt_record)
            return query_record
        self.chat_record.extend(prompt_record)
        return self.chat_record

    def create_base_record(self) -> ChatRecord:
        return ChatRecord(messages=[{"role": "system", "content": self.purpose}])

    @staticmethod
    def create_prompt_record(prompt: str) -> ChatRecord:
        return ChatRecord(messages=[{"role": "user", "content": prompt}])
