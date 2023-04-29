from chat import IChat, ChatRecord
from chat.chats import OpenAIChat


class InterviewChat(IChat):

    def __init__(self, rounds: int):
        """
        Initialize the interviewer chat and the interviewee chat.
        :param rounds: The number of rounds in which the interviewer prompts the interviewee after the original prompt.
        """
        self.rounds = rounds
        self.interviewee = OpenAIChat(
            name="interviewee",
            purpose="""
            Your purpose is to help respond to a prompt.
            """,
            historic=True,
        )
        self.interviewer = OpenAIChat(
            name="interviewer",
            purpose="""
            Your purpose is to help generate prompts for a ChatGPT instance in order to respond to an original prompt.
            """,
            historic=True,
        )

    def query(self, prompt: str) -> ChatRecord:
        interviewee_record = self.interviewee.query(prompt)
        interviewer_record = ChatRecord()
        for i in range(self.rounds):
            interviewer_record = self.interviewer.query(self.create_interviewer_prompt(prompt, str(interviewee_record)))
            interviewer_recommendation = interviewer_record.messages[-1]["content"]
            interviewee_record = self.interviewee.query(self.create_interviewee_prompt(interviewer_recommendation))
        print(interviewer_record)
        return interviewee_record

    @staticmethod
    def create_interviewer_prompt(prompt: str, interviewee_record: str):
        return f"""
        I want to get a response for {prompt} from a ChatGPT instance.
        The chat record is currently:\n{interviewee_record}.
        What should be my next prompt to get more relevant information?
        """

    @staticmethod
    def create_interviewee_prompt(interviewer_recommendation: str):
        return f"""
        Please respond to the prompt recommended by the following message: {interviewer_recommendation}
        """
