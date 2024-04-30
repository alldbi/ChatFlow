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
    Story: User may ask bot to tell a short english story.
    In case of uncertainty regarding the next response, prompt the user for 
    direction on how to contribute to their English language development. This could involve 
    exploring new vocabulary, learning grammar concepts, or discussing specific topics.
    
    Categorize the user message into one of the following categories:
        1. vocabulary
        2. grammar
        3. englishchat
        4. story

        << USER MESSAGE >>
        {user_message}

        << RULES >>
        1- Put your answer in json format.
        2- The output is a json object that the value of the input message 
        category is TRUE and other output keys are FALSE
        

        """
    start_node = NodeFactory.create_node(prompt_template=decision_prompt,
                                         input_variables=['user_message'],
                                         output_variables={'vocabulary': bool,
                                                           'grammar': bool,
                                                           'englishchat': bool,
                                                           'story': bool},
                                         return_inputs=True,
                                         model_name=model_name)


    englishchat_prompt = '''
    Prompt:
    You're interacting with an interactive and educational AI companion 
    designed to support users in refining their English language skills.

    << RULES >>

    RULES 1: Engage in conversational practice with the user to improve their informal English proficiency.
    RULES 2: Encourage an interactive exchange resembling a game of ping pong, involving questions and answers.
    Initiate simple inquiries with the user.
    RULES 3: Maintain a seamless flow of conversation throughout the interaction.


    << USER MESSAGE >>
    {user_message}

    << BOT RESPONSE >>
        '''

    story_prompt = """Deliver original short stories in English
        to users upon request. Engage users with captivating narratives crafted by the chatbot.
        << USER MESSAGE >>
        {user_message}

    BOT RESPONSE:"""
    
    story_node = NodeFactory.create_node(prompt_template=story_prompt,
                                            input_variables=['user_message'],
                                            output_variables='response',
                                            is_output=True,
                                            model_name=model_name)

    englishchat_node = NodeFactory.create_node(prompt_template=englishchat_prompt,
                                            input_variables=['user_message'],
                                            output_variables='response',
                                            is_output=True,
                                            model_name=model_name)


    retieval_prompt_template = """
    As an adept retrieval chatbot specializing in vocabulary enhancement, 
    your primary objective is to aid users in broadening their lexicon. Given 
    a context, swiftly locate and present specific words along with their meanings, 
    usage, and related exercises to the user.

    << Query >>
    {user_message}

    << Context >>
    {context}
    """
    persist_directory = os.path.join(os.getcwd(), "examples","e5","data")
    docs_dir = os.path.join(os.getcwd(), "examples","e5","test1.pdf")
    retrieval_node = NodeFactory.create_retrieval(prompt_template=retieval_prompt_template,
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
    retrieval_node2 = NodeFactory.create_retrieval(prompt_template=retieval_prompt_template2,
                                        input_variables=['user_message'],
                                        output_variables='response',
                                        persist_directory=persist_directory,
                                        collection_name='test-retrieval2',
                                        docs_dir=docs_dir,
                                        context_var='context',
                                        query_var='user_message',
                                        k_result=4,
                                        return_inputs=True,
                                        is_output=True,
                                        model_name=model_name)
    


    start_node.set_next_item({retrieval_node: Condition('vocabulary', True, Operator.EQUALS),
                              retrieval_node2: Condition('grammar', True, Operator.EQUALS),
                              englishchat_node: Condition('englishchat', True, Operator.EQUALS),
                              story_node: Condition('story', True, Operator.EQUALS)})

    flow_bot = Flow(start_node=start_node)
    flow_bot.initialize()
   
    while(True):
        query = input("Ask me here:  ")
        if query == "exit":
            break
        inp = {'user_message': query}
        answer = flow_bot.run(inp)
        print ("____________________Your Answer___________________________")
        print(answer['response'])
        print ("__________________________________________________________")
    

