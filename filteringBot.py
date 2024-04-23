from bot.models.condition import Condition, Operator
from bot.models.node import NodeFactory, RetrievalStrOutputNode
from bot.models.flow import Flow

import os

os.environ["OPENAI_API_KEY"] = "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"


decision_prompt = """
Your job is to classify the query into True or False with the following rules.

<<< Rules >>>
[Rule 1]: Return False if the query is about the movies or any information about the movies.
[Rule 2]: Return False if the query is about a specific year or country.
[Rule 3]: Return False if the query demands information.
[Rule 4]: Return True if the query is like Hi, How are you? Who are you?, What are you?, Thanks, Greeting, Bye, chit-chat style message, etc.
[Rule 5]: Return False if the above rules are not satisfied.

<<< Query >>> 
{user_message}


- Return the answer in the JSON format with the "rule" and "result" keys.
- 'rule' should be the Rule number that matches with the query.
- 'result' should be the Ture or False without any extra character.
"""

start_node = NodeFactory.create_node(
    model_name="gpt-4-turbo-preview",
    prompt_template=decision_prompt,
    input_variables=["user_message"],
    output_variables={"result": bool, "rule": str},
    return_inputs=True,
    verbose=True,
)


chitchat_prompt = """
You are a chatbot named FinitX.
Your role involves responding to inquiries about movies and offering users valuable information from the netflix. 
Please answer the question.

<<< Question >>>
{user_message}

<<< Rules >>>
[Rule 1] Do not return information that is not mentioned in the Information section. Say "sorry, I don't have any relevant information.".

Answer:
"""

chitchat_node = NodeFactory.create_node(
    model_name="gpt-4-turbo",
    prompt_template=chitchat_prompt,
    input_variables=["user_message"],
    output_variables="response",
    is_output=True,
    verbose=True,
)

retrieval_prompt = """
Answer the question based on the Information.

<< Query >>
{user_message}
<< Information >>
{context}


"""

retrieval_node = RetrievalStrOutputNode(
    model_name="gpt-4-turbo",
    prompt_template=retrieval_prompt,
    input_variables=["user_message"],
    output_variables="response",
    context_var="context",
    query_var = "user_message",
    is_output=True,
    verbose=True,
    docs_dir="netflix_test.csv",
    collection_name="netflix",
    persist_directory="netflix",
    content_cols=["title", "description"],
    metadata_cols=["cast", "country", "release_year", "type"],
    k_result=3,
)


start_node.set_next_item(
    {
        chitchat_node: Condition("result", True, Operator.EQUALS),
        retrieval_node: Condition("result", False, Operator.EQUALS),
    }
)


customer_service_flow = Flow(start_node=start_node)
inp = {"user_message": "Can you tell me about new Start War movies?"}
print(customer_service_flow.run(inp))
