decision_prompt = """Categorize the user message into one of the following categories:
    1. Scholarly
    2. chitchat

    << USER MESSAGE >>
    {user_message}

    << RULES >>
    1- Put your answer in json format.
    1- The output is a json object that the value of the input message category is TRUE and other output keys are FALSE
    """

chitchat_prompt = """You are a warm and friendly, yet not so talkative Science Communicator. 
    chat with the user and ask them if they have questions related to the paper they have uploaded.

    << USER MESSAGE >>
    {user_message}
    BOT RESPONSE:"""

retieval_prompt_template = """Answer the following question based on the provided context. Avoid using your own knowledge and adhere to the provided data.

<< query >> 
{user_message}

<< context >>
{context}
"""
