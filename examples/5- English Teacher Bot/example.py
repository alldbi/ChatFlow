from bot.models.node import NodeFactory
from bot.models.condition import Condition, Operator
from bot.models.flow import Flow
from dotenv import load_dotenv
import os
from assets.prompts import *

load_dotenv()

if __name__ == "__main__":

    start_node = NodeFactory.create_node(prompt_template=decision_prompt,
                                         input_variables=['user_message'],
                                         output_variables={'vocabulary': bool,
                                                           'grammar': bool,
                                                           'englishchat': bool,
                                                           'story': bool},
                                         return_inputs=True)

    story_node = NodeFactory.create_node(prompt_template=story_prompt,
                                         input_variables=['user_message'],
                                         output_variables='response',
                                         is_output=True)

    englishchat_node = NodeFactory.create_node(prompt_template=englishchat_prompt,
                                               input_variables=['user_message'],
                                               output_variables='response',
                                               is_output=True)

    persist_directory = os.path.join(os.getcwd(), "data")
    docs_dir = os.path.join(os.getcwd(), "test1.pdf")
    retrieval_node = NodeFactory.create_retrieval(input_variables=['user_message'],
                                                  output_variables='context',
                                                  persist_directory=persist_directory,
                                                  collection_name='test-retrieval',
                                                  docs_dir=docs_dir,
                                                  k_result=4, )

    node_1_qa = NodeFactory.create_node(prompt_template=retrieval_prompt_template,
                                        input_variables=['user_message', 'context'],
                                        output_variables='response',
                                        is_output=True)

    persist_directory = os.path.join(os.getcwd(), "data2")
    docs_dir = os.path.join(os.getcwd(), "test2.pdf")
    retrieval_node2 = NodeFactory.create_retrieval(input_variables=['user_message'],
                                                   output_variables='context',
                                                   persist_directory=persist_directory,
                                                   collection_name='test-retrieval2',
                                                   docs_dir=docs_dir,
                                                   k_result=4,)

    node_2_qa = NodeFactory.create_node(prompt_template=retrieval_prompt_template2,
                                        input_variables=['user_message', 'context'],
                                        output_variables='response',
                                        is_output=True)

    start_node.set_next_item({retrieval_node: Condition('vocabulary', True, Operator.EQUALS),
                              retrieval_node2: Condition('grammar', True, Operator.EQUALS),
                              englishchat_node: Condition('englishchat', True, Operator.EQUALS),
                              story_node: Condition('story', True, Operator.EQUALS)})
    retrieval_node.set_next_item(node_1_qa)
    retrieval_node2.set_next_item(node_2_qa)

    flow_bot = Flow(start_node=start_node)
    flow_bot.initialize()

    while (True):
        query = input("Ask me here:  ")
        if query == "exit":
            break
        inp = {'user_message': query}
        answer = flow_bot.run(inp)
        print("____________________Your Answer___________________________")
        print(answer['response'])
        print("__________________________________________________________")
