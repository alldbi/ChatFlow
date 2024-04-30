# from bot.models.node import RetrievalStrOutputNode
import sys

sys.path.insert(0, r'D:\UNI\Dpna\Projects\Chat Flow\initial code\ChatFlow')
from bot.models.node import NodeFactory
from bot.models.condition import Condition, Operator
from bot.models.flow import Flow
import os

os.environ['OPENAI_API_KEY'] = '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'
model_name = 'gpt-4-turbo-preview'

if __name__ == "__main__":
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
    node_start = NodeFactory.create_node(prompt_template=prompt_decision,
                                         input_variables=['user_message'],
                                         output_variables={'ServicePolicy': bool,
                                                           'DatabaseQuery': bool,
                                                           'chitchat': bool},
                                         return_inputs=True,
                                         model_name=model_name)

    prompt_chitchat = """You are a warm and friendly Customer Support Representative. 
        chat with the user and ask them if they have questions related to the customer service policies or the database.

        << USER MESSAGE >>
        {user_message}
        BOT RESPONSE:"""
    node_chitchat = NodeFactory.create_node(prompt_template=prompt_chitchat,
                                            input_variables=['user_message'],
                                            output_variables='response',
                                            is_output=True,
                                            model_name=model_name)

    prompt_retrieval = """Answer the following question based on the provided context. Avoid using your own knowledge and adhere to the provided data.

    << query >> 
    {user_message}

    << context >>
    {context}
    """
    persist_directory = os.path.join(os.getcwd(), "policyData")
    docs_dir = os.path.join(os.getcwd(), "accessible-customer-service-policy.pdf")
    node_retrieval = NodeFactory.create_retrieval(prompt_template=prompt_retrieval,
                                                  input_variables=['user_message'],
                                                  output_variables='response',
                                                  persist_directory=persist_directory,
                                                  collection_name='test-retrieval',
                                                  docs_dir=docs_dir,
                                                  context_var='context',
                                                  query_var='user_message',
                                                  k_result=4,
                                                  return_inputs=True,
                                                  is_output=True,
                                                  model_name=model_name)

    db_path = "testDB.db"
    node_sql_retrieval = NodeFactory.create_sql_node(input_variables=['user_message'],
                                                  output_variables='response',
                                                  db_path=db_path,
                                                  result='result',
                                                  return_inputs=True,
                                                  model_name=model_name)
    prompt_sql_qa = """Answer the following question based on the result, retrieved from the database. Avoid using your own knowledge and adhere to the provided data.

    << query >> 
    {user_message}

    << result >>
    {result}
    """

    node_sql_qa = NodeFactory.create_node(prompt_template=prompt_sql_qa,
                                            input_variables=['user_message', 'result'],
                                            output_variables='response',
                                            is_output=True,
                                            model_name=model_name)

    node_start.set_next_item({node_retrieval: Condition('ServicePolicy', True, Operator.EQUALS),
                              node_sql_retrieval: Condition('DatabaseQuery', True, Operator.EQUALS),
                              node_chitchat: Condition('chitchat', True, Operator.EQUALS)})
    node_sql_retrieval.set_next_item(node_sql_qa)

    flow_bot = Flow(start_node=node_start)
    flow_bot.initialize()

    inp = {'user_message': "Hi. My name is Henry."}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20 * "@")

    inp = {'user_message': "Could you please provide an overview of your company's policies regarding communication with customers?"}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20 * "@")

    inp = {'user_message': "Are ages of the costumers provided in the database?"}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20 * "@")

    inp = {'user_message': "Give me the names of all the customers."}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20 * "@")

    inp = {'user_message': "What is the time period for your orders?"}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20 * "@")
