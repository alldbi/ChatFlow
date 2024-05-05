from bot.models.node import NodeFactory
from bot.models.condition import Condition, Operator
from bot.models.flow import Flow
import os
from dotenv import load_dotenv
from assets.prompts import *

load_dotenv()


if __name__ == "__main__":
    start_node = NodeFactory.create_node(prompt_template=decision_prompt,
                                         input_variables=['user_message'],
                                         output_variables={'Scholarly': bool,
                                                           'chitchat': bool},
                                         return_inputs=True)


    chitchat_node = NodeFactory.create_node(prompt_template=chitchat_prompt,
                                            input_variables=['user_message'],
                                            output_variables='response',
                                            is_output=True)


    persist_directory = os.path.join(os.getcwd(), "data")
    docs_dir = os.path.join(os.getcwd(), "Candidate Set Sampling for Evaluating Top-N Recommendation.pdf")
    retrieval_node = NodeFactory.create_retrieval(input_variables=['user_message'],
                                                  output_variables='context',
                                                  persist_directory=persist_directory,
                                                  collection_name='test-retrieval',
                                                  docs_dir=docs_dir,
                                                  k_result=3,)

    node_retrieval_qa = NodeFactory.create_node(prompt_template=retieval_prompt_template,
                                                input_variables=['user_message', 'context'],
                                                output_variables='response',
                                                is_output=True)

    start_node.set_next_item({retrieval_node: Condition('Scholarly', True, Operator.EQUALS),
                              chitchat_node: Condition('chitchat', True, Operator.EQUALS)})
    retrieval_node.set_next_item(node_retrieval_qa)

    flow_bot = Flow(start_node=start_node)
    flow_bot.initialize()

    inp = {'user_message': "Hey, how is it going?"}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20*"@")

    inp = {'user_message': "Who are the authors of the paper?"}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20*"@")

    inp = {'user_message': "In less than 40 words, give a summary about the abstract of the paper?"}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20*"@")

    inp = {'user_message': "In less than 40 words, give a summary about the result and conclusion of the paper?"}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20*"@")
