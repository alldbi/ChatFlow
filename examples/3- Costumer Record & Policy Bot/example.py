from bot.models.node import NodeFactory
from bot.models.condition import Condition, Operator
from bot.models.flow import Flow
import os
from dotenv import load_dotenv
from assets.prompts import *

load_dotenv()

if __name__ == "__main__":
    node_start = NodeFactory.create_node(prompt_template=prompt_decision,
                                         input_variables=['user_message'],
                                         output_variables={'ServicePolicy': bool,
                                                           'DatabaseQuery': bool,
                                                           'chitchat': bool},
                                         return_inputs=True)

    node_chitchat = NodeFactory.create_node(prompt_template=prompt_chitchat,
                                            input_variables=['user_message'],
                                            output_variables='response',
                                            is_output=True)


    persist_directory = os.path.join(os.getcwd(), "policyData")
    docs_dir = os.path.join(os.getcwd(), "accessible-customer-service-policy.pdf")
    node_retrieval = NodeFactory.create_retrieval(input_variables=['user_message'],
                                                  output_variables='context',
                                                  persist_directory=persist_directory,
                                                  collection_name='test-retrieval',
                                                  docs_dir=docs_dir,
                                                  k_result=3)

    node_policy_qa = NodeFactory.create_node(prompt_template=prompt_retrieval,
                                            input_variables=['user_message', 'context'],
                                            output_variables='response',
                                            is_output=True)

    db_path = "testDB.db"
    node_sql_retrieval = NodeFactory.create_sql_node(input_variables=['user_message'],
                                                     output_variables='result',
                                                     db_path=db_path,)

    node_db_qa = NodeFactory.create_node(prompt_template=prompt_db_qa,
                                         input_variables=['user_message', 'result'],
                                         output_variables='response',
                                         is_output=True)

    node_start.set_next_item({node_retrieval: Condition('ServicePolicy', True, Operator.EQUALS),
                              node_sql_retrieval: Condition('DatabaseQuery', True, Operator.EQUALS),
                              node_chitchat: Condition('chitchat', True, Operator.EQUALS)})
    node_sql_retrieval.set_next_item(node_db_qa)
    node_retrieval.set_next_item(node_policy_qa)

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
