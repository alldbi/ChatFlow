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
                                         output_variables={'PriceInquiry': bool,
                                                           'NutritionInquiry': bool,
                                                           'chitchat': bool},
                                         return_inputs=True)

    node_chitchat = NodeFactory.create_node(prompt_template=prompt_chitchat,
                                            input_variables=['user_message'],
                                            output_variables='response',
                                            is_output=True)
    # Dataset columns:
    # ['Unnamed: 0', 'url_for_product', 'product_name', 'product_availability',
    #  'product_calories', 'product_price', 'have_sizes', 'Protein', 'Carbs',
    #  'Fat', 'Salt', 'Saturates', 'Sugars']
    metadata_cols = ['url_for_product', 'product_name']
    price_cols = ['product_name', 'product_price', 'product_availability']
    nutrition_cols = ['product_name', 'product_calories', 'have_sizes', 'Protein', 'Carbs', 'Fat', 'Salt', 'Saturates',
                      'Sugars']
    persist_directory = os.path.join(os.getcwd(), "McDonaldsPrice")
    docs_dir = os.path.join(os.getcwd(), "mcdonalds_dataset.csv")
    node_price_retrieval = NodeFactory.create_retrieval(input_variables=['user_message'],
                                                        output_variables='context',
                                                        persist_directory=persist_directory,
                                                        collection_name='food-price',
                                                        content_cols=price_cols,
                                                        metadata_cols=metadata_cols,
                                                        docs_dir=docs_dir,
                                                        k_result=10)

    node_price_qa = NodeFactory.create_node(prompt_template=prompt_price_retrieval,
                                            input_variables=['user_message', 'context'],
                                            output_variables='response',
                                            is_output=True)

    persist_directory = os.path.join(os.getcwd(), "McDonaldsNutrition")
    docs_dir = os.path.join(os.getcwd(), "mcdonalds_dataset.csv")
    node_nutrition_retrieval = NodeFactory.create_retrieval(input_variables=['user_message'],
                                                            output_variables='context',
                                                            persist_directory=persist_directory,
                                                            collection_name='food-nutrition',
                                                            content_cols=nutrition_cols,
                                                            metadata_cols=metadata_cols,
                                                            docs_dir=docs_dir,
                                                            k_result=4)

    node_nutrition_qa = NodeFactory.create_node(prompt_template=prompt_price_retrieval,
                                                input_variables=['user_message', 'context'],
                                                output_variables='response',
                                                is_output=True)

    node_start.set_next_item({node_price_retrieval: Condition('PriceInquiry', True, Operator.EQUALS),
                              node_nutrition_retrieval: Condition('NutritionInquiry', True, Operator.EQUALS),
                              node_chitchat: Condition('chitchat', True, Operator.EQUALS)})
    node_price_retrieval.set_next_item(node_price_qa)
    node_nutrition_retrieval.set_next_item(node_nutrition_qa)

    flow_bot = Flow(start_node=node_start)
    flow_bot.initialize()

    while True:
        query = input("User:  ")
        if query == "exit":
            break
        inp = {'user_message': query}
        answer = flow_bot.run(inp)
        print("____________________Bot Answer___________________________")
        print(answer['response'])
        print("__________________________________________________________")