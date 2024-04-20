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
    decision_prompt = """Categorize the user message into one of the following categories:
        1. ServicePolicy
        2- DatabaseQuery
        3. chitchat

        << USER MESSAGE >>
        {user_message}

        << RULES >>
        1- Put your answer in json format.
        1- The output is a json object that the value of the input message category is TRUE and other output keys are FALSE
        """
    start_node = NodeFactory.create_node(model_name=model_name, prompt_template=decision_prompt,
                                         input_variables=['user_message'],
                                         output_variables={'ServicePolicy': bool,
                                                           'DatabaseQuery': bool,
                                                           'chitchat': bool},
                                         return_inputs=True)

    chitchat_prompt = """You are a warm and friendly Customer Support Representative. 
        chat with the user and ask them if they have questions related to the customer service policies or the database.

        << USER MESSAGE >>
        {user_message}
        BOT RESPONSE:"""
    chitchat_node = NodeFactory.create_node(model_name=model_name, prompt_template=chitchat_prompt,
                                            input_variables=['user_message'],
                                            output_variables='response',
                                            is_output=True)

    retieval_prompt_template = """Answer the following question based on the provided context. Avoid using your own knowledge and adhere to the provided data.

    << query >> 
    {user_message}

    << context >>
    {context}
    """
    persist_directory = os.path.join(os.getcwd(), "policyData")
    docs_dir = os.path.join(os.getcwd(), "accessible-customer-service-policy.pdf")
    retrieval_node = NodeFactory.create_retrieval(model_name=model_name,
                                                  prompt_template=retieval_prompt_template,
                                                  input_variables=['user_message'],
                                                  output_variables='response',
                                                  persist_directory=persist_directory,
                                                  collection_name='test-retrieval',
                                                  docs_dir=docs_dir,
                                                  context_var='context',
                                                  query_var='user_message',
                                                  k_result=4,
                                                  return_inputs=True,
                                                  is_output=True)

    sql_prompt_template = """Answer the following question based on the result, retrieved from the database. Avoid using your own knowledge and adhere to the provided data.

    << query >> 
    {user_message}

    << result >>
    {result}
    """
    db_path = "testDB.db"
    sql_node = NodeFactory.create_sql_node(model_name=model_name,
                                                  prompt_template=sql_prompt_template,
                                                  input_variables=['user_message'],
                                                  output_variables='response',
                                                  db_path=db_path,
                                                  result='result',
                                                  return_inputs=True,
                                                  is_output=True)

    start_node.set_next_item({retrieval_node: Condition('ServicePolicy', True, Operator.EQUALS),
                              sql_node: Condition('DatabaseQuery', True, Operator.EQUALS),
                              chitchat_node: Condition('chitchat', True, Operator.EQUALS)})

    flow_bot = Flow(start_node=start_node)

    inp = {'user_message': "Hi. My name is Henry."}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20 * "@")

    inp = {'user_message': "Could you please provide an overview of your company's policies regarding communication with customers?"}
    res = retrieval_node.run(inp)
    print(inp)
    print(res)
    print(20 * "@")

    inp = {'user_message': "How many customer orders have you received so far?"}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20 * "@")
