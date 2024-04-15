# from bot.models.node import RetrievalStrOutputNode
import sys

sys.path.insert(0, r'D:\UNI\Dpna\Projects\Chat Flow\initial code\ChatFlow')
from bot.models.node import RetrievalNode
from bot.models.node import NodeFactory
from bot.models.condition import Condition, Operator
from bot.models.flow import Flow
import os

os.environ['OPENAI_API_KEY'] = 'sk-...'
model_name = 'gpt-4-turbo-preview'


if __name__ == "__main__":
    decision_prompt = """Categorize the user message into one of the following categories:
        1. Scholarly
        4. chitchat

        << USER MESSAGE >>
        {user_message}

        << RULES >>
        1- Put your answer in json format.
        1- The output is a json object that the value of the input message category is TRUE and other output keys are FALSE
        """
    start_node = NodeFactory.create_node(model_name=model_name, prompt_template=decision_prompt,
                                         input_variables=['user_message'],
                                         output_variables={'Scholarly': bool,
                                                           'chitchat': bool},
                                         return_inputs=True)


    chitchat_prompt = """You are a warm and friendly, yet not so talkative Science Communicator. 
        chat with the user and ask them if they have questions related to the paper they have uploaded.

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
    persist_directory = os.path.join(os.getcwd(), "data")
    docs_dir = os.path.join(os.getcwd(), "Candidate Set Sampling for Evaluating Top-N Recommendation.pdf")
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

    start_node.set_next_item({retrieval_node: Condition('Scholarly', True, Operator.EQUALS),
                              chitchat_node: Condition('chitchat', True, Operator.EQUALS)})

    flow_bot = Flow(start_node=start_node)

    inp = {'user_message': "Hey, how is it going?"}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20*"@")

    inp = {'user_message': "When was the paper published?"}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20*"@")

    inp = {'user_message': "In less than 40 words, give a summary about the abstract of the paper?"}
    res = flow_bot.run(inp)
    print(inp)
    print(res)
    print(20*"@")
