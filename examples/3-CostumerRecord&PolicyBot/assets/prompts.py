prompt_decision = """Categorize the user message into one of the following categories:
    1. ServicePolicy
    2- DatabaseQuery
    3. chitchat

    << USER MESSAGE >>
    {user_message}

    << RULES >>
    1- Put your answer in json format.
    1- The output is a json object that the value of the input message category is TRUE and other output keys are FALSE
    """
prompt_chitchat = """You are a warm and friendly Customer Support Representative. 
    chat with the user and ask them if they have questions related to the customer service policies or the database.

    << USER MESSAGE >>
    {user_message}
    BOT RESPONSE:"""
prompt_retrieval = """Answer the following question based on the provided context. Avoid using your own knowledge and adhere to the provided data.

    << query >> 
    {user_message}

    << context >>
    {context}
    """
prompt_db_qa = """Answer the following question based on the result, retrieved from the database. Avoid using your own knowledge and adhere to the provided data.

<< query >> 
{user_message}

<< result >>
{result}
"""
