# from bot.models.node import RetrievalStrOutputNode
import sys

sys.path.insert(0, r'C:\Users\Saeed\Desktop\ChatFlow')
from bot.models.node import NodeFactory
from bot.models.condition import Condition, Operator
from bot.models.flow import Flow
import os

os.environ['OPENAI_API_KEY'] = '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'
model_name = 'gpt-4-turbo-preview'


if __name__ == "__main__":
    
    decision_prompt = """
    English Chat: Users engage in conversational practice for better communication.
    Vocabulary: Users may request guidance on learning new words.
    Grammar: Users may seek a grammatical rule or structure.
    
    Categorize the user message into one of the following categories:
        1. vocabulary
        2. grammar
        3. englishchat

        << USER MESSAGE >>
        {user_message}

        << RULES >>
        1- Put your answer in json format.
        2- The output is a json object that the value of the input message 
        category is TRUE and other output keys are FALSE
        

        """
    start_node = NodeFactory.create_node(model_name=model_name, prompt_template=decision_prompt,
                                         input_variables=['user_message'],
                                         output_variables={'vocabulary': bool,
                                                           'grammar': bool,
                                                           'englishchat': bool},
                                         return_inputs=True)


    englishchat_prompt = '''
    You are an interactive and educational AI companion, dedicated to helping 
    users improve their English language skills. 

    << RULES >>

    RULES 1: You can chat with user to improve their casual english level.
    RULES 2: Your chat should be like ping pong and includes question and answer. 
            Ask user some simple question from user.
    RULES 3: Your chat should be countinious. 
    RULES 4: When you do not know what you should say ask user how can I help you to improve your english level. 
    Learning a vocab or Learning a grammar tips or Talkining a special topic. 

    << USER MESSAGE >>
    {user_message}

    << BOT RESPONSE >>
    '''

    englishchat_node = NodeFactory.create_node(model_name=model_name, prompt_template=englishchat_prompt,
                                            input_variables=['user_message'],
                                            output_variables='response',
                                            is_output=True)


    retieval_prompt_template = """You are an intelligent retrieval chatbot designed 
    to help users expand their vocabulary. You are provided with a context, you can 
    swiftly locate a specific word and provide its meaning, usage, and related exercises 
    to the user.
    
    << query >> 
    {user_message}
    
    << context >>
    {context}
    """
    persist_directory = os.path.join(os.getcwd(), "examples","e5","data")
    docs_dir = os.path.join(os.getcwd(), "examples","e5","test1.pdf")
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


    retieval_prompt_template2 = """You are an intelligent retrieval chatbot designed 
    to assist users in improving their grammar.  You are provided with a context, you can 
    identify grammatical structures, explain rules, and offer corrections or enhancements 
    to the user's English.


    << query >> 
    {user_message}

    << context >>
    {context}
        """


    persist_directory = os.path.join(os.getcwd(), "examples","e5","data2")
    docs_dir = os.path.join(os.getcwd(), "examples","e5","test2.pdf")
    retrieval_node2 = NodeFactory.create_retrieval(model_name=model_name,
                                        prompt_template=retieval_prompt_template2,
                                        input_variables=['user_message'],
                                        output_variables='response',
                                        persist_directory=persist_directory,
                                        collection_name='test-retrieval2',
                                        docs_dir=docs_dir,
                                        context_var='context',
                                        query_var='user_message',
                                        k_result=4,
                                        return_inputs=True,
                                        is_output=True)
    


    start_node.set_next_item({retrieval_node: Condition('vocabulary', True, Operator.EQUALS),
                              retrieval_node2: Condition('grammar', True, Operator.EQUALS),
                              englishchat_node: Condition('englishchat', True, Operator.EQUALS)})

    flow_bot = Flow(start_node=start_node)
   
    while(True):
        query = input("Ask me here:  ")
        if query == "exit":
            break
        inp = {'user_message': query}
        answer = flow_bot.run(inp)
        print ("____________________Your Answer___________________________")
        print(answer['response'])
        print ("__________________________________________________________")
    

