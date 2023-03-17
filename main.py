from chat.chats import InterviewChat

if __name__ == "__main__":
    interview_chat = InterviewChat(rounds=3)
    result = interview_chat.query("What day is it today?")
    print(result)
